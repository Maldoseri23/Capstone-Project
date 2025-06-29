from django.shortcuts import render
from ..models import Event
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.http import JsonResponse


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


# display event details 
def event_detail(request , Event_id):
    event = Event.objects.get(id=Event_id)
    return render(request , 'events/event_detail.html' , {'event' : event})


# Create Event 
class EventCreate(CreateView):
    model = Event 
    fields = ['title' , 'description' , 'date' , 'location' , 'is_virtual' , 'link' , 'created_by']
    template_name = 'events/event_form.html' 
    success_url='/events/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# Edit Event 
class EventEdit(UpdateView):
    model = Event
    fields = ['description' , 'date' , 'location' , 'is_virtual' , 'link' ]


# Delete Event 
class EventDelete(DeleteView):
    model = Event
    success_url='/events/'                       



def event_json(request):
    events = Event.objects.all()
    data = []

    for event in events:
        data.append({
            'title': event.title,
            'start': event.date.isoformat(),
            'url': f'/events/{event.id}/',
        })

    return JsonResponse(data, safe=False)