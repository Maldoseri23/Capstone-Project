from django.urls import path
from main_app import views

urlpatterns = [
    path('lessons/<str:language_code>/', views.lessons_by_language, name='lessons_by_language'),
    path('lessons/<str:language_code>/<int:pk>/', views.lesson_detail, name='lesson_detail')
]
