import uuid
from django.db import models

class Projects(models.Model):
    PROJECTS_CHOICES = [
        ('website', 'Website'),
        ('game', 'Game'),
        ('mobile app', 'Mobile App'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=PROJECTS_CHOICES, default='other')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Academic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.CharField(max_length=255)
    period = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.institution