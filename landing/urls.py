from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('contact/', views.contact_page, name='contact'),
]
