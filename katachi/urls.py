from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input/', views.input, name='input'),
    path('user/', views.user, name='users'),
    path('user/add',views.user_add,name='user_add')
]