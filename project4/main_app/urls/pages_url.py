from django.urls import path
from main_app import views
from main_app.views import pages_views as views

urlpatterns = [
        path('', views.home, name='home'),
        path('calendar/', views.calendar, name='calendar'),
        path('sign-to-text/', views.sign_to_text_view, name='sign_to_text'),
        path('games/', views.Games, name='Games'),
]
