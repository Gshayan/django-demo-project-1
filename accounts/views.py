from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout


def register_view(requests):
    form = UserCreationForm(requests.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    return render(requests, "accounts/register.html", context=context)

def login_view(requests):
    if requests.method=="POST":
        form = AuthenticationForm(requests, data=requests.POST)
        if form.is_valid():
            user = form.get_user()
            login(requests, user)
            return redirect('/')
    else:
        form = AuthenticationForm(requests)
    context = {
        "form": form
    }
    return render(requests, "accounts/login.html", context=context)

def logout_view(requests):
    context = {}
    if requests.method=="POST":
        logout(requests)
        return redirect('/login/')
    return render(requests, "accounts/logout.html", context=context)
