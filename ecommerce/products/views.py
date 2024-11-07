from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Product, Category
from .forms import CategoryForm


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_category'] = Category.objects.all()
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


def add_category(request):
    product_category = Category.objects.all()
    context = {'product_category': product_category}
    if request.method == 'POST':
        name = request.POST.get('text')
        slug = request.POST.get('slug')
        short_description = request.POST.get('sortdescription')
        full_description = request.POST.get('fulldescription')
        group_tag = request.POST.get('group_tag')


        Category.objects.create(
            name=name,
            slug=slug,
            short_description=short_description,
            full_description=full_description,
            group_tag=group_tag)
        return redirect('products:add_category')  # Adjust to your main list view name

    return render(request, 'products/add_category.html', context)