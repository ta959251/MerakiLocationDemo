from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('event/', views.event),
    path('info/', views.info, name='info'),
    path('info_client/<str:client>/', views.info_client, name='info_client'),
]
