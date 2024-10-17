from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def hello_world(request):
    return HttpResponse("Hello, world!")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
                
        user = authenticate(request, username=username, password=password)
        
        if user is not None:            
            login(request, user)
            return HttpResponse("Login successful!")
        else:
            return HttpResponse("Invalid credentials. Please try again.")
    
    return render(request, 'Loginify/login.html')