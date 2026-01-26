from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.view),
    path('signup', views.signup,name = "register"),
    path('login',views.login,name = "login_page"),
    path('home',views.home,name = 'home'),
    path('<str:room>/', views.chat, name='room'),
]