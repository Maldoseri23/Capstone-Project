from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from ..models import Lesson, Profile , LessonComment
from .garden_views import award_garden_item 
from django.views.generic.edit import UpdateView , DeleteView


def lessons_by_language(request, language_code):
    lessons = Lesson.objects.filter(language=language_code).order_by('lesson_type', 'label')
    return render(request, 'lessons/lessons_by_language.html', {'lessons': lessons, 'language_code': language_code})

def lesson_detail(request, language_code, pk):
    lesson = get_object_or_404(Lesson, pk=pk, language=language_code)

    if request.method == 'POST' and 'submit_comment' in request.POST:
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
        'comments' : comments
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


@login_required
def edit_comment(request, language_code, pk, comment_id):
    comment = get_object_or_404(LessonComment, id=comment_id, user=request.user)
    lesson = get_object_or_404(Lesson, pk=pk, language=language_code)

    if request.method == 'POST':
        comment.comment = request.POST.get('comment')
        comment.rating = int(request.POST.get('rating'))
        comment.save()
        return redirect('lesson_detail', language_code=language_code, pk=pk)

    return render(request, 'lessons/edit_comment.html', {'comment': comment, 'lesson': lesson})



@login_required
def delete_comment(request, language_code, pk, comment_id):
    comment = get_object_or_404(LessonComment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('lesson_detail', language_code=language_code, pk=pk)
    return render(request, 'lessons/delete_comment.html', {'comment': comment})