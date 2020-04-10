from django.shortcuts import render
from basic_app.forms import UserForm,UserProfile

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):
    registered=False

    if(request.method=='POST'):
        user_form=UserForm(data=request.POST)
        profile_form=UserProfile(data=request.POST)

        if(user_form.is_valid() and profile_form.is_valid()):
            user=user_form.save()
            user.set_password(user.password) #Hashing the Password
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user

            if('profile_pic' in request.FILES):
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()


            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfile()

    return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

@login_required
def special(request):
    return HttpResponse("Hi Logged In Successfully!!!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if(user):
            if(user.is_active):
                login(request,user)
                return render(request,'basic_app/logout.html')

            else:
                return HttpResponse("Account not Active!!!")

        else:
            print("Someone tried to login and failed!!!")
            print("Username: {} and Password: {} tried to Log In!! ".format(username,password))
            return HttpResponse("Invalid Login!!")

    else:
        return render(request,'basic_app/login.html',{})
