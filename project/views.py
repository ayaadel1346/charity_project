from django.shortcuts import render, redirect, get_object_or_404
from project.models import Project, Category
from project.models import UserProfile 
from django.contrib.auth.decorators import login_required
from .models import Category, Project
from .models import Project 
from django.http import HttpResponse
from .models import FeaturedProject
from django.shortcuts import render, redirect, get_object_or_404
from project.models import Project, Category
from project.models import UserProfile 
from django.contrib.auth.decorators import login_required
from .models import Category, Project
from .models import Project 
from django.http import HttpResponse
from .models import Project, FeaturedProject

@login_required
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
    featured_projects = Project.objects.filter(featured_project__is_featured=True)
    newest_featured_projects = FeaturedProject.newest_featured_projects()

    categories = Category.objects.all() 
    
    if nearby_projects is not None:
        nearby_projects = [project for project in nearby_projects if not project.is_cancelled and project.progress_percentage != 100][:5]
    if top_projects is not None:
        top_projects = [project for project in top_projects if not project.is_cancelled and project.progress_percentage != 100][:5]
    
    return render(request, 'home.html', {'projects': top_projects, 'nearby_projects': nearby_projects, 'categories': categories,'newest_featured_projects': newest_featured_projects})


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    try:
        projects_query = Project.objects.filter(category=category)
        projects = [project for project in projects_query if not project.is_cancelled and project.progress_percentage != 100]
    except Exception as e:
       
        projects = []

    return render(request, 'category_detail.html', {'category': category, 'projects': projects})




from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Project, Tag, ProjectPicture

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(creator=request.user)
          
            return redirect('project:home')  
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})
