from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MyUserCreationForm
from pay.models import Wallet,Notification
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django_user_agents.utils import get_user_agent




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

    
@login_required
def profile(request):
    return render(request,'users/profile.html',{})


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(phone)
        try:
            user = User.objects.get(phone=phone)
        except:
            messages.error(request, "User does not exist")
        user = authenticate(request,phone=phone,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Phone number or Password is incorrect')
    context = {'page':page}
    return render(request,'users/login_register.html',context)

@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')



def registerUser(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            if user.phone[0] != '0' and user.phone[1] != '9' :
                messages.error(request, "Invalid Phone number")
            elif  len(user.phone) < 9:
                messages.error(request, "Invalid Phone number")
            else:
            
                user.username = user.name
                user_agent = get_user_agent(request)
                ip = get_client_ip(request)
                user.user_agent = user_agent
                user.ip_address = ip
                user.save()
                
                # login(request,user)
                messages.success(request, "Successfully created")
                return redirect('login')
        else:
            messages.error(request, "An error occured during registration")
    return render(request,'users/login_register.html',{'page':page,'form':form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            # Send noti after updated
            Notification.objects.create(
                amount=0,user=request.user, data="Your account password is successfully changed"
                )
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })

