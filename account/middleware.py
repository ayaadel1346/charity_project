from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from project.models import UserProfile

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'username' in request.session:
            request.user = User.objects.get(username=request.session['username'])

        if not request.user.is_authenticated and request.path not in [reverse('account:login'), reverse('account:register')]:
            return HttpResponseRedirect(reverse('account:login'))

        response = self.get_response(request)
        return response
