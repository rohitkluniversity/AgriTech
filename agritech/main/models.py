from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Language Choices
LANGUAGE_CHOICES = (
    ('en', _('English')),
    ('hi', _('Hindi')),
    ('ta', _('Tamil')),
    ('te', _('Telugu')),
    ('mr', _('Marathi')),
    ('bn', _('Bengali')),
)

# User Profile
class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('seller', _('Seller')),
        ('buyer', _('Buyer')),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    preferred_language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    profile_picture = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

# Base Content Model
class BaseContent(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

# Government Scheme
class GovernmentScheme(BaseContent):
    eligibility_criteria = models.TextField()
    benefits = models.TextField()
    application_process = models.TextField()
    contact_information = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    featured = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

# Farming Practice
class FarmingPractice(BaseContent):
    PRACTICE_TYPE_CHOICES = (
        ('organic', _('Organic Farming')),
        ('fish', _('Fish Farming')),
        ('mountain', _('Mountain Farming')),
        ('livestock', _('Livestock Farming')),
        ('hydroponics', _('Hydroponics')),
        ('other', _('Other')),
    )
    
    practice_type = models.CharField(max_length=20, choices=PRACTICE_TYPE_CHOICES)
    implementation_guide = models.TextField()
    benefits = models.TextField()
    success_stories = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.get_practice_type_display()})"

# Agricultural Technology
class AgriculturalTechnology(BaseContent):
    implementation_cost = models.DecimalField(max_digits=10, decimal_places=2)
    usage_instructions = models.TextField()
    supplier_information = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

# Marketplace Category
class MarketplaceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Marketplace Product
class MarketplaceProduct(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(MarketplaceCategory, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.seller.username}"

# Order
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(MarketplaceProduct, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.buyer.username}"

# Educational Resource
class EducationalResource(BaseContent):
    RESOURCE_TYPE_CHOICES = (
        ('article', _('Article')),
        ('video', _('Video')),
        ('document', _('Document')),
        ('research', _('Research Paper')),
        ('case_study', _('Case Study')),
        ('training', _('Training Material')),
    )
    
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    resource_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"

# Blog Category
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Blog Tag
class BlogTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Blog Post
class BlogPost(BaseContent):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(BlogTag, related_name='posts', blank=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)
    image_url = models.URLField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

# Blog Comment
class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
