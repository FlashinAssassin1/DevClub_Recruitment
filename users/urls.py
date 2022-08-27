from django.urls import path
from users.views import home, profile, register, userlist
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('',home,name="home"),
    path('profile/',profile,name='profile'),
    path('userlist/<int:personid>/',userlist,name="userlist"),
]