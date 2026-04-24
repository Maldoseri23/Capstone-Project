from django.contrib import admin
from .models import Profile , Event , Lesson, GameWord ,LessonComment


admin.site.register(Profile)

admin.site.register(Event)

admin.site.register(Lesson)

admin.site.register(GameWord)

admin.site.register(LessonComment)

