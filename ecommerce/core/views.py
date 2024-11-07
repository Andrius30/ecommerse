from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import *


@login_required(login_url='/login/')
def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'index.html', context)

