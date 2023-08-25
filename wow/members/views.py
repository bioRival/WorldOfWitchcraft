from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import  UserCreationForm
from django.contrib import messages
from .forms import BaseRegisterForm
from django_email_verification import send_email
from django.contrib.auth.models import User
from core.models import Author


def login_user(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("Неправильный Email или Пароль. Попробуйте еще раз"))
            return redirect('login')
    else:
        return render(request, 'auth/login.html', {})


def logout_user(request):
    messages.success(request, ("Вы вышли из системы"))
    logout(request)
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = User.objects.create_user(username=username, email=email, password=password)

            Author.objects.create(user=user)

            user.is_active = False

            send_email(user)

            messages.success(request, (f"На ваш email {email} было отправлено письмо"))
            return redirect('home')
    else:
        form = BaseRegisterForm()
    return render(request, 'auth/register.html', {'form':form,})