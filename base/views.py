from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from .forms import RoomForm

# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ) #atleast matches with two or more elements
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count}
    return render(request,"base/home.html", context)

def room(request, pk):
    # room = Room.objects.all
    room = Room.objects.get(id = int(pk))
    context = {'room':room}
    return render(request,"base/room.html", context)

def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST) #passing all the data to form
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {"form":form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room) # Form will be prefilled
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id = int(pk))
    if request.method == 'POST':
        room.delete()
        return redirect("home")
    return render(request, 'base/delete.html', {'obj':room})