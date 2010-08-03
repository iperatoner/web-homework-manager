from datetime import datetime
from django.db import models


class Announcement(models.Model):
    """Model representing an announcement on the homepage."""
    
    title = models.CharField(max_length=256)
    text = models.TextField()
    date_created = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.title
