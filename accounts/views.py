from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(requests):
    if requests.method=="POST":
        username = requests.POST.get("username")
        password = requests.POST.get("password")
        # print(username, password)
        user = authenticate(requests, username=username, password=password)
        if user is None:
            context = {"error": "Invalid username or password"}    
            return render(requests, "accounts/login.html", context=context)
        # print(user)
        login(requests, user)
        return redirect('/')
    return render(requests, "accounts/login.html", {})

def logout_view(requests):
    context = {}
    if requests.method=="POST":
        logout(requests)
        return redirect('/login/')
    return render(requests, "accounts/logout.html", context=context)

def register_view(requests):
    context = {}
    return render(requests, "accounts/register.html", context=context)