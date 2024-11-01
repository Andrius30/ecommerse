from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Product
from django.http import JsonResponse


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
# Product Update
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_edit.html'
    fields = ['name', 'price', 'stock', 'status', 'discount', 'purchased', 'product_img']
    success_url = '/products/'



