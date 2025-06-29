from ..models import Lesson
from django.shortcuts import render, get_object_or_404

def lessons_by_language(request, language_code):
    lessons = Lesson.objects.filter(language=language_code).order_by('lesson_type', 'label')
    return render(request, 'lessons/lessons_by_language.html', {'lessons': lessons, 'language_code': language_code})

def lesson_detail(request, language_code, pk):
    lesson = get_object_or_404(Lesson, pk=pk, language=language_code)
    return render(request, 'lessons/lesson_detail.html', {
        'lesson': lesson,
        'language_code': language_code
    })

