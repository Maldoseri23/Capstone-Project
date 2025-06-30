from django.urls import path
from main_app.views.NameGame_views import name_game_view

urlpatterns = [
    path('name-game/', name_game_view, name='name_game'),
]
