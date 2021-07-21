from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from  .models import ProfileModel, Room, Message, Group, GroupMessages, AddMembers
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
    room_details = Room.objects.get(id=ro).name
    return redirect('/room/'+room_details)


def group(request):
    group_details ="group detail"
    am = AddMembers.objects.filter(member=str(request.user))
    group = []
    for x in am:
        group.append(Group.objects.get(id=int(x.group_id)))
    if group:
        return render(request, 'group.html', {'group_details': group_details,'group_info':group})
    else:
        return render(request,'group.html',{'group_details':group_details,'mess':"no groups available"})


def create_group(request):
    create_group = "create_group"
    if request.method == "POST":
        group_name = request.POST['group_name']
        if Group.objects.filter(name=group_name).exists():
            mess = "This group name is already available"
            return render(request, 'group.html', {'create_group': create_group,'mess':mess})
        else:
            new_group = Group.objects.create(name=group_name,users=str(request.user))
            new_group.save()
            member = str(request.user)
            group_id = new_group.id
            am = AddMembers.objects.create(member=member,group_id=group_id)
            am.save()
            return redirect('/group1/' + group_name)
    return render(request, 'group.html', {'create_group': create_group})


def search_group(request):
    search_group = "search_group"
    if request.method == "POST":
        search = request.POST['search']
        if search:
            match = Group.objects.filter(name=search).exists()
            if match:
                match1 = Group.objects.get(name=search)
                data = AddMembers.objects.filter(group_id=match1.id,member=str(request.user))
                if data:
                    name = Group.objects.get(name=search)
                    ss = "You are alredy joined this group"
                    return render(request, "group.html", {"data": name, "search": search,'search_group': search_group,"ss":ss})
                else:
                    name = Group.objects.get(name=search)
                    ss = "You are not in the group." \
                         " You want to join the group?"
                    return render(request, "group.html", {"data": 'join', "search": search,'search_group': search_group,"ss":ss,"name":name})
            else:
                mess =  "search not found"
                return render(request, "group.html", { "search": search,'search_group': search_group,'mess':mess})
    return render(request, 'group.html', {'search_group': search_group})


def group1(request,group_name):
    username = request.user
    group_details = Group.objects.get(name=group_name).id
    mess = GroupMessages.objects.filter(group=group_details)
    group_details = Group.objects.get(name=group_name)
    return render(request, 'visit_group.html',
                  {'username': str(username), 'group': group_name, 'group_details': group_details, 'mess': mess})


def send1(request):
    message = request.POST['message']
    username = request.POST['username']
    group_id = request.POST['group_id']
    group = request.POST['group']
    new_message = GroupMessages.objects.create(message=message, user=username, group=group_id)
    new_message.save()
    return redirect('/group1/' + group)


def delete_group(request,id,gr):
    z = id+gr
    res_first = z[0:len(z) // 2]
    res_second = z[len(z) // 2 if len(z) % 2 == 0
                          else ((len(z) // 2) + 1):]
    GroupMessages.objects.get(id=res_first).delete()

    group_details = Group.objects.get(id=res_second).name
    return redirect('/group1/'+group_details)

def add_member(request,group):
    if request.method == "POST":
        search = request.POST['search']
        if search:
            match = User.objects.filter(username=search).exists()
            if match:
                gd = Group.objects.get(name=group).id
                m = AddMembers.objects.filter(member=search, group_id=gd).exists()
                if m:
                    mess = "user alredy in this group"
                    return render(request, "add_member.html", {"group_name": group, 'mess': mess})
                else:
                    AddMembers.objects.create(member=search,group_id=gd).save()
                    mess = "successfully added"
                    return render(request, "add_member.html", {"group_name":group,'mess': mess})
            else:
                mess = "user not found"
                return render(request, "add_member.html", {"group_name":group,'mess': mess})

    return render(request,"add_member.html",{"group_name":group})


def group_members(request,group):
    id1 = Group.objects.get(name=group).id
    data = AddMembers.objects.filter(group_id=id1)
    return render(request,'group_members.html',{'data':data})


def leave_group(request,group):
    id1 = Group.objects.get(name=group).id
    data = AddMembers.objects.get(group_id=id1,member=str(request.user)).delete()
    return redirect('group')


def join_group(request):
    group = request.POST['group']
    id = Group.objects.get(name=group).id
    AddMembers.objects.create(member=str(request.user),group_id=id).save()
    return redirect('/group1/' + group)