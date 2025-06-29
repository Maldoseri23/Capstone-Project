from django.urls import path, include
from main_app import views

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'), 
    path('accounts/', include('django.contrib.auth.urls')), 
    path('create-room/', views.create_room, name='create_room'),
    path('join-room/<uuid:room_id>/', views.join_room, name='join_room'),
    path('call-room/<uuid:room_id>/', views.call_room, name='call_room'),
    path('rooms/', views.list_rooms, name='list_rooms'),
    path('deactivate-room/<uuid:room_id>/', views.deactivate_room, name='deactivate_room'),
]
