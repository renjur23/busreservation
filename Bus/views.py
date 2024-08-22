from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm, ContactForm
from .models import CustomUser
from django.core.mail import send_mail

from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'b_register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = CustomUser.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                return redirect('home')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'b_login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    return render(request, 'contact_us.html')




def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

        
            send_mail(
                subject,
                f"Message from {name}, {email}, {phone}\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,
                ['danketravels@gmail.com'], 
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})