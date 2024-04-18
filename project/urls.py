from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('create/', views.create_project, name='create_project'),
     
    
]
