from django.urls import path
from main_app import views

urlpatterns = [
        #event
        path('events/event_list' , views.event_list , name='event_list'),
        path('events/<int:Event_id>/' , views.event_detail , name='event_detail'),
        path('events/create' , views.EventCreate.as_view() , name='EventCreate'),
        path('events/<int:pk>/update' , views.EventEdit.as_view() , name='EventEdit'),
        path('events/<int:pk>/delete' , views.EventDelete.as_view() , name='EventDelete'),
        path('events/json/', views.event_json, name='event_json'),

]
