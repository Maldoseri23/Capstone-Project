from django.urls import path
from main_app import views

urlpatterns = [
path('garden/', views.my_garden, name='my_garden'),
]
