from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # Email OTP verification (during first login)
    path('verify-otp/', views.verify_otp, name='verify_otp'),

    # Forgot password flow
    path('forgot-password/', views.forgot_password_request, name='forgot_password'),
    path('reset/<str:token>/', views.reset_password, name='reset_password'),

    # Dashboard & Lists
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('tests/', views.test_list, name='test_list'),

    # Optional: User editing
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
