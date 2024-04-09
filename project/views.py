from django.shortcuts import render
from project.models import Project, Category
from project.models import UserProfile 

def home(request):
    user_country = None
    nearby_projects = None
    username = request.session.get('username')
    
    if username:
        try:
            user_profile = UserProfile.objects.get(user__username=username)
            user_country = user_profile.country
          
        except UserProfile.DoesNotExist:
            pass
   
    if user_country:

        nearby_projects = Project.objects.filter(country=user_country) 
    
    top_projects = Project.top_rated_projects()
    
    categories = Category.objects.all() 
    
    if nearby_projects is not None:
        nearby_projects = [project for project in nearby_projects if not project.is_cancelled and project.progress_percentage != 100][:5]
    if top_projects is not None:
        top_projects = [project for project in top_projects if not project.is_cancelled and project.progress_percentage != 100][:5]
    
    return render(request, 'home.html', {'projects': top_projects, 'nearby_projects': nearby_projects, 'categories': categories})
