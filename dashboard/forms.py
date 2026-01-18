from django import forms

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(
        label='Upload Resume (PDF/DOC)',
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'})
    )