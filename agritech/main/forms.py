from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import (
    UserProfile, MarketplaceProduct, Order, BlogComment, LANGUAGE_CHOICES
)

# User Registration Form
class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('seller', _('Seller')),
        ('buyer', _('Buyer')),
    )
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, label=_('User Type'))
    phone_number = forms.CharField(max_length=15, required=False, label=_('Phone Number'))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label=_('Address'))
    preferred_language = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=True, label=_('Preferred Language'))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type', 'phone_number', 'address', 'preferred_language']

# Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}),
        label=_('Username')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}),
        label=_('Password')
    )

# Profile Edit Form
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'preferred_language', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

# Marketplace Product Form
class MarketplaceProductForm(forms.ModelForm):
    class Meta:
        model = MarketplaceProduct
        fields = ['category', 'title', 'description', 'price', 'quantity', 'location', 'image_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

# Order Form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'shipping_address']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
        }

# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': _('Add your comment here...')}),
        }

# Search Form
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='', required=True, 
                           widget=forms.TextInput(attrs={'placeholder': _('Search...')}))
    category = forms.ChoiceField(choices=[
        ('all', _('All Categories')),
        ('schemes', _('Government Schemes')),
        ('practices', _('Farming Practices')),
        ('technologies', _('Agricultural Technologies')),
        ('marketplace', _('Marketplace')),
        ('educational', _('Educational Resources')),
        ('blog', _('Blog')),
    ], required=False, initial='all')
