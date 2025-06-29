from django.contrib import admin
from .models import Profile , Video , ForumPost , Event , Comment , Rating , SoundToSign , SignToText, Lesson

# Register your models here.
admin.site.register(Profile)

admin.site.register(Video)

admin.site.register(ForumPost)

admin.site.register(Event)

admin.site.register(Comment)

admin.site.register(Rating)

admin.site.register(SoundToSign)

admin.site.register(SignToText)

admin.site.register(Lesson)