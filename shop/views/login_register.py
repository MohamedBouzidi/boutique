import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from shop.models import BusinessUser


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).count() > 0:
            username = User.objects.filter(email=email).first().username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('index'))
    return render(request, "shop/login_register_form.html")


def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=email, password=password, email=email)
                return HttpResponseRedirect(reverse_lazy('index'))
    return render(request, "shop/login_register_form.html")


def business_register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        description = request.POST['description']
        picture = request.POST['picture']
        type = request.POST['type']

        businessuser = BusinessUser(description=description, picture=picture, type=type)
        businessuser.user = request.user
        businessuser.user.username = username
        businessuser.save()
        data = {
            "message": "success"
        }
        return JsonResponse()
    else:
        return HttpResponseRedirect(reverse_lazy('index'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))