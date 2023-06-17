from django.shortcuts import redirect
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('add_investment/', views.add_investment, name='add_investment'),
    path('edit_investment/<int:investment_id>/', views.edit_investment, name='edit_investment'),
    path('delete_investment/<int:investment_id>/', views.delete_investment, name='delete_investment'),
    path('add_goal/', views.add_goal, name='add_goal'),
    path('edit_goal/<int:goal_id>/', views.edit_goal, name='edit_goal'),
    path('delete_goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('approach/', views.approach, name='approach'),
    path('calculator/', views.calculator, name='calculator'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', lambda request: redirect('portfolio'), name='profile'),
    path('prediction/', views.predict, name='prediction'),
    path('add-investment/', views.add_investment, name='add_investment'),
    path('accept-investment/', views.accept_investment, name='accept_investment'),
]


