from django.contrib.sessions.models import Session
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
          
            request.session['username'] = user.username
            
            return redirect('project:home')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
