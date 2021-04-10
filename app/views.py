from django.shortcuts import render, redirect
from .models import User, Message, Group
from . import models
from django.contrib import messages

def index(request):
    return render(request,"home.html")

def login_page(request):
    return render(request,"login.html")

def registration_page(request):
    return render(request,"registration.html")

def register(request):
    if request.POST['sign'] == 'register':
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'],password=request.POST['password'])
        print("id is :", user.id)
    return render(request, 'registration.html')

def login(request):
    if request.POST['sign'] == 'login':
        try:
            matching_user = User.objects.filter(email=request.POST['email'], password=request.POST['password'])
            current_user = matching_user.first()
            print("String is ", matching_user.count())
            print("id is ", current_user.id)

            if matching_user.count() != 0:
                request.session['login_user'] = current_user.id
                print("id --->",request.session['login_user'])
                request.session['name'] = current_user.first_name + " " + current_user.last_name
                request.session.save()
                return render(request, 'dashboard.html')
        except:
            print("Email or password is wrong!")

    return render(request, 'login.html')

def logout(request):
    del request.session['login_user']
    del request.session['name']
    return render(request, "login.html")

def editAccount(request):
    user = User.objects.get(id = request.session['login_user'])
    context = {
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "email" : user.email,
    }   
    return render(request, "edit_account.html", context)  

def dashboard(request):
    return render(request, 'dashboard.html')

def add_msg(request, group_id):
    print("message views")
    if request.method =='POST':
        errors = models.msg_errors(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            msg = models.addMessage(request.POST,request.session['login_user'], group_id)
            print("message views")
            if msg is not None:
                return redirect('/dashboard')
    return redirect('/dashboard')

##############################################################################################################

def groupDashboard(request):
    context = {
        'groups':models.all_groups_for_user(request.session['login_user']),
        'otherGroups':models.other_groups(request.session['login_user']),
        #'users':models.all_users(),
    }
    return render(request,"groupDashboard.html", context)

def addGroup(request):
    if request.method =='POST':
        models.addGroup(request.POST,request.session['login_user'])
        return redirect('/groups')
    return render(request,"addGroup.html")

def joinGroup(request,group_id):
    models.join(request.session['login_user'], group_id)
    return redirect('/groups')

def view_group_name(request,group_id):
    current_group = models.selected_group(group_id)
    context = {
        'group_name': current_group.group_name,
        'group_id': current_group.id,
        'planner': current_group.planner.first_name,
        'plannerId': current_group.planner.id,
        'description': current_group.description,
        'groupUsers': models.users_joining_the_group(request.session['login_user'],group_id)

    }

    return render(request,"group.html",context)
