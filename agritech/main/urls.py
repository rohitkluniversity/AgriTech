from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Government Schemes
    path('schemes/', views.schemes_list, name='schemes_list'),
    path('schemes/<slug:slug>/', views.scheme_detail, name='scheme_detail'),
    
    # Farming Practices
    path('farming-practices/', views.practices_list, name='practices_list'),
    path('farming-practices/<slug:slug>/', views.practice_detail, name='practice_detail'),
    
    # Agricultural Technologies
    path('technologies/', views.technologies_list, name='technologies_list'),
    path('technologies/<slug:slug>/', views.technology_detail, name='technology_detail'),
    
    # Marketplace
    path('marketplace/', views.marketplace_list, name='marketplace_list'),
    path('marketplace/<int:product_id>/', views.marketplace_detail, name='marketplace_detail'),
    path('marketplace/create-listing/', views.create_listing, name='create_listing'),
    
    # Educational Resources
    path('educational-resources/', views.educational_list, name='educational_list'),
    path('educational-resources/<slug:slug>/', views.educational_detail, name='educational_detail'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Authentication
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    
    # Search
    path('search/', views.search, name='search'),
]
