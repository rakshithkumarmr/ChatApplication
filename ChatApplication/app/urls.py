from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('profile/',views.profile,name='profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('visit_room/',views.visit_room,name='visit_room'),
    path('room1/<str:room>/',views.room1,name='room1'),
    path('checkview/',views.checkview,name='checkview'),
    path('send/',views.send,name='send'),
    path('room/<str:room>/', views.room, name='room1'),
    path('seacrh/', views.search, name='seacrh'),

]