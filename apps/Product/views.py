from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.User.models import *
import django.contrib.postgres


def index(request):
    try: 
        products = Products.objects.all()
        logged_user = User.objects.get(id = request.session['user_id'])
        content = {
            'user':logged_user,
            'products': products,
        }
        return render(request, 'product/index.html', content)
    except:
     
        return render(request, 'product/index.html')

def search(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.POST['search'] is None:
        products = Product.objects.all()
        content ={
            'products':products,
            'user': user,
        }
        return render(request, 'product/search.html', content)
    else:
        search = request.POST['search']
        title = Product.objects.filter(title__icontains = search)
        category = Product.objects.filter(category__icontains = search)
        description = Product.objects.filter(description__icontains = search)
        products =  title.union(category, description)
        content = {
            'products': products,
        }
        return render(request, 'product/search.html', content)

def show(request, id):
    product = Product.objects.get(id = id)
    content = {
        'product':product,
    }
    return render(request, 'product/show.html', content)