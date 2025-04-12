from django.contrib import admin
from .models import (
    UserProfile, GovernmentScheme, FarmingPractice, AgriculturalTechnology,
    MarketplaceCategory, MarketplaceProduct, Order, EducationalResource,
    BlogCategory, BlogTag, BlogPost, BlogComment
)

# User Profile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number', 'preferred_language')
    list_filter = ('user_type', 'preferred_language')
    search_fields = ('user__username', 'phone_number')

# Government Scheme
@admin.register(GovernmentScheme)
class GovernmentSchemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'featured', 'created_at')
    list_filter = ('language', 'featured')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

# Farming Practice
@admin.register(FarmingPractice)
class FarmingPracticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'practice_type', 'language', 'created_at')
    list_filter = ('practice_type', 'language')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

# Agricultural Technology
@admin.register(AgriculturalTechnology)
class AgriculturalTechnologyAdmin(admin.ModelAdmin):
    list_display = ('title', 'implementation_cost', 'language', 'created_at')
    list_filter = ('language',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

# Marketplace Category
@admin.register(MarketplaceCategory)
class MarketplaceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Marketplace Product
@admin.register(MarketplaceProduct)
class MarketplaceProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'quantity', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'seller__username')

# Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('buyer__username', 'product__title')

# Educational Resource
@admin.register(EducationalResource)
class EducationalResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'language', 'created_at')
    list_filter = ('resource_type', 'language')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

# Blog Category
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# Blog Tag
@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# Blog Post
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'language', 'featured', 'created_at')
    list_filter = ('category', 'language', 'featured', 'tags')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)

# Blog Comment
@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content', 'post__title')
