from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from  .models import ProfileModel, Room, Message
from .forms import SignupForm
from django.contrib.auth import logout
from django.db.models import Q

def home(request):
  return render(request, 'index.html')


def signup(request):
    a = SignupForm()
    if request.method == "POST":
        ab = SignupForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        conform_assword = request.POST['conform_assword']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is  already taken. please try another one !")
            return redirect('signup')
        if len(password) < 8:
            messages.error(request, "Password must be atleast 8 characters")
            return redirect('signup')
        if not username.isalnum():
            messages.error(request, "Username should only contain letters")
            return redirect('signup')
        if password != conform_assword:
            messages.error(request, "Password Do not Match")
            return redirect('signup')
        ab = SignupForm(request.POST)
        if ab.is_valid():
            captcha = request.POST.get("captcha")
            a= ProfileModel.objects.create(username=username)
            a.save()
            myuser = User.objects.create_user(username=username, password=password)
            myuser.save()
            messages.error(request, "Successfully registerd Your Account")
            return redirect('login')
        else:
            captcha = request.POST.get("captcha")
            return render(request, "signup.html", {"form": ab, "msg": ab.errors})
    else:
        return render(request, "signup.html", {"form": a})


def login(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
      from django.contrib.auth import login
      login(request, user)
      return redirect('/')
    else:
        message = "Invalid username or password"
        return render(request, "login.html", {"mess": message})
  return render(request, "login.html")


def logout_user(request):
  logout(request)
  return redirect('/')


def edit_profile(request):
    if request.method == "POST":
        id = request.POST['id']
        first_name = request.POST['first_name']
        email = request.POST['email']
        try:
            image = request.FILES['image']
            form = ProfileModel.objects.get(id=id)
            form.id =id
            form.name = first_name
            form.email = email
            form.profile_image = image
            form.save()
        except:
            form = ProfileModel.objects.get(id=id)
            form.id = id
            form.name = first_name
            form.email = email
            form.save()
        return redirect('profile')
    else:
        form = User.objects.get(username=request.user)
        return render(request, "edit_profile.html", {'form': form})

def profile(request):
    try:
        form = ProfileModel.objects.get(username=request.user)
        return render(request, "profile.html",{'form': form})
    except :
        form = None
        return render(request, "profile.html", {'form': form})


def visit_room(request):
    return render(request,'visit_room.html')


def room1(request,room):
    username = request.user
    room_details = Room.objects.get(name=room).id
    mess = Message.objects.filter(room=room_details)
    room_details = Room.objects.get(name=room)
    return render(request,'room.html',{'username':str(username),'room':room,'room_details':room_details,'mess':mess})


def checkview(request):
    room = request.POST['room_name']
    username = request.user
    if Room.objects.filter(name=room).exists():
        return redirect('/room1/'+room)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/room1/'+room)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    room = request.POST['room']
    new_message = Message.objects.create(value=message,user=username,room=room_id)
    new_message.save()
    return redirect('/room/'+room)


def room(request,room):
    username = request.user
    room_details = Room.objects.get(name=room).id
    mess = Message.objects.filter(room=room_details)
    room_details = Room.objects.get(name=room)
    return render(request,'room.html',{'username':str(username),'room':room,'room_details':room_details,'mess':mess})


def search(request):
    search = request.POST['search']
    if search:
        match = ProfileModel.objects.filter(Q(name__icontains=search)).filter(username__icontains=search).distinct()
        if match:
            return render(request, "search.html", {"data": match, "search": search})
        else:
            messages.success(request, "search not found")
            return render(request, "search.html", {"user": '',"search": search})


def delete(request,id,ro):
    Message.objects.get(id=id).delete()
    print(id,"""""""""""""""""",ro)
    room_details = Room.objects.get(id=ro).name
    return redirect('/room/'+room_details)