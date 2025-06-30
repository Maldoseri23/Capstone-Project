from django.urls import path, include

urlpatterns = [
    path('', include('main_app.urls.pages_url')),
    path('', include('main_app.urls.event_url')),
    path('', include('main_app.urls.usercalls_url')),
    path('', include('main_app.urls.lessons_url')),
    path('', include('main_app.urls.sign_to_text_url')),
    path('', include('main_app.urls.guessgame_url')),
    path('', include('main_app.urls.garden_url')),
]

