from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('delete_profile/<int:profile_id>/', views.delete_profile, name='delete_profile'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('add_user/', views.add_user, name='add_user'),
    path('categories/', views.category_list, name='category_list'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('update_category/<int:category_id>/', views.update_category, name='update_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('featured-projects/', views.featured_projects, name='featured_projects'),
    path('delete-featured-project/<int:project_id>/', views.delete_featured_project, name='delete_featured_project'),
    path('featured-projects/<int:project_id>/update/', views.update_featured_project, name='update_featured_project'),
    path('add_featured_project/', views.add_featured_project, name='add_featured_project'),


   
]