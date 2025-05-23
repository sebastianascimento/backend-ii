from django.db import models
from django.utils import timezone
from datetime import timedelta

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100, default="Anonymous")
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        """Return a string representation of the blog post."""
        return f"{self.title} by {self.author}"
    
    def is_recent(self):
        """
        Check if the blog post was published within the last 7 days.
        
        Returns:
            bool: True if the post was published within the last 7 days
        """
        seven_days_ago = timezone.now() - timedelta(days=7)
        return self.published_date >= seven_days_ago
    
    def get_short_preview(self, max_length=100):
        """
        Get a short preview of the blog post content.
        
        Args:
            max_length: Maximum length of the preview
            
        Returns:
            str: Truncated content with ellipsis if truncated
        """
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length].rstrip() + "..."