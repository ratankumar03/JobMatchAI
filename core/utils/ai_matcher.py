"""
AI Matcher - Matches CV skills with job requirements using OpenAI
Dual mode: Job Assistant (CV-based) and AI Chat (ChatGPT-like)
"""
from openai import OpenAI
from django.conf import settings
import json
import time


class AIJobMatcher:
    """AI-powered job matching system with dual chat modes"""
    
    def __init__(self):
        try:
            self.client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                timeout=30.0,
                max_retries=2
            )
        except Exception as e:
            print(f"Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def match_jobs(self, cv_data, job_preferences):
        """
        Match CV data with job preferences and generate job search queries
        Args:
            cv_data: Extracted CV information
            job_preferences: User's job preferences
        Returns:
            dict: Matching results and search queries
        """
        if not self.client:
            print("OpenAI client not initialized, returning empty results")
            return {
                "suitable_job_titles": [],
                "government_queries": [],
                "company_queries": [],
                "recommended_sectors": []
            }
        
        try:
            prompt = f"""
            Based on this candidate profile, suggest the best job search queries and job titles:
            
            Skills: {cv_data.get('skills', '')}
            Experience: {cv_data.get('experience_years', '0')} years
            Education: {cv_data.get('education', '')}
            Previous Jobs: {cv_data.get('job_titles', '')}
            Industries: {cv_data.get('industries', '')}
            
            Job Preferences:
            - Job Type: {job_preferences.get('job_type', 'all')}
            - Desired Role: {job_preferences.get('job_title', 'any')}
            - Location: {job_preferences.get('location', 'any')}
            - Experience Level: {job_preferences.get('experience_level', 'any')}
            
            Generate:
            1. Top 5 most suitable job titles for this candidate
            2. Top 3 search queries for government jobs (if applicable)
            3. Top 3 search queries for company/private jobs
            4. Recommended companies or sectors
            
            Format as JSON:
            {{
                "suitable_job_titles": ["title1", "title2", ...],
                "government_queries": ["query1", "query2", "query3"],
                "company_queries": ["query1", "query2", "query3"],
                "recommended_sectors": ["sector1", "sector2", ...]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert career counselor and job matching specialist. Provide accurate job matching advice in JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            ai_response = response.choices[0].message.content
            
            # Extract JSON from response
            try:
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = ai_response[json_start:json_end]
                    matching_results = json.loads(json_str)
                    return matching_results
                else:
                    raise ValueError("No JSON found in response")
            except Exception as json_error:
                print(f"JSON parsing error: {json_error}")
                print("Returning empty results - OpenAI API required for data")
                return {
                    "suitable_job_titles": [],
                    "government_queries": [],
                    "company_queries": [],
                    "recommended_sectors": []
                }
            
        except Exception as e:
            print(f"Error in AI job matching: {e}")
            print("Returning empty results - OpenAI API required for data")
            return {
                "suitable_job_titles": [],
                "government_queries": [],
                "company_queries": [],
                "recommended_sectors": []
            }
    
    def generate_chatbot_response(self, user_message, cv_data=None, conversation_history=None):
        """
        AI Job Assistant Mode - Uses OpenAI API ONLY for intelligent responses
        """
        if not self.client:
            return "OpenAI API is not available. Please check your API key configuration."

        try:
            # Build CV context for system prompt
            cv_context = ""
            if cv_data:
                cv_context = f"""
The user has uploaded their CV with the following profile:
- Skills: {cv_data.get('skills', 'Not specified')}
- Experience: {cv_data.get('experience_years', '0')} years
- Education: {cv_data.get('education', 'Not specified')}
- Job Titles: {cv_data.get('job_titles', 'Not specified')}

Use this information to provide personalized job search advice.
"""

            # Build conversation messages
            messages = [
                {
                    "role": "system",
                    "content": f"""You are an AI Job Assistant specialized in helping users with job search, CV improvement, interview preparation, and career advice. {cv_context}
Provide helpful, actionable advice in a friendly and professional tone. Keep responses concise and well-formatted."""
                }
            ]

            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-6:]:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })

            # Add current message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"OpenAI API error in job assistant mode: {e}")
            return "I'm having trouble connecting to the AI service. Please try again later."
    
    def generate_general_chat_response(self, user_message, conversation_history=None):
        """
        AI Chat Mode - Uses OpenAI API ONLY for intelligent conversation
        """
        if not self.client:
            return "OpenAI API is not available. Please check your API key configuration."

        try:
            # Build conversation messages for API
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful, friendly, and knowledgeable AI assistant. You engage in natural conversations, answer questions accurately, explain concepts clearly, help with creative tasks, and provide useful information. You are conversational and warm in your tone, like ChatGPT. Keep responses concise but informative."
                }
            ]

            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-6:]:  # Last 6 messages for context
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })

            # Add current message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using GPT-3.5 for chat (faster and cheaper)
                messages=messages,
                temperature=0.7,  # More creative/conversational
                max_tokens=500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"OpenAI API error in chat mode: {e}")
            return "I'm having trouble connecting to the AI service. Please try again later."

    def generate_job_listings(self, filters):
        """
        Generate realistic job listings using OpenAI API based on search filters
        Args:
            filters: Dict with country, job_title, experience_level, company, etc.
        Returns:
            List of job dictionaries with realistic data
        """
        if not self.client:
            print("OpenAI client not available, returning no company jobs")
            return []

        try:
            # Build prompt based on filters
            country = filters.get('country', 'Global')
            job_title = filters.get('job_title', 'Software Engineer')
            experience = filters.get('experience_level', 'Mid Level')
            company = filters.get('company', 'Top Tech Companies')
            state = filters.get('state', '')

            # Map experience level to years
            exp_years_map = {
                'fresher': '0-1 years',
                'entry': '0-2 years',
                'mid': '2-5 years',
                'senior': '5-10 years',
                'lead': '10+ years'
            }
            exp_years = exp_years_map.get(experience, '2-5 years')

            location_str = f"{state}, {country}" if state else country

            # List of ONLY reputed, established companies
            reputed_companies = [
                'Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 'Netflix', 'Tesla', 'IBM', 'Oracle', 'Salesforce',
                'Adobe', 'Intel', 'Nvidia', 'Cisco', 'Dell', 'HP', 'VMware', 'Qualcomm', 'PayPal', 'eBay',
                'Accenture', 'Deloitte', 'PwC', 'EY', 'KPMG', 'McKinsey', 'BCG', 'Bain', 'Capgemini', 'Cognizant',
                'TCS', 'Infosys', 'Wipro', 'HCL', 'Tech Mahindra', 'L&T Infotech',
                'JPMorgan', 'Goldman Sachs', 'Morgan Stanley', 'Citibank', 'Bank of America', 'HSBC', 'Barclays',
                'ICICI Bank', 'HDFC Bank', 'Axis Bank', 'SBI',
                'Walmart', 'Target', 'Flipkart', 'Alibaba',
                'Verizon', 'AT&T', 'Vodafone', 'Airtel', 'Reliance Jio',
                'Ford', 'Toyota', 'BMW', 'Mercedes', 'Tata Motors',
                'Pfizer', 'Johnson & Johnson', 'AstraZeneca', 'Sun Pharma',
                'P&G', 'Unilever', 'Nestle', 'Coca-Cola', 'PepsiCo', 'HUL',
                'Shell', 'BP', 'ExxonMobil', 'Reliance Industries',
                'Boeing', 'Airbus', 'Lockheed Martin',
                'Disney', 'Warner Bros', 'Sony',
                'Samsung', 'LG', 'Siemens', 'Philips', 'GE', 'Bosch', 'Honeywell'
            ]

            companies_list = ', '.join(reputed_companies[:30])

            prompt = f"""Generate 7-8 job listings: {job_title} in {location_str}, {experience} level.
{f'Company: ONLY {company}' if company else f'Companies: ONLY use these reputed companies: {companies_list}'}

CRITICAL: Use ONLY well-known, established companies. NO startups, NO small companies.

JSON format:
[{{"title":"job","company":"name","location":"city,state,country","experience_required":"X-Y years","qualification":"degree","salary_range":"Rs X-Y LPA","responsibilities":["r1","r2","r3","r4","r5"],"qualifications":["q1","q2","q3","q4","q5"]}}]

Generate 7-8 jobs from REPUTED companies only. ONLY JSON."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Generate job listings ONLY from well-known, reputed, established companies. NO startups or small companies."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )

            # Parse response
            content = response.choices[0].message.content.strip()

            # Extract JSON from response (in case there's extra text)
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                jobs_data = json.loads(json_str)

                # Add REAL, WORKING application links - NO fake company websites
                enhanced_jobs = []
                for job in jobs_data:
                    company_name = job.get('company', 'Company')
                    job_title_for_search = job.get('title', '').replace(' ', '+')
                    location = job.get('location', '')
                    is_india = 'India' in location

                    # LinkedIn - REAL search URL (always works)
                    job['linkedin_link'] = f"https://www.linkedin.com/jobs/search/?keywords={company_name}+{job_title_for_search}"

                    # Indeed - REAL search URL (works globally, use .in for India)
                    if is_india:
                        job['indeed_link'] = f"https://in.indeed.com/jobs?q={company_name}+{job_title_for_search}"
                    else:
                        job['indeed_link'] = f"https://www.indeed.com/jobs?q={company_name}+{job_title_for_search}"

                    # Glassdoor - REAL search URL (works globally, use .co.in for India)
                    company_for_glassdoor = company_name.replace(' ', '-').lower()
                    if is_india:
                        job['glassdoor_link'] = f"https://www.glassdoor.co.in/Job/{company_for_glassdoor}-jobs-SRCH_KO0,{len(company_name)}.htm"
                    else:
                        job['glassdoor_link'] = f"https://www.glassdoor.com/Job/{company_for_glassdoor}-jobs-SRCH_KO0,{len(company_name)}.htm"

                    # Naukri - REAL search URL (only for Indian jobs)
                    if is_india:
                        job['naukri_link'] = f"https://www.naukri.com/{company_name.lower().replace(' ', '-')}-jobs"
                    else:
                        job['naukri_link'] = None

                    # Company Website - Set to None (we don't have real career page URLs)
                    job['company_website'] = None

                    enhanced_jobs.append(job)

                print(f"[OK] Generated {len(enhanced_jobs)} jobs using OpenAI API")
                return enhanced_jobs
            else:
                print("[ERROR] No valid JSON found in API response")
                return []

        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parsing error: {e}")
            print(f"Response content: {content[:500] if 'content' in locals() else 'N/A'}")
            print("Returning no jobs due to OpenAI error")
            return []
        except Exception as e:
            print(f"[ERROR] Error generating jobs with OpenAI: {e}")
            print("Returning no jobs due to OpenAI error")
            return []

    def generate_government_jobs(self, filters):
        """
        Generate realistic GOVERNMENT job listings using OpenAI API
        Args:
            filters: Dict with country, job_title, state
        Returns:
            List of government job dictionaries
        """
        if not self.client:
            print("OpenAI client not available, returning no government jobs")
            return []

        try:
            country = filters.get('country', 'United Kingdom')
            job_title = filters.get('job_title', 'Civil Service')
            state = filters.get('state', '')

            location_str = f"{state}, {country}" if state else country

            prompt = f"""Generate 5-10 realistic GOVERNMENT job listings for the following criteria:
- Job Title/Department: {job_title}
- Country: {country}
- Location: {location_str}

IMPORTANT: These must be GOVERNMENT/PUBLIC SECTOR jobs only from official government departments, agencies, or public services.

For each government job, provide:
1. Exact job title (government position)
2. Government organization/department name (e.g., "UK Civil Service", "US Department of Defense", "NHS", "Indian Railways")
3. Specific location (city, state/province, country)
4. Qualification needed
5. Salary range (use appropriate currency for country)
6. Posted date (use "Posted X days ago" format)
7. 5 key requirements

Return ONLY valid JSON array format:
[
  {{
    "title": "Administrative Officer",
    "organization": "UK Civil Service",
    "location": "London, United Kingdom",
    "qualification": "Bachelor's Degree in any discipline",
    "salary": "£25,000 - £35,000 per annum",
    "posted_date": "Posted 2 days ago",
    "description": "Join the UK Civil Service as an Administrative Officer...",
    "requirements": ["Req 1", "Req 2", "Req 3", "Req 4", "Req 5"],
    "official_link": "https://www.civilservicejobs.service.gov.uk/"
  }}
]

Use REAL government organizations for {country}. Examples:
- UK: Civil Service, NHS, HMRC, Home Office
- USA: Federal Agencies, USAJOBS, State Departments
- India: NCS, UPSC, SSC, Indian Railways, IBPS

Generate realistic, diverse government jobs. No explanation, ONLY JSON array."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a government job data generator that creates realistic official government job listings in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )

            content = response.choices[0].message.content.strip()

            # Extract JSON
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                jobs_data = json.loads(json_str)

                print(f"[OK] Generated {len(jobs_data)} government jobs using OpenAI API")
                return jobs_data
            else:
                print("[ERROR] No valid JSON found in government jobs API response")
                return []

        except Exception as e:
            print(f"[ERROR] Error generating government jobs with OpenAI: {e}")
            print("Returning no jobs due to OpenAI error")
            return []

