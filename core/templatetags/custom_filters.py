from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def time_ago(value):
    """Convert datetime to 'X days/weeks/months ago' format"""
    if not value:
        return "Recently"
    
    try:
        if isinstance(value, str):
            date = datetime.fromisoformat(value.replace('Z', '+00:00'))
        else:
            date = value
        
        now = datetime.now()
        if date.tzinfo:
            from django.utils import timezone
            now = timezone.now()
        
        diff = now - date
        
        if diff.days == 0:
            return "Today"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif diff.days < 365:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
    except:
        return "Recently"