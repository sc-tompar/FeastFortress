from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import ContactSubmission, UserProfile, ForumPost

def landing_page(request):
    return render(request, 'app_feastfortress/landingpage.html')

@login_required
def home_page(request):
    forum_posts = ForumPost.objects.all().order_by('-timestamp')  
    return render(request, 'app_feastfortress/homepage.html', {'forum_posts': forum_posts, 'user': request.user})

@login_required
def forum_page(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        ForumPost.objects.create(user=request.user, content=content)
        return redirect('forum_page')  

    forum_posts = ForumPost.objects.all().order_by('-timestamp')
    return render(request, 'app_feastfortress/homepage.html', {'forum_posts': forum_posts})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id, user=request.user)  
    if request.method == 'POST':
        post.delete()
        return redirect('forum_page')  
    else:
        return HttpResponse('Invalid request method', status=405)

@login_required
def profile_page(request):
    user_email = request.user.email if request.user.is_authenticated else "Guest"

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        favorite_food = request.POST.get('favorite_food')
        favorite_restaurant = request.POST.get('favorite_restaurant')

        user_profile.favorite_food = favorite_food
        user_profile.favorite_restaurant = favorite_restaurant
        user_profile.save()

        messages.success(request, 'Preferences saved successfully!')

    return render(
        request,
        'app_feastfortress/profile.html',
        {
            'user_email': user_email,
            'user_profile': user_profile,
            'favorite_food': user_profile.favorite_food,  
            'favorite_restaurant': user_profile.favorite_restaurant,
        },
    )

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = form.data.get('email') 

        if User.objects.filter(username=email).exists():  
            messages.error(request, f'An account with the email "{email}" already exists. Please log in or use a different email address.')
            return render(request, 'app_feastfortress/register.html', {'form': form})
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = email  
            user.save()
            messages.success(request, f'Account created for {email}!')
            return redirect('login_page')  
    else:
        form = RegisterForm()

    return render(request, 'app_feastfortress/register.html', {'form': form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password') 

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('home_page')
            else:
                return JsonResponse({'error_message': 'Your account is disabled.'})
        else:
            return JsonResponse({'error_message': 'Invalid email or password'})

    return render(request, 'app_feastfortress/login.html')

@login_required
def submit_contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        submission = ContactSubmission(name=name, email=email, message=message)
        submission.save()

        return HttpResponse('Thanks for submitting your contact request!')
    else:
        return HttpResponseRedirect('/')
    

def logout_view(request):
    auth_logout(request)  
    return redirect('login_page')  