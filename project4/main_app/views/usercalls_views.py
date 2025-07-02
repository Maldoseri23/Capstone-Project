from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from ..models import CallRoom, CallParticipant
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

# help from: https://www.videosdk.live/developer-hub/webrtc/django-webrtc

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Define form inside POST block
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    else:  # Handle GET requests separately
        form = UserCreationForm()  # Define form for non-POST requests
    
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name', f"{request.user.username}'s Room")
        max_participants = int(request.POST.get('max_participants', 4))
        
        room = CallRoom.objects.create(
            name=room_name,
            created_by=request.user,
            max_participants=max_participants
        )
        
        messages.success(request, f'Room "{room_name}" created successfully!')
        return redirect('call_room', room_id=room.room_id)
    
    return render(request, 'main_app/create_room.html')

@login_required
def join_room(request, room_id):
    room = get_object_or_404(CallRoom, room_id=room_id, is_active=True)
    
    # Check if room is full
    current_participants = CallParticipant.objects.filter(
        room=room, 
        is_online=True
    ).count()
    
    if current_participants >= room.max_participants:
        messages.error(request, 'This room is full!')
        return redirect('list_rooms')
    
    return redirect('call_room', room_id=room_id)

@login_required
def call_room(request, room_id):
    room = get_object_or_404(CallRoom, room_id=room_id, is_active=True)
    
    # Ensure the user is added as a participant
    participant, created = CallParticipant.objects.get_or_create(
        room=room,
        user=request.user,
        defaults={'is_online': True}
    )
    if not created and not participant.is_online:
        participant.is_online = True
        participant.save()
    
    # Get current participants
    participants = CallParticipant.objects.filter(
        room=room, 
        is_online=True
    ).select_related('user')
    
    context = {
        'room': room,
        'participants': participants,
        'room_id_str': str(room.room_id),
        'user_id': request.user.id,
        'username': request.user.username,
        'user': request.user,  # for template comparison
    }
    
    return render(request, 'main_app/call_room.html', context)


@login_required
def list_rooms(request):
    active_rooms = CallRoom.objects.filter(is_active=True).order_by('-created_at')
    
    # Add participant count to each room
    for room in active_rooms:
        room.current_participants = CallParticipant.objects.filter(
            room=room, 
            is_online=True
        ).count()
    
    context = {
        'rooms': active_rooms
    }
    
    return render(request, 'main_app/list_rooms.html', context)

@login_required
def deactivate_room(request, room_id):
    room = get_object_or_404(CallRoom, room_id=room_id)
    if request.user == room.created_by:  # Only creator can deactivate
        room.is_active = False
        room.save()
        messages.success(request, "Room has been deactivated.")
    else:
        messages.error(request, "Only the room creator can deactivate this room.")
    return redirect('list_rooms')
