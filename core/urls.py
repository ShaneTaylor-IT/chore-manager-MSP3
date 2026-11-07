from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('members/', views.members, name='members'),
    path('chores/', views.chores, name='chores'),
    path('add_chore/', views.add_chore, name='add_chore'),
    path('edit_chore/<int:chore_id>/', views.edit_chore, name='edit_chore'),
]

