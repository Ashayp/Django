from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import UserDetails
from django.contrib.auth.hashers import make_password, check_password


def hello_world(request):
    return HttpResponse("Hello, world!")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user exists and verify the password
        try:
            user = UserDetails.objects.get(email=email)
            if check_password(password, user.password):
                return HttpResponse("Login successful!")
            else:
                return HttpResponse("Invalid credentials!")
        except UserDetails.DoesNotExist:
            return HttpResponse("User not found!")
    
    return render(request, 'loginify/login.html')


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if UserDetails.objects.filter(email=email).exists():
            return HttpResponse("Email already registered!")

        user = UserDetails(username=username, email=email, password=make_password(password))
        user.save()

        return redirect('login')
    
    return render(request, 'loginify/signup.html')