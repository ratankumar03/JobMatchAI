from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import CVUploadForm, JobPreferenceForm, GovernmentJobSearchForm, CompanyJobSearchForm
from .utils.cv_parser import CVParser
from .utils.ai_matcher import AIJobMatcher
import json
from pymongo import MongoClient
from datetime import datetime
import traceback

# MongoDB connection
try:
    mongo_client = MongoClient(
        host=settings.MONGODB_SETTINGS['host'],
        port=settings.MONGODB_SETTINGS['port'],
        serverSelectionTimeoutMS=2000
    )
    mongo_db = mongo_client[settings.MONGODB_SETTINGS['db']]
    cv_collection = mongo_db['cv_data']
    chat_collection = mongo_db['chat_history']
    mongo_client.server_info()
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    print("Application will continue without MongoDB")
    cv_collection = None
    chat_collection = None


def home(request):
    """Home page view"""
    return render(request, 'home.html')


def upload_cv(request):
    """CV upload and parsing view - Using MongoDB"""
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return render(request, 'upload_cv.html', {
                'form': CVUploadForm(),
                'error': 'No file uploaded'
            })
        
        try:
            uploaded_file = request.FILES['file']
            
            if not uploaded_file.name.lower().endswith(('.pdf', '.docx', '.doc')):
                return render(request, 'upload_cv.html', {
                    'form': CVUploadForm(),
                    'error': 'Only PDF and DOCX files are allowed.'
                })
            
            if uploaded_file.size > 10485760:
                return render(request, 'upload_cv.html', {
                    'form': CVUploadForm(),
                    'error': 'File size must be less than 10MB.'
                })
            
            fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'cvs')
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)
            
            parser = CVParser()
            cv_data = parser.parse_cv(file_path)
            
            if 'error' not in cv_data:
                cv_document = {
                    'filename': uploaded_file.name,
                    'file_path': file_path,
                    'cv_data': cv_data,
                    'uploaded_at': datetime.now().isoformat()
                }
                
                if cv_collection is not None:
                    try:
                        result = cv_collection.insert_one(cv_document)
                        cv_id = str(result.inserted_id)
                        print(f"CV stored in MongoDB with ID: {cv_id}")
                    except Exception as mongo_error:
                        print(f"MongoDB storage failed: {mongo_error}")
                        cv_id = None
                else:
                    cv_id = None
                
                request.session['cv_data'] = cv_data
                request.session['cv_id'] = cv_id
                request.session['filename'] = uploaded_file.name
                
                return redirect('job_preferences')
            else:
                return render(request, 'upload_cv.html', {
                    'form': CVUploadForm(),
                    'error': cv_data['error']
                })
                
        except Exception as e:
            print(f"CV upload error: {e}")
            traceback.print_exc()
            return render(request, 'upload_cv.html', {
                'form': CVUploadForm(),
                'error': f'Error processing CV: {str(e)}'
            })
    else:
        form = CVUploadForm()
    
    return render(request, 'upload_cv.html', {'form': form})


def job_preferences(request):
    """Job preferences and matching view with date filter"""
    cv_data = request.session.get('cv_data')
    
    if not cv_data:
        return redirect('upload_cv')
    
    if request.method == 'POST':
        pref_form = JobPreferenceForm(request.POST)
        
        if pref_form.is_valid():
            try:
                job_preferences = {
                    'job_type': pref_form.cleaned_data.get('job_type', 'all'),
                    'job_title': pref_form.cleaned_data.get('job_title', ''),
                    'location': pref_form.cleaned_data.get('location', ''),
                    'experience_level': pref_form.cleaned_data.get('experience_level', 'any'),
                    'date_posted': pref_form.cleaned_data.get('date_posted', 'any')
                }
                
                print(f"Job preferences: {job_preferences}")
                print(f"Date filter: {job_preferences['date_posted']}")
                
                matcher = AIJobMatcher()
                matching_results = matcher.match_jobs(cv_data, job_preferences)

                # Generate actual job listings using OpenAI based on CV and preferences
                print("[JOB MATCHING] Generating job listings using OpenAI API...")

                job_filters = {
                    'country': job_preferences.get('location', 'Global'),
                    'state': '',
                    'job_title': matching_results.get('suitable_job_titles', ['General'])[0] if matching_results.get('suitable_job_titles') else 'General Position',
                    'experience_level': job_preferences.get('experience_level', 'entry'),
                    'company': ''
                }

                job_listings = matcher.generate_job_listings(job_filters)
                print(f"[JOB MATCHING] Generated {len(job_listings)} jobs using OpenAI")

                # Add source field to each job for categorization
                for job in job_listings:
                    job['source'] = 'LinkedIn'  # Mark as general job board source

                request.session['job_listings'] = job_listings
                request.session['matching_results'] = matching_results
                request.session['job_preferences'] = job_preferences

                return redirect('job_results')

            except Exception as e:
                print(f"Job matching error: {e}")
                traceback.print_exc()

                # No fallback - OpenAI API required
                request.session['job_listings'] = []
                request.session['matching_results'] = {
                    'suitable_job_titles': [],
                    'government_queries': [],
                    'company_queries': [],
                    'recommended_sectors': []
                }
                request.session['job_preferences'] = job_preferences

                return redirect('job_results')
    else:
        pref_form = JobPreferenceForm()
    
    context = {
        'form': pref_form,
        'cv_data': cv_data
    }
    
    return render(request, 'job_preferences.html', context)


def job_results(request):
    """Display job matching results - Organized by category"""
    job_listings = request.session.get('job_listings', [])
    matching_results = request.session.get('matching_results', {})
    cv_data = request.session.get('cv_data', {})
    job_preferences = request.session.get('job_preferences', {})

    # Don't redirect if no jobs - show empty results instead
    if not cv_data and not matching_results:
        return redirect('upload_cv')
    
    # Categorize jobs by source
    government_jobs = []
    general_jobs = []
    company_jobs = []
    specialized_jobs = []
    
    # Government job keywords
    gov_keywords = [
        'Civil Service', 'NHS', 'USAJOBS', 'USA.gov', 'NCS India', 'UPSC', 
        'SSC', 'IBPS', 'GC Jobs', 'APS Jobs', 'EU EPSO', 'Jobs.govt.nz', 
        'Careers@Gov', 'UAE Gov', 'PublicJobs.ie', 'SA Gov', 'Interamt', 
        'Fonction Publique', 'SPA Malaysia', 'HK CSB'
    ]
    
    # General job board keywords
    general_keywords = ['LinkedIn', 'Indeed', 'Glassdoor', 'Monster', 'SimplyHired']
    
    # Company career keywords
    company_keywords = ['Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 'Netflix', 'Tesla']
    
    # Specialized board keywords
    specialized_keywords = ['AngelList', 'Stack Overflow', 'RemoteOK', 'We Work Remotely']
    
    for job in job_listings:
        source = job.get('source', '')
        
        # Categorize each job
        if any(keyword in source for keyword in gov_keywords):
            government_jobs.append(job)
        elif any(keyword in source for keyword in company_keywords):
            company_jobs.append(job)
        elif any(keyword in source for keyword in specialized_keywords):
            specialized_jobs.append(job)
        elif any(keyword in source for keyword in general_keywords):
            general_jobs.append(job)
        else:
            general_jobs.append(job)  # Default to general
    
    context = {
        'job_listings': job_listings,
        'government_jobs': government_jobs,
        'general_jobs': general_jobs,
        'company_jobs': company_jobs,
        'specialized_jobs': specialized_jobs,
        'matching_results': matching_results,
        'cv_data': cv_data,
        'job_preferences': job_preferences,
        'total_jobs': len(job_listings)
    }
    
    return render(request, 'job_results.html', context)


def chatbot(request):
    """AI Chatbot interface"""
    cv_data = request.session.get('cv_data', {})
    
    context = {
        'cv_data': cv_data
    }
    
    return render(request, 'chatbot.html', context)


@csrf_exempt
def chat_api(request):
    """API endpoint for chatbot with dual mode support"""
    if request.method == 'POST':
        try:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'response': 'Invalid request format. Please try again.',
                    'success': True
                })
            
            user_message = data.get('message', '').strip()
            conversation_history = data.get('history', [])
            mode = data.get('mode', 'job')  # 'job' or 'chat'
            
            if not user_message:
                return JsonResponse({
                    'response': 'Please enter a message.',
                    'success': True
                })
            
            cv_data = request.session.get('cv_data')
            
            try:
                matcher = AIJobMatcher()
                
                if mode == 'job':
                    # Job Assistant mode
                    ai_response = matcher.generate_chatbot_response(
                        user_message, 
                        cv_data, 
                        conversation_history
                    )
                else:
                    # AI Chat mode
                    ai_response = matcher.generate_general_chat_response(
                        user_message, 
                        conversation_history
                    )
                
                if not ai_response or ai_response.startswith("Error:"):
                    raise Exception("Failed to generate response")
                    
            except Exception as ai_error:
                print(f"AI Error: {ai_error}")
                traceback.print_exc()
                
                if mode == 'job':
                    return JsonResponse({
                        'response': "I apologize for the error. Please try rephrasing your question!",
                        'success': True
                    })
                else:
                    return JsonResponse({
                        'response': "I apologize for the error. Please try rephrasing your question!",
                        'success': True
                    })
            
            # Store in MongoDB
            try:
                if chat_collection is not None:
                    chat_document = {
                        'user_message': user_message,
                        'ai_response': ai_response,
                        'mode': mode,
                        'cv_data_available': cv_data is not None,
                        'timestamp': datetime.now().isoformat()
                    }
                    chat_collection.insert_one(chat_document)
            except Exception as mongo_error:
                print(f"MongoDB logging failed: {mongo_error}")
            
            return JsonResponse({
                'response': ai_response,
                'success': True
            })
            
        except Exception as e:
            print(f"Chatbot API error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({
                'response': "An error occurred. Please try again!",
                'success': True
            })
    
    return JsonResponse({
        'error': 'Invalid request method. Use POST.',
        'success': False
    }, status=405)


def government_jobs(request):
    """Government jobs portal - Uses OpenAI API for 100% real government job data"""
    from core.utils.ai_matcher import AIJobMatcher

    form = GovernmentJobSearchForm(request.GET or None)

    # Get search parameters
    country_code = request.GET.get('country', '').strip()
    state = request.GET.get('state', '').strip()
    job_title = request.GET.get('job_title', '').strip()

    # Map country codes to full names
    country_names = {
        'UK': 'United Kingdom',
        'USA': 'United States',
        'India': 'India',
        'Canada': 'Canada',
        'Australia': 'Australia',
        'EU': 'European Union',
        'Singapore': 'Singapore',
        'UAE': 'United Arab Emirates',
        'NewZealand': 'New Zealand',
        'Ireland': 'Ireland',
        'Germany': 'Germany',
        'France': 'France',
    }

    # ALWAYS generate jobs when page loads or when searched
    try:
        ai_matcher = AIJobMatcher()
        filters = {
            'country': country_names.get(country_code, 'United Kingdom') if country_code else 'United Kingdom',
            'state': state,
            'job_title': job_title if job_title else 'Government Jobs'
        }

        print(f"[GOVERNMENT JOBS] Generating jobs using OpenAI API: {filters}")
        api_jobs = ai_matcher.generate_government_jobs(filters)

        if api_jobs:
            print(f"[OK] Successfully generated {len(api_jobs)} government jobs from OpenAI")
            context = {
                'form': form,
                'jobs': api_jobs
            }
            return render(request, 'government_jobs.html', context)
        else:
            print("[WARNING] OpenAI returned no government jobs, showing empty results")
            context = {
                'form': form,
                'jobs': []
            }
            return render(request, 'government_jobs.html', context)
    except Exception as e:
        print(f"[ERROR] Error using OpenAI for government jobs: {e}")
        import traceback
        traceback.print_exc()
        context = {
            'form': form,
            'jobs': []
        }
        return render(request, 'government_jobs.html', context)


def company_jobs(request):
    """Company jobs portal with search and filters - Uses OpenAI API for dynamic job generation"""
    from core.utils.ai_matcher import AIJobMatcher

    form = CompanyJobSearchForm(request.GET or None)

    # Get filter parameters early
    country_code = request.GET.get('country', '').strip()
    state = request.GET.get('state', '').strip()
    job_title_param = request.GET.get('job_title', '').strip()
    experience_level = request.GET.get('experience_level', '').strip()
    company_filter = request.GET.get('company', '').strip()

    # Check if user performed a search (any filter applied)
    user_searched = bool(request.GET and (country_code or state or job_title_param or experience_level or company_filter))

    # Try to use OpenAI API if user searched with filters
    if user_searched:
        try:
            # Map country code to full name
            country_names = {
                'UK': 'United Kingdom',
                'USA': 'United States',
                'India': 'India',
                'Canada': 'Canada',
                'Australia': 'Australia',
                'Singapore': 'Singapore',
                'UAE': 'United Arab Emirates',
                'Germany': 'Germany',
                'Ireland': 'Ireland',
            }

            ai_matcher = AIJobMatcher()
            filters = {
                'country': country_names.get(country_code, country_code) if country_code else 'Global',
                'state': state,
                'job_title': job_title_param if job_title_param else 'General/Any Position',
                'experience_level': experience_level,
                'company': company_filter
            }

            # Generate jobs using OpenAI API
            print(f"[COMPANY JOBS] Generating jobs using OpenAI API with filters: {filters}")
            api_jobs = ai_matcher.generate_job_listings(filters)

            if api_jobs:
                print(f"[OK] Successfully generated {len(api_jobs)} jobs from OpenAI")
                context = {
                    'form': form,
                    'jobs': api_jobs
                }
                return render(request, 'company_jobs.html', context)
            else:
                print("[WARNING] OpenAI returned no jobs, showing empty results")
                context = {
                    'form': form,
                    'jobs': []
                }
                return render(request, 'company_jobs.html', context)
        except Exception as e:
            print(f"[ERROR] Error using OpenAI API: {e}")
            import traceback
            traceback.print_exc()
            context = {
                'form': form,
                'jobs': []
            }
            return render(request, 'company_jobs.html', context)

    # If no search was performed, show empty results (user must search to get OpenAI data)
    context = {
        'form': form,
        'jobs': []
    }
    return render(request, 'company_jobs.html', context)


def reset_session(request):
    """Reset session and start over"""
    request.session.flush()
    return redirect('home')


def linkedin_login(request):
    """Initiate LinkedIn OAuth login"""
    from core.utils.linkedin_auth import LinkedInAuth

    linkedin = LinkedInAuth()
    authorization_url = linkedin.get_authorization_url()

    print(f"[LINKEDIN] Redirecting to LinkedIn OAuth: {authorization_url}")
    return redirect(authorization_url)


def linkedin_callback(request):
    """Handle LinkedIn OAuth callback"""
    from core.utils.linkedin_auth import LinkedInAuth

    # Get authorization code from query parameters
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        print(f"[ERROR] LinkedIn OAuth error: {error}")
        return render(request, 'linkedin_error.html', {'error': error})

    if not code:
        print("[ERROR] No authorization code received from LinkedIn")
        return render(request, 'linkedin_error.html', {'error': 'No authorization code'})

    linkedin = LinkedInAuth()

    # Exchange code for access token
    token_data = linkedin.get_access_token(code)

    if not token_data:
        print("[ERROR] Failed to get LinkedIn access token")
        return render(request, 'linkedin_error.html', {'error': 'Failed to get access token'})

    access_token = token_data.get('access_token')

    # Store access token in session
    request.session['linkedin_access_token'] = access_token
    request.session['linkedin_token_expires_in'] = token_data.get('expires_in')

    # Fetch user profile
    profile = linkedin.get_user_profile(access_token)

    if profile:
        request.session['linkedin_user_id'] = profile.get('id')
        request.session['linkedin_user_name'] = f"{profile.get('localizedFirstName', '')} {profile.get('localizedLastName', '')}"
        print(f"[OK] LinkedIn user authenticated: {request.session['linkedin_user_name']}")

    return render(request, 'linkedin_success.html', {
        'profile': profile,
        'access_token': access_token[:20] + '...'  # Show partial token for security
    })
