# ✅ FINAL WORKING USERS APP FOR FULL REGISTRATION, LOGIN, OTP VERIFICATION

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
import traceback
import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect
User = get_user_model()

# Memory stores
otp_store = {}  # { email: { otp, data, sent_time } }
reset_tokens = {}  # { token: username }
trial_ip_attempts = {}  # { ip: count }

# -------------------- GET CLIENT IP --------------------
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

# -------------------- REGISTER VIEW --------------------
def register(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        department = request.POST.get('department') if user_type == 'student' else None

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messages.error(request, 'Invalid email format.')
            return redirect('users:register')

        if password != confirm or len(password) < 6:
            messages.error(request, 'Passwords must match and be at least 6 characters.')
            return redirect('users:register')

        if user_type == 'trial':
            ip = get_client_ip(request)
            if trial_ip_attempts.get(ip, 0) >= 5:
                return HttpResponse("Trial attempt limit exceeded from this IP/device.")

        otp = get_random_string(length=6, allowed_chars='1234567890')
        otp_store[email] = {
            'otp': otp,
            'sent_time': timezone.now(),
            'data': {
                'name': name,
                'email': email,
                'password': password,  # plain for now, hash later in verify
                'user_type': user_type,
                'department': department
            }
        }

        send_mail(
            subject="InteleView AI – Verify Your Email",
            message=f"Your OTP is: {otp}\nValid for 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email]
        )

        return redirect('users:verify_otp', email=email)

    return render(request, 'users/register.html')

# -------------------- VERIFY OTP --------------------
def verify_otp(request, email):
    saved = otp_store.get(email)
    if not saved:
        messages.error(request, "OTP session expired. Please register again.")
        return redirect('users:register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp_sent_time = saved.get('sent_time', timezone.now())

        if timezone.now() - otp_sent_time > timedelta(minutes=10):
            del otp_store[email]
            messages.error(request, "OTP expired. Please resend OTP.")
            return redirect('users:register')

        if saved['otp'] == entered_otp:
            data = saved['data']
            try:
                user = User.objects.create_user(
                    username=data['email'],
                    email=data['email'],
                    password=data['password']  # this is hashed inside create_user
                )
                user.first_name = data['name']
                user.user_type = data['user_type']
                if data.get('department'):
                    user.department = data['department']
                user.email_verified = True
                user.otp_code = None
                user.otp_created_at = timezone.now()
                user.save()

                if user.user_type == 'trial':
                    ip = get_client_ip(request)
                    trial_ip_attempts[ip] = trial_ip_attempts.get(ip, 0) + 1

                del otp_store[email]
                messages.success(request, 'Email verified successfully. Please login.')
                return redirect('users:user_login')

            except Exception as e:
                print("OTP verification error:")
                traceback.print_exc()
                messages.error(request, 'Something went wrong. Try again.')
                return redirect('users:register')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'users/verify_otp.html', {'email': email})

# -------------------- LOGIN VIEW --------------------
def login_view(request):
    if request.user.is_authenticated:
        try:
            user_type = getattr(request.user, 'user_type', None)
            if user_type == 'student':
                return redirect('dashboard:student')
            elif user_type == 'professional':
                return redirect('dashboard:professional')
            elif user_type == 'trial':
                return redirect('dashboard:trial')
        except Exception as e:
            print("LOGIN REDIRECT ERROR:", e)
        return redirect('landing:home')

    user_type_from_url = request.GET.get('type', '')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        redirect_type = request.POST.get('user_type', '')

        # Basic validation
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messages.error(request, 'Invalid email format.')
            return redirect('users:user_login')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return redirect('users:user_login')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            try:
                redirect_type = redirect_type or getattr(user, 'user_type', None)
                if redirect_type == 'student':
                    return redirect('dashboard:student')
                elif redirect_type == 'professional':
                    return redirect('dashboard:professional')
                elif redirect_type == 'trial':
                    return redirect('dashboard:trial')
            except Exception as e:
                print("REDIRECT ERROR:", e)

            return redirect('landing:home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'users/login.html', {'user_type': user_type_from_url})

# -------------------- RESEND OTP --------------------
@require_GET
def resend_otp(request, email):
    saved = otp_store.get(email)
    if not saved:
        messages.error(request, "No OTP request found for this email.")
        return redirect('users:register')

    new_otp = get_random_string(length=6, allowed_chars='1234567890')
    saved['otp'] = new_otp
    saved['sent_time'] = timezone.now()
    otp_store[email] = saved

    send_mail(
        subject="InteleView AI – Resend OTP",
        message=f"Your new OTP is: {new_otp}\nThis OTP is valid for only 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )

    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('users:verify_otp', email=email)



# -------------------- FORGOT PASSWORD --------------------
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = get_random_string(30)
            reset_tokens[token] = user.username

            reset_link = request.build_absolute_uri(
                f"/users/reset-password/{token}/"
            )

            send_mail(
                subject="Reset Your Password – InteleView AI",
                message=f"Click the link to reset your password:\n{reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )

            messages.success(request, "Reset link sent to your email.")
        except User.DoesNotExist:
            messages.error(request, "Email not registered.")

    return render(request, 'users/forgot_password.html')


# -------------------- RESET PASSWORD --------------------
def reset_password(request, token):
    username = reset_tokens.get(token)
    if not username:
        return HttpResponse("Invalid or expired token.")

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        if password != confirm or len(password) < 6:
            messages.error(request, "Passwords must match and be at least 6 characters.")
        else:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            del reset_tokens[token]
            messages.success(request, "Password reset successful.")
            return redirect('users:user_login')

    return render(request, 'users/reset_password.html', {'token': token})


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('landing:home')


@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        messages.success(request, "✅ Profile updated!")
        return redirect('users:profile')
    return render(request, 'users/edit_profile.html')


from .forms import SettingsForm, CareerPreferencesForm
from django.contrib import messages
from django.urls import reverse
@login_required
def settings_view(request):
    user = request.user

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'account_settings':
            form = SettingsForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Profile updated successfully.")
                return redirect('users:settings')

        elif form_type == 'preferences':
            user.camera_enabled = 'camera_enabled' in request.POST
            user.sound_enabled = 'sound_enabled' in request.POST
            user.tab_alert = 'tab_alert' in request.POST
            user.save()
            messages.success(request, "✅ Preferences updated successfully.")
            return HttpResponseRedirect(reverse('users:settings') + '#preferences')

        elif form_type == 'notifications':
            user.email_notify = 'email_notify' in request.POST
            user.push_notify = 'push_notify' in request.POST
            user.save()
            messages.success(request, "✅ Notification settings updated successfully.")
            return redirect('users:settings')

        elif form_type == 'career':
            career_form = CareerPreferencesForm(request.POST)
            if career_form.is_valid():
                request.session['career_preferences'] = career_form.cleaned_data
                messages.success(request, "✅ Career preferences saved.")
                return redirect('users:settings')

    # GET method
    form = SettingsForm(instance=user)
    career_data = request.session.get('career_preferences', {})
    career_form = CareerPreferencesForm(initial=career_data)

    return render(request, 'users/settings.html', {
        'form': form,
        'career_form': career_form
    })
@login_required
def delete_account(request):
    user = request.user

    if request.method == "POST":
        entered_email = request.POST.get('email')
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('delete_account_otp')
        otp_time_str = request.session.get('otp_created_at')

        if not session_otp or not otp_time_str:
            messages.error(request, "❌ OTP not found. Please request again.")
            return redirect('users:settings')

        # Check OTP expiry
        otp_time = datetime.fromisoformat(otp_time_str)
        if timezone.now() - otp_time > timedelta(minutes=5):
            messages.error(request, "❌ OTP expired. Please request a new one.")
            return redirect('users:settings')

        if entered_email != user.email:
            messages.error(request, "❌ Email mismatch.")
            return redirect('users:settings')

        if entered_otp != session_otp:
            messages.error(request, "❌ Invalid OTP.")
            return redirect('users:settings')

        # Delete account
        user_email = user.email
        username = user.username
        user.delete()

        send_mail(
            subject="Account Deleted - InteleView AI",
            message=f"Hi {username}, your account has been successfully deleted from InteleView AI.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=True,
        )

        messages.success(request, "✅ Your account has been permanently deleted.")
        return render(request, 'users/account_deleted.html')

    return redirect('users:settings')


from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
import random

@login_required
def send_delete_otp(request):
    if request.method == "POST":
        now = timezone.now()
        last_sent_str = request.session.get('otp_last_sent')

        if last_sent_str:
            last_sent = datetime.fromisoformat(last_sent_str)
            if now - last_sent < timedelta(seconds=60):
                return JsonResponse({"status": False, "error": "Wait 60s before resending."}, status=429)

        otp = str(random.randint(100000, 999999))
        request.session['delete_account_otp'] = otp
        request.session['otp_created_at'] = now.isoformat()
        request.session['otp_last_sent'] = now.isoformat()

        send_mail(
            subject="OTP for Account Deletion - InteleView AI",
            message=f"Hi {request.user.username}, your OTP to delete your account is: {otp}. It expires in 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": "Invalid method"}, status=405)
