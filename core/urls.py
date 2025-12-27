from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-cv/', views.upload_cv, name='upload_cv'),
    path('job-preferences/', views.job_preferences, name='job_preferences'),
    path('job-results/', views.job_results, name='job_results'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat-api/', views.chat_api, name='chat_api'),
    path('reset/', views.reset_session, name='reset_session'),

    # Government and Company Jobs
    path('government-jobs/', views.government_jobs, name='government_jobs'),
    path('company-jobs/', views.company_jobs, name='company_jobs'),

    # LinkedIn OAuth
    path('linkedin/login/', views.linkedin_login, name='linkedin_login'),
    path('linkedin/callback/', views.linkedin_callback, name='linkedin_callback'),
]