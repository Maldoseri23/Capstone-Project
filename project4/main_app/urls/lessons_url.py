from django.urls import path
from main_app import views

urlpatterns = [
    path('lessons/<str:language_code>/', views.lessons_by_language, name='lessons_by_language'),
    path('lessons/<str:language_code>/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<str:language_code>/<int:pk>/complete/', views.complete_lesson, name='complete_lesson'),
    path('lessons/<str:language_code>/<int:pk>/comment/<int:comment_id>/edit/', views.edit_comment , name='edit_comment'),
    path('lessons/<str:language_code>/<int:pk>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
