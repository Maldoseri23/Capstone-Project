from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from ..models import GameWord, Profile
import random
import json
from .garden_views import award_garden_item

@login_required
def game_home(request):
    # Get or create profile for the user
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'guessgame/guessgame.html', {
        'highscore': profile.highscore,
        'score': request.session.get('score', 0)
    })

@login_required
def get_random_word(request):
    words = list(GameWord.objects.all())
    if not words:
        return JsonResponse({'error': 'No words available'}, status=404)
    
    word = random.choice(words)
    request.session['current_word_id'] = word.id
    
    return JsonResponse({
        'word_id': word.id,
        'images': word.images,
        'length': len(word.word)
    })

@csrf_exempt
@login_required
def check_guess(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    
    try:
        data = json.loads(request.body)
        word_id = data.get('word_id')
        guess = data.get('guess', '').strip().lower()
    except:
        # Fallback to form data
        word_id = request.POST.get('word_id')
        guess = request.POST.get('guess', '').strip().lower()
    
    if not word_id or not guess:
        return JsonResponse({'error': 'Missing word_id or guess'}, status=400)
    
    word = get_object_or_404(GameWord, id=word_id)
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    score = request.session.get('score', 0)
    
    if guess == word.word.lower():
        score += 1
        request.session['score'] = score
        
        # Update streak
        profile.streak_count += 1
        
        # Update high score
        if score > profile.highscore:
            profile.highscore = score
        
        profile.save()

        # Alternate between flower and fruit based on score
        if score % 2 == 0:
            award_garden_item(profile, 'fruit')
        else:
            award_garden_item(profile, 'flower')

        return JsonResponse({
            'correct': True, 
            'score': score, 
            'highscore': profile.highscore,
            'streak': profile.streak_count
        })
    else:
        # Reset streak on wrong answer
        profile.streak_count = 0
        profile.save()
        
        return JsonResponse({
            'correct': False, 
            'score': score, 
            'highscore': profile.highscore,
            'streak': profile.streak_count
        })


@login_required
def show_answer(request):
    word_id = request.GET.get('word_id')
    if not word_id:
        return JsonResponse({'error': 'Missing word_id'}, status=400)
    
    word = get_object_or_404(GameWord, id=word_id)
    return JsonResponse({'answer': word.word})

@login_required
def reset_score(request):
    request.session['score'] = 0
    return redirect('game_home')

def leaderboard(request):
    top_profiles = Profile.objects.select_related('user').order_by('-highscore')[:10]
    return render(request, 'guessgame/leaderboard.html', {
        'top_profiles': top_profiles
    })

