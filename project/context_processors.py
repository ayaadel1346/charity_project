from project.models import UserProfile

def user_info(request):
  
    username = None
    user_profile = None

    if 'username' in request.session:
        username = request.session['username']

        try:
            user_profile = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            pass
    
    return {
        'username': username,
        'user_profile': user_profile,
    }
