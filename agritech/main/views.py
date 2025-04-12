from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import (
    UserProfile, GovernmentScheme, FarmingPractice, AgriculturalTechnology,
    MarketplaceCategory, MarketplaceProduct, Order, EducationalResource,
    BlogCategory, BlogTag, BlogPost, BlogComment
)
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm, MarketplaceProductForm,
    OrderForm, CommentForm, SearchForm
)

# Home page view
def home(request):
    # Featured items for carousel
    schemes = GovernmentScheme.objects.filter(featured=True)[:5]
    blog_posts = BlogPost.objects.filter(featured=True)[:5]
    
    # Recent items sections
    recent_practices = FarmingPractice.objects.order_by('-created_at')[:4]
    recent_technologies = AgriculturalTechnology.objects.order_by('-created_at')[:4]
    recent_resources = EducationalResource.objects.order_by('-created_at')[:4]
    recent_products = MarketplaceProduct.objects.order_by('-created_at')[:8]
    
    context = {
        'schemes': schemes,
        'blog_posts': blog_posts,
        'recent_practices': recent_practices,
        'recent_technologies': recent_technologies,
        'recent_resources': recent_resources,
        'recent_products': recent_products,
    }
    
    return render(request, 'home.html', context)

# Government Schemes
def schemes_list(request):
    schemes = GovernmentScheme.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(schemes, 10)
    page = request.GET.get('page')
    
    try:
        schemes = paginator.page(page)
    except PageNotAnInteger:
        schemes = paginator.page(1)
    except EmptyPage:
        schemes = paginator.page(paginator.num_pages)
    
    context = {
        'schemes': schemes,
    }
    
    return render(request, 'schemes/index.html', context)

def scheme_detail(request, slug):
    scheme = get_object_or_404(GovernmentScheme, slug=slug)
    
    context = {
        'scheme': scheme,
    }
    
    return render(request, 'schemes/detail.html', context)

# Farming Practices
def practices_list(request):
    practices = FarmingPractice.objects.all().order_by('-created_at')
    
    # Filter by practice type if specified
    practice_type = request.GET.get('type')
    if practice_type:
        practices = practices.filter(practice_type=practice_type)
    
    # Pagination
    paginator = Paginator(practices, 10)
    page = request.GET.get('page')
    
    try:
        practices = paginator.page(page)
    except PageNotAnInteger:
        practices = paginator.page(1)
    except EmptyPage:
        practices = paginator.page(paginator.num_pages)
    
    context = {
        'practices': practices,
        'practice_type': practice_type,
        'practice_types': dict(FarmingPractice.PRACTICE_TYPE_CHOICES),
    }
    
    return render(request, 'farming_practices/index.html', context)

def practice_detail(request, slug):
    practice = get_object_or_404(FarmingPractice, slug=slug)
    
    context = {
        'practice': practice,
    }
    
    return render(request, 'farming_practices/detail.html', context)

# Agricultural Technologies
def technologies_list(request):
    technologies = AgriculturalTechnology.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(technologies, 10)
    page = request.GET.get('page')
    
    try:
        technologies = paginator.page(page)
    except PageNotAnInteger:
        technologies = paginator.page(1)
    except EmptyPage:
        technologies = paginator.page(paginator.num_pages)
    
    context = {
        'technologies': technologies,
    }
    
    return render(request, 'technologies/index.html', context)

def technology_detail(request, slug):
    technology = get_object_or_404(AgriculturalTechnology, slug=slug)
    
    context = {
        'technology': technology,
    }
    
    return render(request, 'technologies/detail.html', context)

# Marketplace
def marketplace_list(request):
    products = MarketplaceProduct.objects.all().order_by('-created_at')
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    categories = MarketplaceCategory.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    }
    
    return render(request, 'marketplace/index.html', context)

def marketplace_detail(request, product_id):
    product = get_object_or_404(MarketplaceProduct, id=product_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.product = product
            order.total_price = product.price * order.quantity
            # Calculate commission (e.g. 5% of total price)
            order.commission = order.total_price * 0.05
            if order.quantity <= product.quantity:
                order.save()
                
                # Update product quantity
                product.quantity -= order.quantity
                product.save()
                
                messages.success(request, _('Order placed successfully!'))
                return redirect('marketplace_list')
            else:
                messages.error(request, _('Not enough quantity available.'))
    else:
        form = OrderForm()
    
    context = {
        'product': product,
        'form': form,
    }
    
    return render(request, 'marketplace/detail.html', context)

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = MarketplaceProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, _('Product listed successfully!'))
            return redirect('marketplace_list')
    else:
        form = MarketplaceProductForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'marketplace/create_listing.html', context)

# Educational Resources
def educational_list(request):
    resources = EducationalResource.objects.all().order_by('-created_at')
    
    # Filter by resource type if specified
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    
    # Pagination
    paginator = Paginator(resources, 10)
    page = request.GET.get('page')
    
    try:
        resources = paginator.page(page)
    except PageNotAnInteger:
        resources = paginator.page(1)
    except EmptyPage:
        resources = paginator.page(paginator.num_pages)
    
    context = {
        'resources': resources,
        'resource_type': resource_type,
        'resource_types': dict(EducationalResource.RESOURCE_TYPE_CHOICES),
    }
    
    return render(request, 'educational/index.html', context)

def educational_detail(request, slug):
    resource = get_object_or_404(EducationalResource, slug=slug)
    
    context = {
        'resource': resource,
    }
    
    return render(request, 'educational/detail.html', context)

# Blog
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    
    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug)
        posts = posts.filter(category=category)
    
    # Filter by tag if specified
    tag_slug = request.GET.get('tag')
    if tag_slug:
        tag = get_object_or_404(BlogTag, slug=tag_slug)
        posts = posts.filter(tags=tag)
    
    # Pagination
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    categories = BlogCategory.objects.all()
    tags = BlogTag.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'selected_category': category_slug,
        'selected_tag': tag_slug,
    }
    
    return render(request, 'blog/index.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, _('Comment added successfully!'))
            return HttpResponseRedirect(reverse('blog_detail', args=[slug]))
    else:
        form = CommentForm()
    
    # Related posts (same category)
    related_posts = BlogPost.objects.filter(category=post.category).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'related_posts': related_posts,
    }
    
    return render(request, 'blog/detail.html', context)

# User Authentication
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                preferred_language=form.cleaned_data['preferred_language']
            )
            
            # Log the user in
            login(request, authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            ))
            
            messages.success(request, _('Registration successful!'))
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/register.html', context)

@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            # Update user data
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            # Update profile data
            form.save()
            
            messages.success(request, _('Profile updated successfully!'))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    # Get user orders if any
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    
    # Get user products if seller
    products = []
    if user_profile.user_type == 'seller':
        products = MarketplaceProduct.objects.filter(seller=request.user).order_by('-created_at')
    
    context = {
        'form': form,
        'user_profile': user_profile,
        'orders': orders,
        'products': products,
    }
    
    return render(request, 'accounts/profile.html', context)

# Search
def search(request):
    form = SearchForm(request.GET)
    results = []
    query = request.GET.get('query', '')
    category = request.GET.get('category', 'all')
    
    if query:
        if category == 'all' or category == 'schemes':
            schemes = GovernmentScheme.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            results.extend([{'type': 'scheme', 'obj': scheme} for scheme in schemes])
        
        if category == 'all' or category == 'practices':
            practices = FarmingPractice.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            results.extend([{'type': 'practice', 'obj': practice} for practice in practices])
        
        if category == 'all' or category == 'technologies':
            technologies = AgriculturalTechnology.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            results.extend([{'type': 'technology', 'obj': tech} for tech in technologies])
        
        if category == 'all' or category == 'marketplace':
            products = MarketplaceProduct.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            results.extend([{'type': 'product', 'obj': product} for product in products])
        
        if category == 'all' or category == 'educational':
            resources = EducationalResource.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            results.extend([{'type': 'resource', 'obj': resource} for resource in resources])
        
        if category == 'all' or category == 'blog':
            posts = BlogPost.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            results.extend([{'type': 'post', 'obj': post} for post in posts])
    
    context = {
        'form': form,
        'results': results,
        'query': query,
        'category': category,
    }
    
    return render(request, 'search_results.html', context)
