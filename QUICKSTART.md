# JobMatchAI - Quick Start Guide

## 🚀 Fastest Way to Get Started

### Prerequisites
- Python 3.10+
- MongoDB installed

### Quick Setup (5 Steps)

1. **Extract the ZIP file**
   ```
   Extract JobMatchAI.zip to your desired location
   ```

2. **Open in VS Code**
   ```
   File -> Open Folder -> Select JobMatchAI folder
   Open Terminal (Ctrl + `)
   ```

3. **Install & Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py migrate
   ```

4. **Start MongoDB** (in a SEPARATE terminal)
   ```bash
   # Windows:
   mongod --dbpath="C:\data\db"
   
   # Mac/Linux:
   mongod --dbpath=/data/db
   ```

5. **Run the Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the App**
   ```
   Open browser: http://127.0.0.1:8000/
   ```

## 🎯 Core Features

1. **Upload CV**: Upload PDF/DOCX resume
2. **AI Analysis**: Automatic skill extraction using OpenAI GPT-4
3. **Job Matching**: Get verified job listings from:
   - LinkedIn
   - Indeed
   - Glassdoor
   - Government portals
4. **AI Chatbot**: Ask career questions and get personalized advice

## 🔑 Important Files

- `.env` - Contains your OpenAI API key (already configured)
- `SETUP_GUIDE.txt` - Detailed setup instructions
- `README.md` - Full project documentation

## 📁 Project Structure

```
JobMatchAI/
├── core/               # Main application code
│   ├── views.py        # Main logic
│   ├── models.py       # Database models
│   ├── forms.py        # Form definitions
│   └── utils/          # AI & parsing utilities
├── templates/          # HTML templates
├── static/             # CSS & JavaScript
├── media/              # Uploaded CVs
└── manage.py           # Django management
```

## ⚡ VS Code Terminal Commands

All commands to run in VS Code terminal after activating virtual environment:

```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Access admin panel
http://127.0.0.1:8000/admin/

# Stop server
Ctrl + C
```

## 🔧 Troubleshooting

**MongoDB not connecting?**
- Ensure MongoDB is running in separate terminal
- Check port 27017 is not blocked

**OpenAI API errors?**
- Verify API key in `.env` file
- Check API key has available credits

**Module not found?**
- Activate virtual environment first
- Run: `pip install -r requirements.txt`

## 📞 Need Help?

See `SETUP_GUIDE.txt` for detailed troubleshooting and full documentation.

## 🎉 You're Ready!

Your JobMatchAI application is fully configured with:
✅ OpenAI API integration
✅ MongoDB database setup
✅ Responsive mobile-friendly design
✅ CV parsing with AI
✅ Job matching from verified sources
✅ Interactive chatbot

Enjoy finding your perfect job with AI! 🚀
