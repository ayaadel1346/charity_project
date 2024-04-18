from django.contrib.sessions.models import Session
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm, UserProfileForm
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from project.models import UserProfile, Project, Donation
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from .forms import UserProfileForm, UserForm,UserProfileRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:

                return render(request, 'registration/login.html', {'form': form, 'error_message': 'Invalid email or password.'})

        
            if check_password(password, user.password):
               
                request.session['username'] = user.username
                
               
                if user.is_superuser:
                    return redirect('admin_panel:admin_panel')  
                else:
                    return redirect('project:home')  
            else:
              
                return render(request, 'registration/login.html', {'form': form, 'error_message': 'Invalid email or password.'})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})



def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        request.session.flush()
        return HttpResponseRedirect(reverse('account:login'))
    else:
        return HttpResponseRedirect(reverse('account:login'))


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                # If the email already exists, send an error message
                user_form.add_error('email', 'This email is already in use. Please choose another one.')
            else:
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                protocol = 'http'
                domain = request.META['HTTP_HOST']
                activation_link = f"{protocol}://{domain}/account/?uidb64={uid}&token={token}"

                context = {
                    'email': user.email,
                    'protocol': protocol,
                    'domain': domain,
                    'uid': uid,
                    'token': token,
                    'user': user,
                    'activation_link': activation_link,
                }

                send_mail(
                    'Activate your account',
                    'registration/activation_email.html',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                    html_message=render_to_string('registration/activation_email.html', context)
                )

                return render(request, 'registration/activation_email_sent.html')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})



from django.contrib.auth.models import User

@login_required
def user_profile(request):
 
    username = request.session.get('username')

  
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:

        return HttpResponse("User does not exist for the provided username")

   
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
       
        return HttpResponse("User profile does not exist for the provided username")

    projects = Project.objects.filter(creator=user)
    donations = Donation.objects.filter(user=user)

    context = {
        'user_profile': user_profile,
        'projects': projects,
        'donations': donations,
    }
    return render(request, 'profile/Profile.html', context)




@login_required
def delete_account(request):
    error_message = None  
    
    if request.method == 'POST':
        password = request.POST.get('password', '')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
           
            user_profile = UserProfile.objects.get(user=user)
            user_profile.delete()
            user.delete()
            logout(request)
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('project:home')  
        else:
           
            error_message = 'Invalid password. Please try again.'

  
    return render(request, 'profile/delete_account.html', {'error_message': error_message})
 
def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account:profile')  
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        
    return render(request, 'profile/userUpdate.html', {'user_form': user_form, 'profile_form': profile_form})

