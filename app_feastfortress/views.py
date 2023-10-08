from django.shortcuts import render

def landing_page(request):
    return render(request, 'app_feastfortress/landingpage.html')

def login_page(request):
    return render(request, 'app_feastfortress/login.html')

def profile_page(request):
    return render(request, 'app_feastfortress/profile.html')

def register_page(request):
    return render(request, 'app_feastfortress/register.html')
