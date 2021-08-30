from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import UserData
from .models import Country


def index(request):
    if request.user.is_authenticated:
        return redirect('/account-profile')
    else:
        return render(
            request,
            'demo-web-studio.html',
            {}
        )


'''def handle_redirect(request, template):
    return render(
        request,
        template + '.html',
        {}
    )'''


@login_required(login_url='/login')
def delete_account(request):
    user = User.objects.get(username=request.user)
    logout(request)
    user.delete()
    return redirect('/')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        keepsignin = request.POST.get('keepsignin')
        print(keepsignin)
        try:
            users = User.objects.get(Q(username=username) | Q(email=username))
            if check_password(password, users.password):
                login(request, users)
                return HttpResponse(json.dumps({'status_msg': 'Ok'}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'Invalid Username or Password'}),
                                    content_type='application/json')
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'Invalid Username or Password'}),
                                content_type='application/json')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        usersemail = User.objects.filter(Q(username=username) | Q(email=email))
        if len(usersemail) != 0:
            return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'User or Email Already Exists'}),
                                content_type='application/json')
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return HttpResponse(json.dumps({'status_msg': 'Ok', 'msg': 'Successfully Registered'}),
                            content_type='application/json')


@login_required(login_url='/')
def dashboard(request):
    userdetails = User.objects.get(username=request.user)
    countries = Country.objects.all()
    try:
        userdata = UserData.objects.get(userrelation=userdetails)
        print(userdata.profilepic)
        print(userdata.country)
        return render(
            request,
            'account-profile.html',
            {
                'logged': True,
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'address': userdata.address,
                'zipcode': userdata.zipcode,
                'country': userdata.country,
                'city': userdata.city,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic),
                'countries': countries,
            }
        )
    except UserData.DoesNotExist:
        return render(
            request,
            'account-profile.html',
            {
                'logged': True,
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'address': '',
                'zipcode': '',
                'country': False,
                'city': False,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png',
                'countries': countries
            }
        )


@permission_classes([permissions.AllowAny])
def getCities(request):
    sname = request.GET['countrydata']
    results = []
    answer = str(sname)
    selected_country = Country.objects.get(country=answer)
    cities = selected_country.city_set.all()
    for city in cities:
        results.append({'name': city.city})
    return HttpResponse(json.dumps(results), content_type='application/json')


@login_required(login_url='/')
def updateProfile(request):
    try:
        user = User.objects.get(username=request.user)
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        try:
            userdata = UserData.objects.get(userrelation=user.id)
            userdata.country = request.POST.get('country')
            userdata.city = request.POST.get('city')
            userdata.address = request.POST.get('address')
            userdata.zipcode = request.POST.get('zipcode')
            userdata.save()
        except UserData.DoesNotExist:
            userdata = UserData.objects.create(
                userrelation=user,
                country=request.POST.get('country'),
                city=request.POST.get('city'),
                address=request.POST.get('address'),
                zipcode=request.POST.get('zipcode')
            )
            userdata.save()
        return redirect('/account-profile')
    except User.DoesNotExist:
        return render(
            request,
            'demo-web-studio.html',
            {}
        )


@login_required(login_url='/login')
def updateProfilePic(request):
    user = User.objects.get(username=request.user)
    userdetails = UserData.objects.get(userrelation=user.id)
    userdetails.profilepic = request.FILES.get('profilepic')
    userdetails.save()
    return redirect('/account-profile')


def aboutus(request):
    return render(
        request,
        'about.html',
        {}
    )


def contactus(request):
    return render(
        request,
        'contacts-v3.html',
        {}
    )


@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return redirect('/')
