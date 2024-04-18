from django.contrib.auth.decorators import login_required
from project.models import UserProfile 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import UserProfileForm, UserForm
from .forms import AddUserForm, AddUserProfileForm
from project.models import Category
from .forms import CategoryUpdateForm
from .forms import AddCategoryForm
from project.models import FeaturedProject, Project
from .forms import FeaturedProjectForm

@login_required
def admin_panel(request):
    return render(request, 'base_admin.html')


def user_profile_view(request):
    user_profiles = UserProfile.objects.all()
    return render(request, 'user_profile.html', {'user_profiles': user_profiles})





def delete_profile(request, profile_id):
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(id=profile_id)
            user_id = profile.user.id
            User.objects.filter(id=user_id).delete()
            profile.delete()
        except UserProfile.DoesNotExist:
            pass  
    return redirect('admin_panel:user_profile')







def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data.get('email')
            if User.objects.exclude(pk=user_id).filter(email=email).exists():
                user_form.add_error('email', 'This email is already in use. Please choose another one.')
            else:
                user_form.save()
                profile_form.save()
                return redirect('admin_panel:user_profile') 
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        
    return render(request, 'user_update_form.html', {'user_form': user_form, 'profile_form': profile_form})




def add_user(request):
    if request.method == 'POST':
        user_form = AddUserForm(request.POST)
        profile_form = AddUserProfileForm(request.POST, request.FILES)  

        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                user_form.add_error('email', 'This email is already in use. Please choose another one.')
            else:
                user_instance = user_form.save(commit=False)
                user_instance.set_password(user_form.cleaned_data["password"])
                user_instance.save()

                profile_instance = profile_form.save(commit=False)
                profile_instance.user = user_instance
                
                if 'image' in request.FILES:
                    profile_instance.image = request.FILES['image']
                    
                profile_instance.save()
                
                return redirect('admin_panel:user_profile')
    else:
        user_form = AddUserForm()
        profile_form = AddUserProfileForm()
        
    return render(request, 'add_user_form.html', {'user_form': user_form, 'profile_form': profile_form})




def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})





def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
        except Category.DoesNotExist:
            pass 
    return redirect('admin_panel:category_list')







def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryUpdateForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:category_list')
    else:
        form = CategoryUpdateForm(instance=category)
    return render(request, 'update_category.html', {'form': form})





def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:category_list') 
    else:
        form = AddCategoryForm()
    return render(request, 'add_category_form.html', {'form': form})







def featured_projects(request):
    featured_projects = FeaturedProject.objects.all()
    return render(request, 'featured_project.html', {'featured_projects': featured_projects})



def delete_featured_project(request, project_id):
    featured_project = FeaturedProject.objects.get(project_id=project_id)
    if request.method == 'POST':
        featured_project.delete()
        return redirect('admin_panel:featured_projects')
    return render(request, 'featured_project.html', {'featured_projects': FeaturedProject.objects.all()})





def update_featured_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    featured_project = get_object_or_404(FeaturedProject, project=project)
    if request.method == 'POST':
        form = FeaturedProjectForm(request.POST, instance=featured_project)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:featured_projects')
    else:
        form = FeaturedProjectForm(instance=featured_project)
    return render(request, 'featured_project_update_form.html', {'form': form})



def add_featured_project(request):
    if request.method == 'POST':
        form = FeaturedProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:featured_projects') 
    else:
        form = FeaturedProjectForm()
    return render(request, 'add_featured_project.html', {'form': form})
