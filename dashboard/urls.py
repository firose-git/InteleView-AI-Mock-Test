from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('student/', views.student_dashboard, name='student'),
    path('professional/', views.professional_dashboard, name='professional'),
    path('trial/', views.trial_dashboard, name='trial'),

    # Add these:
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('aptitude/', views.aptitude_test, name='aptitude'),
    path('technical/', views.technical_round, name='technical'),
    path('gd/', views.group_discussion, name='gd'),
    path('hr/', views.hr_round, name='hr'),
    path('history/', views.performance_history, name='history'),
    path('feedback/', views.feedback_form, name='feedback'),
]
