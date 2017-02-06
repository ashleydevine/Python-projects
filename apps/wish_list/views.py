from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Wish
from ..login_and_registration.models import User

def index(request):
    user_id = request.session['user_id']
    my_items = Wish.objects.my_items(user_id)
    others_items = Wish.objects.others_items(user_id)
    context = {
        'my_items':my_items,
        'others_items':others_items,
    }
    return render(request, 'wish_list/dashboard.html', context)

def create(request):
    return render(request, 'wish_list/create.html')

def process(request):
    user_id = request.session['user_id']
    valid, response = Wish.objects.create_item(request.POST, user_id)
    if not valid:
        for error in response:
            print error
            messages.error(request, error)
        return redirect(reverse('wish_list:create'))
    else:
        messages.success(request, "Item has been added!")
    return redirect(reverse('wish_list:index'))

def add_item(request, wish_id):
    user_id = request.session['user_id']
    user_items = Wish.objects.adding_item(user_id, wish_id)
    return redirect(reverse('wish_list:index'))

def delete_item(request, wish_id):
    user_id = request.session['user_id']
    item = Wish.objects.delete_item(user_id, wish_id)
    return redirect(reverse('wish_list:index'))

def remove_item(request, wish_id):
    user_id = request.session['user_id']
    item = Wish.objects.remove_item(user_id, wish_id)
    return redirect(reverse('wish_list:index'))

def wish_detail(request, wish_id):
    users = User.objects.filter(added_items__id=wish_id)
    valid, wish = Wish.objects.wish_detail(wish_id)
    if valid:
        context = {
            'users':users,
            'wish':wish,
            }
    else:
        messages.error(request, wish)
    return render(request, 'wish_list/wish_details.html', context)

def logout(request):
    return redirect(reverse('login_and_registration:index'))
