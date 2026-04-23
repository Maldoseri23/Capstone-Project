from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    bio = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='main_app/static/uploads', default='')
    streak_count = models.IntegerField(default=0)
    highscore = models.PositiveIntegerField(default=0)
    garden_level = models.PositiveIntegerField(default=0)
    flowers = models.PositiveIntegerField(default=0)
    fruits = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField() 
    location = models.CharField(max_length=100)
    is_virtual = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)


    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title


class LessonComment(models.Model):
    rating = models.PositiveIntegerField(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson' , on_delete=models.CASCADE ,  related_name='comments')


class CallRoom(models.Model):
    """Model to represent a video call room"""
    room_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
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
    channel_name = models.CharField(max_length=255, null=True, blank=True)
    
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


class Lesson(models.Model):
    LESSON_TYPE_CHOICES = [
        ('letter', 'Letter'),
        ('word', 'Word'),
    ]
    LANGUAGE_CHOICES = [
        ('esl', 'English Sign Language'),
        ('asl', 'Arabic Sign Language'),
    ]
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPE_CHOICES)
    label = models.CharField(max_length=50)  
    video_url = models.CharField(max_length=200)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return f"{self.get_language_display()} {self.get_lesson_type_display()}: {self.label}"
    
class GameWord(models.Model):
    word = models.CharField(max_length=20, unique=True)
    images = models.JSONField()

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ar', 'Arabic'),
    ]
    
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
