from django.db import models
from datetime import datetime

class CVUpload(models.Model):
    """Model for storing CV upload information"""
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    skills_extracted = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"
    
    class Meta:
        ordering = ['-uploaded_at']
