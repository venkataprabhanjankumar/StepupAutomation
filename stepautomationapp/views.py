from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from .models import UserData
from .models import Country
from rest_framework import permissions
from rest_framework.decorators import permission_classes


def index(request):
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


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        keepsignin = request.POST.get('keepsignin')
        print(keepsignin)
        try:
            users = User.objects.get(Q(username=username) | Q(email=username))
            if check_password(password, users.password):
                try:
                    authToken = Token.objects.get(user_id=users.id)
                    authKey = authToken.key
                    print(authKey)
                    return HttpResponse(json.dumps({'status_msg': 'Ok', 'authKey': authKey}),
                                        content_type='application/json')
                except Token.DoesNotExist:
                    token_generation = Token.objects.create(user_id=users.id)
                    token_generation.save()
                    authToken = Token.objects.get(user_id=users.id)
                    authKey = authToken.key
                    print(authKey)
                    return HttpResponse(json.dumps({'status_msg': 'Ok', 'authKey': authKey}),
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


def dashboard(request, token):
    try:
        user = Token.objects.get(key=token)
        userdetails = User.objects.get(username=user.user)
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
                    'profilepic': 'http://127.0.0.1:8000/' + str(userdata.profilepic),
                    'countries': countries
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
                    'profilepic': 'http://127.0.0.1:8000/media/profilepic.png',
                    'countries': countries
                }
            )
    except Token.DoesNotExist:
        return render(
            request,
            'demo-web-studio.html',
            {}
        )


@permission_classes([permissions.AllowAny])
def getCities(request):
    sname = request.GET['countrydata']
    results = []
    cities = []
    answer = str(sname)
    selected_country = Country.objects.get(country=answer)
    cities = selected_country.city_set.all()
    for city in cities:
        results.append({'name': city.city})
    return HttpResponse(json.dumps(results), content_type='application/json')


def updateProfile(request, token):
    try:
        userdeatils = Token.objects.get(key=token)
        user = User.objects.get(username=userdeatils.user)
        print(request.body)
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        print(first_name, last_name, username, email)
        print(data.get('city'), data.get('country'))
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        try:
            userdetails = UserData.objects.get(userrelation=user.id)
            userdetails.country = data.get('country')
            userdetails.city = data.get('city')
            userdetails.address = data.get('address')
            userdetails.zipcode = data.get('zipcode')
            userdetails.save()
        except UserData.DoesNotExist:
            userdata = UserData.objects.create(
                userrelation=user,
                country=data.get('country'),
                city=data.get('city'),
                address=data.get('address'),
                zipcode=data.get('address')
            )
            userdata.save()

        return HttpResponse(json.dumps({'status_msg': 'Ok', 'msg': 'Successfully Updated'}),
                            content_type='application/json')
    except Token.DoesNotExist:
        return render(
            request,
            'demo-web-studio.html',
            {}
        )


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


def logout(request, token):
    try:
        token = Token.objects.get(key=token)
        token.delete()
        return HttpResponseRedirect('/')
    except Token.DoesNotExist:
        return render(
            request,
            'demo-web-studio.html',
            {}
        )
