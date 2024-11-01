from django.urls import path
from . import views
from .views import ProductUpdateView

app_name = 'products'
urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products_list'),
    # path('products/delete/<int:product_id>/',views.delete_product,name='delete_product'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit')
]