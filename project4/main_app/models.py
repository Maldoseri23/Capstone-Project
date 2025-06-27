from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    bio = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='main_app/static/uploads', default='')
    streak_count = models.IntegerField()

    # Foreign Key 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # model objects
    def __str__(self):
        return self.user.username


class Video(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField(max_length=200)
    is_tutorial = models.BooleanField() 
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign Key 
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # model objects
    def __str__(self):
        return self.title  


class ForumPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign Key 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # model objects
    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField() 
    location = models.CharField(max_length=100)

    # Foreign Key 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # model objects
    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign Key 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)

    # model objects
    def __str__(self):
        return f"Comment by {self.user.username}"


class Rating(models.Model):
    score = models.IntegerField()

    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    
    comment = models.TextField(blank=True)

    # model objects
    def __str__(self):
        return f"{self.user.username} - {self.video.title} - {self.score}"


class SoundToSign(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    recognized_speech = models.CharField(max_length=255)

    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # model objects
    def __str__(self):
        return f"{self.user.username} - SoundToSign"


class SignToText(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    recognized_sign = models.CharField(max_length=255)

    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # model objects
    def __str__(self):
        return f"{self.user.username} - SignToText"

class CallRoom(models.Model):
    """Model to represent a video call room"""
    room_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    max_participants = models.IntegerField(default=4)
    
    def __str__(self):
        return f"Room: {self.name} ({self.room_id})"

class CallParticipant(models.Model):
    """Model to track participants in a call room"""
    room = models.ForeignKey(CallRoom, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['room', 'user']
    
    def __str__(self):
        return f"{self.user.username} in {self.room.name}"

class CallSession(models.Model):
    """Model to log call sessions for analytics"""
    room = models.ForeignKey(CallRoom, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    participant_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Session in {self.room.name} - {self.started_at}"