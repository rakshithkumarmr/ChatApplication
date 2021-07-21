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
    path('delete/<str:id><str:ro>/',views.delete,name='delete'),

    path('group/',views.group,name='group'),
    path('create_group/',views.create_group,name='create_group'),
    path('group1/<str:group_name>/',views.group1,name='group1'),
    path('search_group/',views.search_group,name='search_group'),
    path('send1/',views.send1,name='send1'),
    path('delete_group/<str:id><str:gr>/',views.delete_group,name='delete_group'),

    path('add_member/<str:group>/',views.add_member,name='add_member'),
    path('group_members/<str:group>/', views.group_members, name='group_members'),
    path('leave_group/<str:group>/', views.leave_group, name='leave_group'),
    path('join_group/', views.join_group, name='join_group'),

]