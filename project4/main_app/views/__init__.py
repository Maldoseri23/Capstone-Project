from .event_views import event_list , event_detail , EventCreate , EventEdit , EventDelete ,event_list_calender
from .usercalls_views import signup, create_room, join_room, call_room, list_rooms, deactivate_room
from .pages_views import home , calendar
from .lessons_views import lessons_by_language, lesson_detail, complete_lesson , edit_comment , delete_comment
from .guessgame_views import game_home, get_random_word, check_guess, show_answer, reset_score, leaderboard
from .garden_views import my_garden, award_garden_item
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Profile

@login_required
def profile_page(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile/profile_page.html', {'profile': profile})