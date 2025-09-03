"""
URL configuration for django_ssl_checker project.
"""


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('handle_operation/', views.handle_operation, name="handle_operation"),
    path('verify_cert/', views.verify_cert, name='verify_cert'),
    path('decrypt_key/', views.decrypt_key, name='decrypt_key'),
    path('verify_bundle/', views.verify_bundle, name='verify_bundle'),
]
