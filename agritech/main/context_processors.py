from django.conf import settings
from .models import MarketplaceCategory, BlogCategory, BlogTag

def language_processor(request):
    """
    Context processor that adds language choices to the context.
    """
    return {'LANGUAGES': settings.LANGUAGES}

def categories_processor(request):
    """
    Context processor that adds marketplace categories and blog categories to the context.
    """
    marketplace_categories = MarketplaceCategory.objects.all()
    blog_categories = BlogCategory.objects.all()
    popular_tags = BlogTag.objects.all()[:10]  # Get 10 most popular tags
    
    return {
        'marketplace_categories': marketplace_categories,
        'blog_categories': blog_categories,
        'popular_tags': popular_tags
    }
