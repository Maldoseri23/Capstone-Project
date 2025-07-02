from django.urls import path
from main_app.views import pages_views as views
from main_app.views.NameGame_views import name_game_view
from main_app.views.quiz_views import quiz_view, quiz_submit




urlpatterns = [
        path('', views.home, name='home'),
        path('calendar/', views.calendar, name='calendar'),
        path('sign-to-text/', views.sign_to_text_view, name='sign_to_text'),
        path('name-game/', name_game_view, name='name-game'),
        path('quiz/', quiz_view, name='quiz'),
        path('quiz/submit/', quiz_submit, name='quiz_submit'),
       
        
]

