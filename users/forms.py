from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser, Profile
from django import forms

class MemberRegisterForm(UserCreationForm):
    class Meta():
        model = CustomUser
        fields = ['username','email','password1','password2']

class ProfileUpdateForm(forms.ModelForm):
     class Meta():
        model = Profile
        fields = ['image']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta():
        model = CustomUser
        fields = ['username','email','description']   