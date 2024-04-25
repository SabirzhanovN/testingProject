from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('test_detail/<int:id>/', views.test_detail, name='test_detail'),
    path('testing/<str:ids>/', views.testing, name='testing'),
    path('result/<int:id>/', views.result, name='result')
]