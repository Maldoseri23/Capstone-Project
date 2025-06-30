from ..models import Lesson
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Lesson, Profile
from .garden_views import award_garden_item 

def lessons_by_language(request, language_code):
    lessons = Lesson.objects.filter(language=language_code).order_by('lesson_type', 'label')
    return render(request, 'lessons/lessons_by_language.html', {'lessons': lessons, 'language_code': language_code})

def lesson_detail(request, language_code, pk):
    lesson = get_object_or_404(Lesson, pk=pk, language=language_code)
    return render(request, 'lessons/lesson_detail.html', {
        'lesson': lesson,
        'language_code': language_code
    })

@login_required
def complete_lesson(request, language_code, pk):
    lesson = get_object_or_404(Lesson, pk=pk, language=language_code)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    message = None

    if request.method == "POST":
        # Award a flower for lesson completion
        award_garden_item(profile, 'flower')
        message = "🎉 Garden updated! You earned a flower for completing the lesson."

    # Re-render the lesson detail page with a success message
    return render(request, 'lessons/lesson_detail.html', {
        'lesson': lesson,
        'language_code': language_code,
        'message': message,
    })