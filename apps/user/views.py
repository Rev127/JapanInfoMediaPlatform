from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'registration/login.html')

def register_view(request):
    return render(request, 'registration/signup.html')

def profile_view(request):
    return render(request, 'user/profile.html')
