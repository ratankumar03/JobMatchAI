from django.contrib import admin
from .models import CVUpload

@admin.register(CVUpload)
class CVUploadAdmin(admin.ModelAdmin):
    list_display = ('filename', 'uploaded_at', 'experience')
    list_filter = ('uploaded_at',)
    search_fields = ('filename', 'skills_extracted')
    readonly_fields = ('uploaded_at',)
    
    fieldsets = (
        ('File Information', {
            'fields': ('filename', 'file', 'uploaded_at')
        }),
        ('Extracted Data', {
            'fields': ('skills_extracted', 'experience')
        }),
    )
