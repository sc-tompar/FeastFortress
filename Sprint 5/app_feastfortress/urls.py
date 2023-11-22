from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_page, name='login_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('register/', views.register_page, name='register_page'),
    path('home/', views.home_page, name='home_page'),
    path('forum/', views.forum_page, name='forum_page'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('submitContact/', views.submit_contact, name='submit_contact'),
    path('logout/', views.logout_view, name='logout_view'),
]
