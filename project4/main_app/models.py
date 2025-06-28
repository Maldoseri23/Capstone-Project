from django.db import models
from django.contrib.auth.models import User


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
    is_virtual = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)

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
