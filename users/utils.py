import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_email(to_email, otp):
    subject = 'Your InteleView Admin OTP Code'
    message = f'Your OTP code for verification is: {otp}. It will expire in 10 minutes.'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [to_email])
