from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Lesson, Profile, LessonComment
from .garden_views import award_garden_item


def lessons_by_language(request, language_code):
    lessons = Lesson.objects.filter(language=language_code).order_by('lesson_type', 'label')
    return render(request, 'lessons/lessons_by_language.html', {
        'lessons': lessons,
        'language_code': language_code
    })


def lesson_detail(request, language_code, pk):
    lesson = get_object_or_404(Lesson, pk=pk, language=language_code)

    # FIX #3: only allow logged-in users to submit comments
    if request.method == 'POST' and 'submit_comment' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        LessonComment.objects.create(
            lesson=lesson,
            user=request.user,
            rating=rating,
            comment=comment
        )
        return redirect('lesson_detail', language_code=language_code, pk=pk)

    comments = LessonComment.objects.filter(lesson=lesson).select_related('user')

    return render(request, 'lessons/lesson_detail.html', {
        'lesson': lesson,
        'language_code': language_code,
        'comments': comments,
    })


@login_required
def complete_lesson(request, language_code, pk):
    lesson = get_object_or_404(Lesson, pk=pk, language=language_code)
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        award_garden_item(profile, 'flower')
        # FIX #2 & #5: use messages framework and redirect (PRG pattern)
        messages.success(request, "🎉 Garden updated! You earned a flower for completing the lesson.")
        return redirect('lesson_detail', language_code=language_code, pk=pk)

    return redirect('lesson_detail', language_code=language_code, pk=pk)


@login_required
def edit_comment(request, language_code, pk, comment_id):
    comment = get_object_or_404(LessonComment, id=comment_id, user=request.user)
    lesson = get_object_or_404(Lesson, pk=pk, language=language_code)

    if request.method == 'POST':
        comment.comment = request.POST.get('comment')
        comment.rating = int(request.POST.get('rating'))
        comment.save()
        return redirect('lesson_detail', language_code=language_code, pk=pk)

    return render(request, 'lessons/edit_comment.html', {
        'comment': comment,
        'lesson': lesson
    })


@login_required
def delete_comment(request, language_code, pk, comment_id):
    comment = get_object_or_404(LessonComment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('lesson_detail', language_code=language_code, pk=pk)
    # FIX #1: pass language_code and pk so the Cancel link works
    return render(request, 'lessons/delete_comment.html', {
        'comment': comment,
        'language_code': language_code,
        'pk': pk,
    })

