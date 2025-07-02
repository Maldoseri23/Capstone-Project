from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Profile

def award_garden_item(profile, item_type):
    if item_type == 'flower':
        profile.flowers += 1
    elif item_type == 'fruit':
        profile.fruits += 1
    # Optionally, increase garden_level based on total items
    profile.garden_level = profile.flowers + profile.fruits
    profile.save()

@login_required
def my_garden(request):
    profile = Profile.objects.get(user=request.user)
    flower_imgs = [{'left': i * 30} for i in range(profile.flowers)]
    fruit_imgs = [{'left': i * 50} for i in range(profile.fruits)]
    return render(request, 'garden/my_garden.html', {
        'profile': profile,
        'flower_imgs': flower_imgs,
        'fruit_imgs': fruit_imgs,
    })
