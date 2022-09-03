from django.urls import path
from sports.views import CourtCreateView, ItemCreateView, SportCreateView, sportdetail,courtdetail
from users.views import home, register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('create/',SportCreateView.as_view(),name="sport-create"),
    path('detail/<int:sportid>/',sportdetail,name='sport-detail'),
    path('courtcreate/<int:sportid>/',CourtCreateView.as_view(),name='court-create'),
    path('courtdetail/<int:courtid>/',courtdetail,name='court-detail'),
    path('itemcreate/<int:sportid>/',ItemCreateView.as_view(),name='item-create'),
]