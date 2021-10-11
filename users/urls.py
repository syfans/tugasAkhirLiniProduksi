from django.urls import path

from . import views
app_name = 'users'

urlpatterns = [
    path('', views.registerView, name='index'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
]