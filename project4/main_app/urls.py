from django.urls import path
from . import views





urlpatterns = [
        path('', views.home, name='home'),
        path('create-room/', views.create_room, name='create_room'),
        path('join-room/<uuid:room_id>/', views.join_room, name='join_room'),
        path('call-room/<uuid:room_id>/', views.call_room, name='call_room'),
        path('rooms/', views.list_rooms, name='list_rooms'),
        path('deactivate-room/<uuid:room_id>/', views.deactivate_room, name='deactivate_room'),
]
