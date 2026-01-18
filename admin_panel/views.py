from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta

from users.models import UserProfile
from testsystem.models import TestSession
from users.utils import generate_otp, send_otp_email


# ✅ Restrict only staff/admin users
def is_admin(user):
    return user.is_authenticated and user.is_staff


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower().strip()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            if not user.email_verified:
                otp = generate_otp()
                user.otp_code = otp
                user.otp_created_at = now()
                user.save()
                send_otp_email(user.email, otp)
                request.session['temp_user_id'] = user.id
                return redirect('admin_panel:verify_otp')
            else:
                login(request, user)
                return redirect('admin_panel:dashboard')

        messages.error(request, "Invalid credentials or not an admin.")
    return render(request, 'admin_panel/login.html')


def verify_otp(request):
    user_id = request.session.get('temp_user_id')
    if not user_id:
        return redirect('admin_panel:admin_login')

    user = get_object_or_404(UserProfile, pk=user_id)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if (
            user.otp_code == otp_input and
            user.otp_created_at and
            now() - user.otp_created_at <= timedelta(minutes=10)
        ):
            user.email_verified = True
            user.otp_code = None
            user.save()
            login(request, user)
            return redirect('admin_panel:dashboard')
        else:
            messages.error(request, "Invalid or expired OTP.")

    return render(request, 'admin_panel/verify_otp.html', {'email': user.email})


@login_required(login_url='admin_panel:admin_login')
@user_passes_test(is_admin)
def admin_logout(request):
    logout(request)
    return redirect('admin_panel:admin_login')


@login_required(login_url='admin_panel:admin_login')
@user_passes_test(is_admin)
def dashboard(request):
    total_users = UserProfile.objects.count()
    total_sessions = TestSession.objects.count()
    total_score = TestSession.objects.aggregate(Sum('score'))['score__sum'] or 0
    recent_sessions = TestSession.objects.select_related('user').order_by('-started_at')[:5]
    
    return render(request, 'admin_panel/dashboard.html', {
        'total_users': total_users,
        'total_sessions': total_sessions,
        'total_score': total_score,
        'recent_sessions': recent_sessions
    })


@login_required(login_url='admin_panel:admin_login')
@user_passes_test(is_admin)
def user_list(request):
    query = request.GET.get('q', '')
    users = UserProfile.objects.filter(username__icontains=query).order_by('-updated_at')

    return render(request, 'admin_panel/user_list.html', {
        'users': users,
        'search_query': query
    })

@login_required(login_url='admin_panel:admin_login')
@user_passes_test(is_admin)
def test_list(request):
    tests = TestSession.objects.select_related('user').all()
    return render(request, 'admin_panel/test_list.html', {'tests': tests})


from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from users.models import UserProfile
from django.shortcuts import get_object_or_404

# Store token in DB (optional: use a separate model for production)
reset_tokens = {}

def forgot_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = UserProfile.objects.filter(email=email, is_staff=True).first()
        if user:
            token = get_random_string(32)
            reset_tokens[token] = {'user_id': user.id, 'created': now()}

            reset_url = request.build_absolute_uri(reverse('admin_panel:reset_password', args=[token]))
            send_mail(
                'InteleView Admin Password Reset',
                f'Click the link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )
            messages.success(request, "Reset link sent to your email.")
        else:
            messages.error(request, "Email not found or not an admin.")

    return render(request, 'admin_panel/forgot_password.html')


def reset_password(request, token):
    token_data = reset_tokens.get(token)

    if not token_data:
        messages.error(request, "Invalid or expired token.")
        return redirect('admin_panel:forgot_password')

    if (now() - token_data['created']).total_seconds() > 900:
        messages.error(request, "Token expired. Try again.")
        return redirect('admin_panel:forgot_password')

    user = get_object_or_404(UserProfile, id=token_data['user_id'])

    if request.method == 'POST':
        new_password = request.POST.get('password')
        user.password = make_password(new_password)
        user.save()
        del reset_tokens[token]
        messages.success(request, "Password reset successful. Please login.")
        return redirect('admin_panel:admin_login')

    return render(request, 'admin_panel/reset_password.html', {'token': token})



from django.shortcuts import get_object_or_404

@login_required(login_url='admin_panel:admin_login')
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        user.attempts_left = request.POST.get('attempts_left', user.attempts_left)
        user.score = request.POST.get('score', user.score)
        user.rating = request.POST.get('rating', user.rating)
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('admin_panel:user_list')

    return render(request, 'admin_panel/edit_user.html', {'user': user})

@login_required(login_url='admin_panel:admin_login')
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    user.delete()
    messages.success(request, "User deleted.")
    return redirect('admin_panel:user_list')
