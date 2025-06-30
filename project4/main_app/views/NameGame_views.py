from django.shortcuts import render

def name_game_view(request):
    return render(request, 'NameGame/NameGame.html')
