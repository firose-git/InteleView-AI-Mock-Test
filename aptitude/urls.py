from django.urls import path
from . import views

app_name = 'aptitude'

urlpatterns = [
    path('start/', views.start_test_page, name='start_test'),          # Show confirmation
    path('start-test/', views.start_test_logic, name='start_test_logic'),  # Starts the test
    path('question/', views.question_page, name='question_page'),
    path('result/', views.result_page, name='result'),
    path('log-cheating/', views.log_cheating, name='log_cheating'),

]
