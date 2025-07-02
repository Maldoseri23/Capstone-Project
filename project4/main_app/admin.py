from django.contrib import admin
from .models import Profile , Video , ForumPost , Event , Lesson, GameWord ,LessonComment

# Register your models here.
admin.site.register(Profile)

admin.site.register(Video)

admin.site.register(ForumPost)

admin.site.register(Event)

admin.site.register(Lesson)

admin.site.register(GameWord)

admin.site.register(LessonComment)

