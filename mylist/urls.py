from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register,name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('',index, name='list'),
    path('<int:pk>', view_detail, name='detail'),
    path('create/', create_todolist, name='create'),
    path('update/<int:pk>', update_todolist, name='update'),
    path('delete/<int:pk>/', delete_todolist, name='delete'),
    path('category/create', create_category, name='create_category'),
    path('search/',Search.as_view(),name='search'),
    path('delete/point/<int:pk>', delete_point, name='delete_point'),
    path('update/point/<int:pk>', update_point, name='update_point'),
]


