from django.urls import path
from . import views

app_name = 'GD'

urlpatterns = [
    path('', views.gd_home, name='gd_home'),
    path('instructions/', views.gd_instructions, name='gd_instructions'),
    path('start/', views.gd_session, name='gd_session'),
    path('results/', views.gd_results, name='gd_results'),
    path('transcribe/', views.transcribe_audio, name='gd_transcribe'),
    path('submit_results/', views.submit_results, name='submit_results'),  # ✅ FIXED: no leading slash
]
