from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')
    return render(request, 'main/index.html')


def dash(request):
    if 'user_id' not in request.session:
        return redirect('/')
    

    context = {
        'your_trips' : Trip.objects.filter(created_by__id=request.session['user_id']),
        'other_trips' : Trip.objects.exclude(created_by__id=request.session['user_id']),
        'unjoined_trips' : Trip.objects.exclude(created_by = User.objects.get(id = request.session['user_id'])).exclude(join = User.objects.get(id = request.session['user_id'])),
    }

    return render(request, 'main/dashboard.html', context)

def process_reg(request):
    potential_errors = User.objects.validate_user(request.POST)
    if len(potential_errors):
        for key, val in potential_errors.items():
           messages.error(request, val, extra_tags=key)
        return redirect('/')

    hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(
        first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=hash)
    request.session['user_id'] = user.id
    request.session['user'] = user.first_name
    print('success')
    print(User.objects.all().values())
    return redirect('/dashboard')


def process_log(request):
    potential_errors = User.objects.validate_user(request.POST)
    if len(potential_errors):
        for key, val in potential_errors.items():
           messages.error(request, val, extra_tags=key)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['checkemail'])
        request.session['user_id'] = user.id
        request.session['user'] = user.first_name
        return redirect('/dashboard')


def logout(request):
    request.session.clear()
    return redirect('/')

def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'main/new.html')

def process_new(request):
    if 'user_id' not in request.session:
        return redirect('/')

    potential_errors = Trip.objects.validate_trip(request.POST)
    if len(potential_errors):
        for key, val in potential_errors.items():
            messages.error(request, val, extra_tags = key)
        return redirect('/new')

    creator = User.objects.get(id=request.session['user_id'])
    Trip.objects.create(dest=request.POST['dest'], plan = request.POST['plan'], start_date=request.POST['start'], end_date = request.POST['end'], created_by=creator)

    print(Trip.objects.all().values())
    return redirect('/dashboard')

def trip(request, number):
    if 'user_id' not in request.session:
        return redirect('/')

    trip = Trip.objects.get(id=number)
    context = {
        'trip' : trip,
        'joined': trip.join.all().values()
    }
    return render(request, 'main/view.html', context)

def remove(request, number):
    if 'user_id' not in request.session:
        return redirect('/')

    d = Trip.objects.get(id=number)
    d.delete()
    return redirect('/dashboard')

def edit(request, number):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'trip' : Trip.objects.get(id=number)
    }
    
    return render(request, 'main/edit.html', context)    

def process_edit(request, number):
    if 'user_id' not in request.session:
        return redirect('/')

    potential_errors = Trip.objects.validate_trip(request.POST)
    if len(potential_errors):
        for key, val in potential_errors.items():
           messages.error(request, val)
        return redirect('/trips/edit/' +number)


    update = Trip.objects.get(id=number)
    update.dest = request.POST['dest']
    update.plan = request.POST['plan']
    update.start_date = request.POST['start']
    update.end_date = request.POST['end']
    update.save()
    return redirect('/dashboard')

def join(request, number):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.get(id=number)
    this_trip.join.add(this_user)
    return redirect('/dashboard')

def cancel(request, number):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.get(id=number)
    this_trip.join.remove(this_user)
    return redirect('/dashboard')
