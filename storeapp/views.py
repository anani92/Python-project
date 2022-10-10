from django.shortcuts import render, redirect

# Create your views here.


def index(request):

    return render(request, 'store/home.html')


def login(request):
    return render(request, 'login/login.html')


def seller_signup(request):
    return render(request, 'login/seller_signup.html')
