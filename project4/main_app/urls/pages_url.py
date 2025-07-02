from django.urls import path
from main_app.views import pages_views as views
from main_app.views.NameGame_views import name_game_view





urlpatterns = [
        path('', views.home, name='home'),
        path('calendar/', views.calendar, name='calendar'),
        path('sign-to-text/', views.sign_to_text_view, name='sign_to_text'),
        path('name-game/', name_game_view, name='name-game'),

       
        
]

