from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from .models import UserDetails
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserDetailsSerializer
from rest_framework.response import Response
import json
from django.views.decorators.csrf import csrf_exempt


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

@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        try:
            all_users = UserDetails.objects.all() # queryset
            serializer_data=UserDetailsSerializer(all_users,many=True) #data in serialized form ~= json format
            return JsonResponse(serializer_data.data,safe=False)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            },status=500)

    if request.method == "POST":
        input_data = json.loads(request.body) #json 
        serializer_data = UserDetailsSerializer(data=input_data)
        try:
            if serializer_data.is_valid():
                serializer_data.save()
                return JsonResponse({
                    "Success": True,
                    "message": "User created successfully",
                    "data": serializer_data.data
                    }, status=201)
            else:
                return JsonResponse(serializer_data.errors, status=400)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            },status=500)
            
@csrf_exempt       
def get_user_by_username(request, pk):
    if request.method == 'GET':
        try:
            user = UserDetails.objects.get(pk=pk)
            serializer_data = UserDetailsSerializer(user)
            return JsonResponse(serializer_data.data, safe=False)
        except UserDetails.DoesNotExist:
            return JsonResponse({
                "error": "User not found"
            },status=404)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            },status=500)

    if request.method == 'PUT':
        try:
            user = UserDetails.objects.get(pk=pk)
            input_data = json.loads(request.body)
            serializer_data = UserDetailsSerializer(user, data=input_data)

            if serializer_data.is_valid():
                serializer_data.save()
                return JsonResponse({
                    "Success": True,
                    "message": "User updated successfully",
                    "data": serializer_data.data
                    }, status=200)
            else:
                return JsonResponse(serializer_data.errors, status=400)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            },status=500)

    if request.method == 'PATCH':
        try:
            user = UserDetails.objects.get(pk=pk)
            input_data = json.loads(request.body)
            serializer_data = UserDetailsSerializer(user,data=input_data,partial=True)

            if serializer_data.is_valid():
                serializer_data.save()
                return JsonResponse({
                    "Success": True,
                    "message": "User updated successfully",
                    "data": serializer_data.data
                    }, status=200)
            else:
                return JsonResponse(serializer_data.errors, status=400)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            },status=500)

    if request.method == 'DELETE':
        try:
            user = UserDetails.objects.get(pk=pk)
            user.delete()
            return JsonResponse({
                "Success": True,
                "message": "User deleted successfully"
            }, status=204)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            },status=500)
    