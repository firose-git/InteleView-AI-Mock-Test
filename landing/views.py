from django.shortcuts import render, redirect

def landing_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'student':
            return redirect('dashboard:student')
        elif request.user.user_type == 'professional':
            return redirect('dashboard:professional')
        elif request.user.user_type == 'trial':
            return redirect('dashboard:trial')
    return render(request, 'landing/landing.html')

from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will respond shortly.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'landing/contact.html', {'form': form})
