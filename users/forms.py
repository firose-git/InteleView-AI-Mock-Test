# users/forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SettingsForm(forms.ModelForm):
    camera_monitoring = forms.BooleanField(required=False, label="Enable Camera Monitoring")
    tab_switch_alert = forms.BooleanField(required=False, label="Enable Tab Switch Alerts")
    sound_alert = forms.BooleanField(required=False, label="Enable Sound Alerts")

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'profile_pic','first_name', 'last_name']

class CareerPreferencesForm(forms.Form):
    job_role = forms.CharField(max_length=100, required=False)
    preferred_location = forms.CharField(max_length=100, required=False)
    expected_salary = forms.CharField(max_length=50, required=False)
