from django.urls import path
from . import views
from .views import ProductUpdateView, ProductDeleteView, add_category, add_subcategory, add_product

app_name = 'products'
urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products_list'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('add_category/', add_category, name='add_category'),
    path('add_subcategory/', add_subcategory, name='add_subcategory'),
    path('add_product/', add_product, name='add_product'),
]