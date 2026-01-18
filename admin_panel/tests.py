from django.test import TestCase
from django.urls import reverse
from users.models import UserProfile
from django.utils.timezone import now, timedelta
from django.core import mail


class AdminLoginTests(TestCase):
    def setUp(self):
        self.admin_user = UserProfile.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            email_verified=False  # simulate unverified user
        )

    def test_admin_login_triggers_otp_if_not_verified(self):
        response = self.client.post(reverse('admin_panel:admin_login'), {
            'username': 'admin_user',
            'password': 'admin123'
        })

        # Should redirect to OTP verification
        self.assertRedirects(response, reverse('admin_panel:verify_otp'))

        # OTP must be generated
        self.admin_user.refresh_from_db()
        self.assertIsNotNone(self.admin_user.otp_code)

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Your One-Time Password', mail.outbox[0].subject)

    def test_admin_login_wrong_password(self):
        response = self.client.post(reverse('admin_panel:admin_login'), {
            'username': 'admin_user',
            'password': 'wrongpass'
        })
        self.assertContains(response, "Invalid credentials", status_code=200)

    def test_verified_admin_direct_login(self):
        self.admin_user.email_verified = True
        self.admin_user.save()

        response = self.client.post(reverse('admin_panel:admin_login'), {
            'username': 'admin_user',
            'password': 'admin123'
        })

        self.assertRedirects(response, reverse('admin_panel:dashboard'))

    def test_otp_verification_success(self):
        self.admin_user.otp_code = '1234'
        self.admin_user.otp_created_at = now()
        self.admin_user.save()
        self.client.session['temp_user_id'] = self.admin_user.id
        self.client.session.save()

        response = self.client.post(reverse('admin_panel:verify_otp'), {'otp': '1234'})
        self.assertRedirects(response, reverse('admin_panel:dashboard'))

        # User must now be marked as verified
        self.admin_user.refresh_from_db()
        self.assertTrue(self.admin_user.email_verified)

    def test_otp_verification_expired(self):
        self.admin_user.otp_code = '1234'
        self.admin_user.otp_created_at = now() - timedelta(minutes=11)
        self.admin_user.save()
        self.client.session['temp_user_id'] = self.admin_user.id
        self.client.session.save()

        response = self.client.post(reverse('admin_panel:verify_otp'), {'otp': '1234'})
        self.assertContains(response, "Invalid or expired OTP", status_code=200)

    def test_password_reset_flow(self):
        response = self.client.post(reverse('admin_panel:forgot_password'), {'email': 'admin@example.com'})
        self.assertRedirects(response, reverse('admin_panel:admin_login'))

        user = UserProfile.objects.get(username='admin_user')
        token = user.reset_token
        reset_url = reverse('admin_panel:reset_password', args=[token])

        response = self.client.post(reset_url, {
        'new_password': 'newpass123',
        'confirm_password': 'newpass123'
        })
        self.assertRedirects(response, reverse('admin_panel:admin_login'))

    # Check password update
        user.refresh_from_db()
        self.assertTrue(user.check_password('newpass123'))
