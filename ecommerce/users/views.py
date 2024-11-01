from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from .models import User
from django.contrib import messages


# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('core:home')

    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, "Please enter a correct username and password.")
    else:
        messages.error(request, "Invalid username or password.")

    return render(request, 'login/login.html')


def logoutUser(request):
    logout(request)
    return redirect('users:login')