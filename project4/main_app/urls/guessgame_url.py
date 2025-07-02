from django.urls import path
from main_app import views

urlpatterns = [
    path('game/', views.game_home, name='game_home'),
    path('game/get-word/', views.get_random_word, name='get_word'),
    path('game/check-guess/', views.check_guess, name='check_guess'),
    path('game/show-answer/', views.show_answer, name='show_answer'),
    path('game/reset/', views.reset_score, name='reset_score'),
    path('game/leaderboard/', views.leaderboard, name='leaderboard'),
]
