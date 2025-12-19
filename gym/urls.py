from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='gym/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('members/', views.member_list, name='member_list'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    path('classes/', views.class_schedule, name='class_schedule'),
    path('classes/<int:pk>/', views.class_detail, name='class_detail'),
    path('classes/<int:pk>/register/', views.class_register, name='class_register'),
    path('check-in/', views.check_in, name='check_in'),
    path('profile/', views.profile, name='profile'),
    path('info/', views.gym_info, name='gym_info'),
    path('instructors/', views.instructors, name='instructors'),
]
