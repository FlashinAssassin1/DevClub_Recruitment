from django.views.generic import ListView
from django.shortcuts import render,redirect
from users.forms import MemberRegisterForm
from django.contrib import messages
from sports.models import Sport, UserBooking
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import send_mail
from users.models import CustomUser
from .forms import UserUpdateForm,ProfileUpdateForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from six import text_type
import os
from django.contrib.sites.shortcuts import get_current_site

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

def register(request):
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if CustomUser.objects.filter(email__iexact=email).count() == 0:
                print('cool')
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                subject = 'Activate the Account'
                current_site = get_current_site(request)
                message = render_to_string('users/email_template.html',{
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                send_mail(subject,message,os.environ.get('EMAIL_USER'),[email])
                messages.success(request, f'Account created for {username}! Activate from Email!')
                return redirect('register')
            else:
                messages.warning(request, f'There is already an account with this email!')
                return redirect('register')

    else:
        form = MemberRegisterForm()
    return render(request,'users/register.html',{'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Account activated for {user.username}!')
        return redirect('login')
    else:
        messages.warning(request, f'Activation Link is invalid')
        return redirect('register')

def home(request):
    recentbooks = UserBooking.objects.all().order_by('-modified_time')[0:5]
    trendsports = set()
    for booking in recentbooks:
        if booking:
            trendsports.add(booking.slot.court.sport)

    if request.method == 'POST':
        searched = request.POST['searched']
        result = Sport.objects.filter(name__contains=searched)
        return render(request,"users/home.html",{'sports':trendsports,'searched': searched,'searchedsports': result})
    else:
        return render(request,"users/home.html",{'sports':trendsports})

def allsports(request):
    allsports = Sport.objects.all()
    return render(request,'users/allsports.html',{'allsports':allsports})

class SportListView(ListView):
    model = Sport
    template_name = 'users/allsports.html'
    context_object_name = 'sports'
    paginate_by = 2

    def get_queryset(self):
        return Sport.objects.all()

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
    
    if request.method == 'POST' and request.user.type == 2:
        stat = request.POST['stat']
        id = request.POST['id']
        if id:
            booking = UserBooking.objects.filter(pk=id).first()
            booking.status = stat
            booking.save()
            if stat == 1:
                message = 'Booking Accepted'
            else:
                message = 'Booking Rejected'
            send_mail('Booking Status Change',message,os.environ.get('EMAIL_USER'),[booking.user.email])


    
    userbookings = UserBooking.objects.filter(user=request.user).order_by('-modified_time')
    allbookings = UserBooking.objects.all().order_by('-modified_time')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'userbookings':userbookings,
        'allbookings':allbookings,
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