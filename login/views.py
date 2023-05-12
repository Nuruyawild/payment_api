from django.shortcuts import render

# Create your views here.


from django.shortcuts import render,redirect
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .models import User,ConfirmString,invoice_detail
from .forms import UserForm,RegisterForm
from . import serializers
import hashlib
import datetime
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework_jwt.settings import api_settings


#encrypt
def hash_code(s,salt='mysite'):
    h=hashlib.sha3_256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    return render(request,'login/index.html')

def balance(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    return render(request,'login/balance.html')


def deposit(request):
    if request.method == 'GET':
        return render(request,'login/deposit.html')
    elif request.method == 'POST':
        x = int(request.session.get('balance'))
        y = int(request.POST['y'])
        result = x + y
        st=User.objects.filter(id=request.session.get('user_id')).update(balance=result)
        serializer_class = serializers.PostSerializer
        if(st==1):
            return render(request,'login/deposit.html',locals())   
        else:
            return HttpResponse('<h1>Unsuccessful!</h1>')
        
def invoice_pay(request):
     # add | delete | modified | select
    # GET ?id=xxx data list
    # POST  submit data  success | fail
    # PUT submit data  success | fail
    # delete /id success | fail 
    if request.method == 'GET':
        return render(request,'login/invoice_pay.html')
    elif request.method == 'POST':

        if request.session.get('balance'):
    
            x = int(request.session.get('balance'))
        # print(request.POST)
        # y = request.POST.get('y')
        
        

        data = json.loads(request.body)
        y = data['totalAmount']


        # u=request.POST.get('id')
        print(request.body)
        u = data['orderid']
        s = data['AID']
        e = data['airline']
        # s=request.POST.get('AID')
        # e=request.POST.get('airline')
        result = x - int(y) 

        print("totalAMount:", y, "AID:", s, "airline:", e, "result:", result)

        key = hash_code(u + s + e + str(result) +  str(y) )


        return JsonResponse({'key': key})

        
        # invoice_detail.objects.create(
        #     orderid=u,
        #     AID=s,
        #     airline=e,
        #     totalAmount=y,
        #     key = key,
        # )
        # generate key
        # serializer_class = serializers.TutorialSerializer
        # return render(request,'login/invoice_pay.html',locals()) 
        

def statement(request):
     
    if request.method=="POST":
 
        info_list=invoice_detail.objects.all()
        serializer_class = serializers.PostSerializer
 
        return render(request,"login/statement.html",{"info_list":info_list})
    
    return render(request,"login/statement.html")
 


def login(request):
    if request.session.get('is_login',None): 
        return redirect('/index/')
    if request.method=='POST':
        login_form=UserForm(request.POST)
        
        message='Please check content！'
        if login_form.is_valid():
            is_api = login_form.cleaned_data.get('is_api')
            print("is_api:",is_api)
            if is_api == 1:
                print(request.cookies)        
                return JsonResponse({'csrf_token': True})


            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')


            try:
                user=User.objects.get(name=username)
            except:
                message='Username does not exist！'
                return render(request,'login/login.html',locals())
            if user.password==hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['balance'] = user.balance
                
                return redirect('/index/')
            else:
                message='Password incorrect!'
                return render(request,'login/login.html',locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form=UserForm()
    return render(request, 'login/login.html',locals())


def login(request):
    # username + password  -> csrftoken
    csrf_token = ''
    if request.COOKIES.get('csrftoken'):
       csrf_token = request.COOKIES.get('csrftoken')
    if request.method == 'POST' and request.content_type == 'application/json':
        if request.body:
            postData = json.loads(request.body)
        if postData['is_api'] == 1:
            username = postData['username']
            password = postData['password']
            try:
                user=User.objects.get(name=username)
            except:
                message='Username does not exist！'
                return JsonResponse({'code': -1, 'message': message})
            if user.password==hash_code(password) and csrf_token != '':
                return JsonResponse({'code': 0, 'message': 'success', 'csrf_token': csrf_token })
            elif csrf_token == '':
                return JsonResponse({'code': -1, 'message': 'Program error', 'csrf_token': '' })
            else:
                message='Password incorrect!'
                return JsonResponse({'code': -1, 'message': message, 'csrf_token': '' })


    if request.session.get('is_login',None): 
        return redirect('/index/')
    if request.method=='POST':
        login_form=UserForm(request.POST)
        
        message='Please check content！'
        if login_form.is_valid():
            is_api = login_form.cleaned_data.get('is_api')
            print("is_api:",is_api)
            if is_api == 1:
                print(request.cookies)        
                return JsonResponse({'csrf_token': True})


            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')


            try:
                user=User.objects.get(name=username)
            except:
                message='Username does not exist！'
                return render(request,'login/login.html',locals())
            if user.password==hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['balance'] = user.balance
                
                return redirect('/index/')
            else:
                message='Password incorrect!'
                return render(request,'login/login.html',locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form=UserForm()
    return render(request, 'login/login.html',locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form =RegisterForm(request.POST)
        message = "Please check the content!"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            realname = register_form.cleaned_data.get('realname')
            user_id_number = register_form.cleaned_data.get('user_id_number')
            user_phone = register_form.cleaned_data.get('user_phone')
            

            if password1 != password2:
                message = 'Different password!'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = 'User existed!'
                    return render(request, 'login/register.html', locals())
                same_email_user =User.objects.filter(email=email)
                if same_email_user:
                    message = 'Email existed!'
                    return render(request, 'login/register.html', locals())

                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.realname = realname
                new_user.user_id_number = user_id_number
                new_user.user_phone = user_phone
                new_user.save()
                serializer_class = serializers.PostSerializer
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form =RegisterForm()
    return render(request, 'login/register.html', locals())


def user_confirm(request):
    code=request.GET.get('code',None)
    message=''
    try:
        confirm=ConfirmString.objects.get(code=code)
    except:
        message='Error!'
        return render(request,'/login/confirm.html',locals())

    c_time=confirm.c_time
    now=datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = 'Error!'
        return render(request, 'login/confirm.html', locals())

    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = 'Thanks'
        return render(request, 'login/confirm.html', locals())











def logout(request):
    if not request.session.get('is_login',None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")

    request.session.flush()
    # 或者使用下面的方法清除缓存数据
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")