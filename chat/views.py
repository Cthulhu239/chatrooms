from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

def view(request):
    return HttpResponse("welcome to the chatapp")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error("password too short")
            return redirect('register')
        
        us = User.objects.filter(username = username).exists()
        if us:
            messages.error(request,"the user already exists")
            return redirect('register')
        
        new_user = User.objects.create_user(username = username,email = email,password = password)
        new_user.save()
        messages.success(request, "user successfully created, login now")
        return redirect('login_page')
    return render(request,'signup.html')



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username,password = password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request,"the given user does not exist, pls register")
            return redirect('register')
    return render(request,'login.html')    

@login_required
def home(request):
     if request.method == 'POST':
         room = request.POST.get('room')
         if Room.objects.filter(room_name = room).exists():
             messages.error(request,"the given room already exists")
             return redirect('home')
         else:    
             Room.objects.create(room_name = room)
         return redirect('home')
     all_rooms = Room.objects.all()
     return render(request,'home.html',{'rooms' : all_rooms})

@login_required
def chat(request,room):
    if request.method == 'POST':
        message_sent = request.POST.get('write')
        room_detail = get_object_or_404(Room, room_name=room)
        Message.objects.create(message = message_sent,author = request.user,room = room_detail)
    room_detail = get_object_or_404(Room, room_name=room)
    message_detail = Message.objects.filter(room = room_detail).order_by('timestamp')
    context = {
              'messages':message_detail,
              'room_name':room,
              }
    return render(request,'chat.html',context)

