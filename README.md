<<<<<<< HEAD
# JobMatchAI - AI-Powered Job Matching Platform

## Features
- CV/Resume Upload & Parsing (PDF, DOCX)
- AI-powered skill extraction
- Job matching from government and company portals
- Real-time AI chatbot with verified job links
- Mobile responsive design
- MongoDB database
- OpenAI GPT integration

## Technology Stack
- Backend: Django 5.0
- Database: MongoDB
- AI: OpenAI GPT-4
- Frontend: HTML5, CSS3, JavaScript
- CV Parsing: PyPDF2, python-docx

## Folder Structure
```
JobMatchAI/
├── manage.py
├── requirements.txt
├── .env
├── README.md
├── jobmatch/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cv_parser.py
│   │   ├── ai_matcher.py
│   │   └── job_scraper.py
│   └── migrations/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
└── templates/
    ├── base.html
    ├── home.html
    ├── upload_cv.html
    ├── job_results.html
    └── chatbot.html
```

## Setup Instructions

### 1. Install Python 3.10+
Ensure Python is installed on your system.

### 2. Install MongoDB
Download and install MongoDB Community Server from: https://www.mongodb.com/try/download/community

### 3. Create Virtual Environment
```bash
python -m venv venv
```

### 4. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables
Create `.env` file in root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

### 7. Start MongoDB
**Windows:**
```bash
mongod --dbpath="C:\data\db"
```

**Mac/Linux:**
```bash
mongod --dbpath=/data/db
```

### 8. Run Migrations
```bash
python manage.py migrate
```

### 9. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 10. Run Development Server
```bash
python manage.py runserver
```

### 11. Access Application
Open browser and navigate to: http://127.0.0.1:8000/

## Usage Guide

1. **Upload CV**: Upload your resume in PDF or DOCX format
2. **Skill Extraction**: AI automatically extracts your skills and experience
3. **Job Preferences**: Specify job type, location, and preferences
4. **View Matches**: Get verified job listings from government and company portals
5. **AI Chatbot**: Ask questions and get accurate job recommendations with verified links

## API Endpoints
- `/` - Home page
- `/upload-cv/` - CV upload interface
- `/job-results/` - Job matching results
- `/chatbot/` - AI chatbot interface
- `/api/chat/` - Chatbot API endpoint
- `/api/parse-cv/` - CV parsing endpoint

## Security Features
- Link verification system
- Only trusted job portals (Government sites, LinkedIn, Indeed, Glassdoor)
- AI response validation
- No fake or unverified links

## Support
For issues or questions, please create an issue in the repository.
=======
# JobMatchAI
AI-powered job matching platform with CV parsing, intelligent job search across 60+ verified portals, dual-mode AI chatbot, and comprehensive government &amp; company job listings. Built with Django, MongoDB, and OpenAI API.
>>>>>>> 3c429845e849d25584679ece0e69504c662baff7
