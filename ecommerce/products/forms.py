from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'short_description', 'full_description', 'group_tag']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'full_description': forms.Textarea(attrs={'class': 'form-control'}),
            'group_tag': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'short_description', 'full_description', 'price', 'stock', 'status', 'discount', 'product_img', 'category']
        widgets = {
            'status': forms.Select(choices=Product.PRODUCT_STATUS),
            'product_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Product.objects.filter(slug=slug).exists():
            raise forms.ValidationError('This slug is already taken.')
        return slug
