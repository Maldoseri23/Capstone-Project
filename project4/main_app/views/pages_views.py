from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def sign_to_text_view(request):
    return render(request, 'sign_to_text/sign_to_text.html')



