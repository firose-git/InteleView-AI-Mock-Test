from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from .forms import ResumeUploadForm
import os
from django.contrib import messages
from django.conf import settings
@login_required
def after_login(request):
    return redirect_user_dashboard(request.user)

@login_required
def upload_resume(request):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        if resume_file:
            user = request.user
            resumes_dir = os.path.join(settings.MEDIA_ROOT, 'resumes')

            # ✅ Create 'resumes' directory if it doesn't exist
            os.makedirs(resumes_dir, exist_ok=True)

            # File path
            resume_path = f'resumes/{user.username}_{resume_file.name}'
            full_path = os.path.join(settings.MEDIA_ROOT, resume_path)

            # Save the uploaded file
            with open(full_path, 'wb+') as destination:
                for chunk in resume_file.chunks():
                    destination.write(chunk)

            # Optional: Save the resume path to the user model if needed
            user.resume = resume_path
            user.save()

            messages.success(request, "✅ Resume uploaded successfully.")
        else:
            messages.error(request, "⚠️ Please upload a valid file.")

        return redirect('dashboard:student')

    return render(request, 'dashboard/upload_resume.html')


@login_required
def aptitude_test(request):
    return render(request, 'dashboard/aptitude_test.html')

@login_required
def technical_round(request):
    return render(request, 'dashboard/technical_round.html')

@login_required
def group_discussion(request):
    return render(request, 'dashboard/group_discussion.html')

@login_required
def hr_round(request):
    return render(request, 'dashboard/hr_round.html')

@login_required
def performance_history(request):
    return render(request, 'dashboard/performance_history.html')

@login_required
def feedback_form(request):
    return render(request, 'dashboard/feedback_form.html')

@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect_user_dashboard(request.user)
    return render(request, 'dashboard/student_dashboard.html', {'user': request.user})

@login_required
def professional_dashboard(request):
    if request.user.user_type != 'professional':
        return redirect_user_dashboard(request.user)
    return render(request, 'dashboard/professional_dashboard.html', {'user': request.user})

@login_required
def trial_dashboard(request):
    if request.user.user_type != 'trial':
        return redirect_user_dashboard(request.user)
    return render(request, 'dashboard/trial_dashboard.html', {'user': request.user})

from django.shortcuts import redirect

def redirect_user_dashboard(user):
    if user.user_type == 'student':
        return redirect('dashboard:student')
    elif user.user_type == 'professional':
        return redirect('dashboard:professional')
    elif user.user_type == 'trial':
        return redirect('dashboard:trial')
    else:
        return redirect('home')  # fallback
