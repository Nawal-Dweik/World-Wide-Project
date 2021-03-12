from django.shortcuts import render, redirect
from .models import User, Message

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

def send_msg(request):
    return render(request, 'dashboard.html')
