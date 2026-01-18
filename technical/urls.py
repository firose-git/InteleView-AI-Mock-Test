# technical/urls.py

from django.urls import path
from . import views
app_name = 'technical'  # 👈 namespace for the app
urlpatterns = [
    path('', views.technical_ui, name='technical_ui'),  # 👈 use empty string to match /technical/
    path('api/questions/', views.get_technical_questions, name='get_technical_questions'),
    path('api/submit/', views.submit_technical_answer, name='submit_technical_answer'),
    path('result/', views.technical_result, name='technical_result'), 
]
