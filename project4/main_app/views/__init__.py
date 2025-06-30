from .event_views import event_list , event_detail , EventCreate , EventEdit , EventDelete , event_json
from .usercalls_views import signup, create_room, join_room, call_room, list_rooms, deactivate_room
from .pages_views import home , calendar
from .lessons_views import lessons_by_language, lesson_detail, complete_lesson
from .guessgame_views import game_home, get_random_word, check_guess, show_answer, reset_score, leaderboard
from .garden_views import my_garden, award_garden_item