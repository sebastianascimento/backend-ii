"""
URL patterns for the hello app.
"""
from django.urls import path
from . import views

app_name = 'hello'  # Namespace for URL naming

urlpatterns = [
    path('', views.index, name='index'),
    path('api/hello/', views.hello_api, name='hello_api'),
]