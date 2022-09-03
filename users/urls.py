from django.urls import path
from users.views import SportListView, activate, allsports, home, profile, register, userlist
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('',home,name="home"),
    path('profile/',profile,name='profile'),
    path('userlist/<int:personid>/',userlist,name="userlist"),
    path('activate/<slug:uidb64>/<slug:token>/',activate,name='activate'),
    path('all-sports/',SportListView.as_view(),name='all-sports'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),name="password_reset_complete"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),name="password_reset_confirm"),
]