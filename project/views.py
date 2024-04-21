from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from project.forms import *
from project.models import *


def home(request):
    user_country = None
    nearby_projects = None
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user_profile = UserProfile.objects.get(user__pk=user_id)
            user_country = user_profile.country
        except UserProfile.DoesNotExist:
            pass
   
    if user_country:
        nearby_projects = Project.objects.filter(country=user_country) 
    
    top_projects = Project.top_rated_projects()
    featured_projects = FeaturedProject.objects.filter(is_featured=True)
    newest_featured_projects = FeaturedProject.newest_featured_projects()

    categories = Category.objects.all() 
    
    if nearby_projects is not None:
        nearby_projects = [project for project in nearby_projects if not project.is_cancelled and project.progress_percentage != 100][:5]
    if top_projects is not None:
        top_projects = [project for project in top_projects if not project.is_cancelled and project.progress_percentage != 100][:5]
    
    return render(request, 'homepage/home.html', {'projects': top_projects, 'nearby_projects': nearby_projects, 'categories': categories,'newest_featured_projects': newest_featured_projects})




def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    try:
        projects_query = Project.objects.filter(category=category)
        projects = [project for project in projects_query if not project.is_cancelled and project.progress_percentage != 100]
    except Exception as e:
        projects = []

    return render(request, 'homepage/category_detail.html', {'category': category, 'projects': projects})




def search_projects(request):
    query = request.GET.get('query')

    projects = Project.objects.filter(title__icontains=query) | Project.objects.filter(tags__name__icontains=query)

    return render(request, 'homepage/search_results.html', {'projects': projects})





def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(creator=request.user)
            return redirect('project:home')  
    else:
        form = ProjectForm()
    return render(request, 'createproject/create_project.html', {'form': form})
