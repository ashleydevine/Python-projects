from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'login_and_registration/index.html')

def profile(request):
    return render(request, 'login_and_registration/profile.html')

def login(request):
    valid, response = User.objects.login_validation(request.POST)

    if not valid:
        for error in response:
            messages.error(request, error)
        return redirect(reverse('login_and_registration:index'))
    else:
        messages.success(request, "Welcome Back!")
        request.session['user_id'] = response.id
        request.session['first_name'] = response.first_name
    return redirect(reverse('wish_list:index'))

def register(request):
    valid, response = User.objects.registration_validation(request.POST)

    if not valid:
        for error in response:
            messages.error(request, error)
        return redirect(reverse('login_and_registration:index'))
    else:
        messages.success(request, "Thanks for registering!")
        request.session['user_id'] = response.id
        request.session['first_name'] = response.first_name
    return redirect(reverse('wish_list:index'))

def delete(request, id):
    valid = User.objects.delete_user(id)
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
