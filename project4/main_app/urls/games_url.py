from django.urls import path
from . import views

urlpatterns = [
    path('game/', views.game_home, name='game_home'),
    path('games/get-random-word/', views.get_random_word, name='get_random_word'),
    path('games/Spelling-Game/', views.check_guess, name='check_guess'),
    path('games/Spelling-Game/show-answer/', views.show_answer, name='show_answer'),
    path('games/Spelling-Game/reset-score/', views.reset_score, name='reset_score'),
    path('games/Spelling-Game/leaderboard/', views.leaderboard, name='leaderboard'),
    path('games/name-game/', views.name_game_view, name='name_game'),
    path('games/', views.games, name='games'),

]