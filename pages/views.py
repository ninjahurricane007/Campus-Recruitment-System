from polls.models import Question
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from pages.models import Profile
from django.contrib.auth.decorators import login_required





# Create your views here.


def home(request):
    return render(request, 'pages/home.html')

def landing(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'pages/landing.html', context)

def user_login(request):
    print('hello')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('/login')
    else:
        return render(request,'userreg/login.html')

def user_logout(request):
    logout(request)
    messages.success(request,("You Were Logged Out!"))
    return redirect('/')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if password.isnumeric():
            messages.info(request,'Password should include atleast one alphabet')
            return redirect(user_signup)
        elif password.isalpha():
            messages.info(request,'password should include atleast one number')
            return redirect(user_signup)
        hashed_password = make_password(password)
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            messages.info(request,'Already have an account with same email id')
            return redirect(user_signup)
        else:
            user = User(username=username,password=hashed_password,email=email)
            user.save()
            user = authenticate(request, username=username, password=password)
            login(request,user)
            return redirect('/home')
    return render(request,'userreg/signup.html')

@login_required(login_url='/auth/login')
def profile(request):
    all_data = User.objects.all()
    return render(request,'pages/profile.html', {'key':all_data})

@login_required(login_url='/auth/login')
def editprofile(request):
    if request.method == 'POST':
        ph_num = request.POST.get('ph_num')
        clg_name = request.POST.get('clg_name')
        sem = request.POST.get('sem')
        brch = request.POST.get('brch')
        cgpa = request.POST.get('cgpa')
        bklgs =request.POST.get('bklgs')
        dp_img = request.FILES.get('dp_img')
        profile = Profile(ph_num=ph_num,clg_name=clg_name,sem=sem,brch=brch,cgpa=cgpa,bklgs=bklgs,dp_img=dp_img,user=request.user)
        profile.save()
        print(profile)
        return redirect('/profile')
    return render(request,'pages/editprofile.html')