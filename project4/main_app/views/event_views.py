from django.shortcuts import render
from django.urls import reverse
from ..models import Event
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.http import JsonResponse


def event_list_calender(request):
    events = Event.objects.all()
    data = []
    for event in events:
        data.append({
            "title": event.title,
            "start": event.date.isoformat(),
            "url" : f"/events/{event.id}",
        })
    return JsonResponse(data, safe=False)

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})



# display event details 
def event_detail(request , pk):
    event = Event.objects.get(id= pk)
    return render(request , 'events/event_detail.html' , {'event' : event})


# Create Event 
class EventCreate(CreateView):
    model = Event 
    fields = ['title' , 'description' , 'date' , 'location' , 'is_virtual' , 'link' , 'created_by']
    template_name = 'events/event_form.html' 
    success_url='/calendar/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# Edit Event 
class EventEdit(UpdateView):
    model = Event
    fields = ['description' , 'date' , 'location' , 'is_virtual' , 'link' ]
    template_name = 'events/event_form.html' 
    
    def get_success_url(self):
        return reverse('event_detail', args=[self.object.pk])


# Delete Event 
class EventDelete(DeleteView):
    model = Event
    success_url='/calendar/'
    template_name = 'events/event_confirm_delete.html' 