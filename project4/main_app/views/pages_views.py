from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def calendar(request):
    return render(request, 'events/calendar.html')

def sign_to_text_view(request):
    return render(request, 'main_app/sign_to_text.html')

def Games(request):
    return render(request, 'games.html')

