# helpdesk/urls.py (update this file)
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import create_ticket
from .views import user_dashboard
from .views import admin_dashboard

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='helpdesk/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('create-ticket/', create_ticket, name='create_ticket'),
     path('dashboard/', user_dashboard, name='ticket_list'),
     path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]
