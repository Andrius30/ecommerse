from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Product, Category
from django.db.models import Count
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib import messages

class ProductsListView(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_category'] = ((Category.objects
                                        .filter(parent_category__isnull=True)
                                        .prefetch_related('subcategories'))
                                       .annotate(product_count=Count('product')))
        return context


# Product Update
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_edit.html'
    fields = ['name', 'price', 'stock', 'status', 'discount', 'purchased', 'product_img', 'category']
    success_url = '/products/'


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    success_url = '/products/'


def add_product(request):
    categories = Category.objects.filter(parent_category=None)
    product_status_choices = Product.PRODUCT_STATUS  # Product status choices

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('products:products_list')  # Adjust redirect if needed
        else:
            print(form.errors)  # Print form errors to debug issues
    else:
        form = ProductForm()

    context = {
        'form': form,
        'product_category': categories,
        'product_status_choices': product_status_choices
    }
    return render(request, 'products/add_product.html', context)


def add_category(request):
    product_category = Category.objects.all()
    context = {'product_category': product_category}

    if request.method == 'POST':
        name = request.POST.get('text')
        slug = request.POST.get('slug')
        short_description = request.POST.get('sortdescription')
        full_description = request.POST.get('fulldescription')
        group_tag = request.POST.get('group_tag')
        parent_category_id = request.POST.get('parent_category')

        # Get the parent category if provided
        parent_category = Category.objects.get(pk=parent_category_id) if parent_category_id else None

        # Create the category with or without a parent
        Category.objects.create(
            name=name,
            slug=slug,
            short_description=short_description,
            full_description=full_description,
            group_tag=group_tag,
            parent_category=parent_category  # self-referential field in model
        )

        return redirect('products:add_category')  # Adjust redirect as needed

    return render(request, 'products/add_category.html', context)


def add_subcategory(request):
    product_category = Category.objects.filter(parent_category__isnull=True)  # Categories for dropdown

    if request.method == 'POST':
        name = request.POST.get('text')
        slug = request.POST.get('slug')
        short_description = request.POST.get('sortdescription')
        full_description = request.POST.get('fulldescription')
        group_tag = request.POST.get('group_tag')
        parent_category_id = request.POST.get('parent_category')

        parent_category = Category.objects.get(pk=parent_category_id) if parent_category_id else None
        Category.objects.create(
            name=name,
            slug=slug,
            short_description=short_description,
            full_description=full_description,
            group_tag=group_tag,
            parent_category=parent_category
        )
        return redirect('products:add_category')

    context = {'product_category': product_category}
    return render(request, 'products/add_subcategory.html', context)


