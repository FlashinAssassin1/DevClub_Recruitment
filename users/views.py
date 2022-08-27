from django.shortcuts import render,redirect
from users.forms import MemberRegisterForm
from django.contrib import messages
from sports.models import Sport
from django.contrib.auth.decorators import login_required,user_passes_test

from users.models import CustomUser
from .forms import UserUpdateForm,ProfileUpdateForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = MemberRegisterForm()
    return render(request,'users/register.html',{'form': form})

def home(request):
    sports = Sport.objects.all()
    
    if request.method == 'POST':
        searched = request.POST['searched']
        result = Sport.objects.filter(name__contains=searched)
        return render(request,"users/home.html",{'sports':sports,'searched': searched,'searchedsports': result})
    else:
        return render(request,"users/home.html",{'sports':sports})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)

def admin_check(user):
    if user.type == 3:
        return True
    return False

@user_passes_test(admin_check)
def userlist(request,personid):
    members = CustomUser.objects.filter(type=1)
    staff = CustomUser.objects.filter(type=2)

    if personid != 0:
        person = CustomUser.objects.filter(pk=personid).first()
        if person.type == 2:
            person.type = 1
        else:
            person.type = 2
        person.save()

    return render(request,"users/userlist.html",{'members':members,'staff':staff})