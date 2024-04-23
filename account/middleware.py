import logging
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
       
       
        if 'user_id' in request.session:
            try:
                request.user = User.objects.get(pk=request.session['user_id'])
            except User.DoesNotExist:
                request.user = None

       
        if request.user and request.user.is_authenticated:
           
            if not request.user.is_superuser and request.path.startswith('/admin_panel/'):
                
                return HttpResponseRedirect(reverse('account:login'))
        else:
           
            if request.path not in [reverse('account:login'), reverse('account:register')]:
                
                return HttpResponseRedirect(reverse('account:login'))

        response = self.get_response(request)
        return response
