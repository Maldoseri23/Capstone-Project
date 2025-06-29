from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def calendar(request):
    return render(request, 'calendar.html')
