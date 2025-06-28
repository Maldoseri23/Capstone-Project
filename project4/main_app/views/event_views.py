from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from ..models import Event 
from django.views.generic.edit import CreateView , UpdateView , DeleteView


# Event Controllers 
# NEW THING I HAVE LEARNED : the difference between def , class - def: for Simple pages m easier to control - class : for CRUD , for complex apps.

# List of event 
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


# display event details 
def event_detail(request , event_id):
    event = Event.objects.get(id=event_id)
    return render(request , 'events/event_detail.html' , {'event' : event})


# Create Event 
class EventCreate(CreateView):
    model = Event 
    fields = ['title' , 'description' , 'date' , 'location' , 'is_virtual' , 'link' ]
    success_url='/events/'


# Edit Event 
class EventEdit(UpdateView):
    model = Event
    fields = ['description' , 'date' , ' location' , 'is_virtual' , 'link' ]


# Delete Event 
class EventDelete(DeleteView):
    model = Event
    success_url='/events/'


#calendar 
def event_json(request):
    events = Event.objects.all()
    data = []
    for event in events:
        data.append({
            "id": event.id,
            "title": event.title,
            "start": event.date.isoformat(),
        })
    return JsonResponse(data, safe=False)

def calendar_view(request):
    return render(request, 'events/calendar.html')

