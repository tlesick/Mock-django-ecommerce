from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from apps.Address.models import *
from apps.Cart.models import *
from apps.Product.models import *

# Brings up the Registration page
def registration(request):
    return render(request, 'user/registration.html')

# Creates a new User
def register(request):
    new_user = User.objects.register(request.POST)

    # if incorrect information was entered
    if 'error_msg' in new_user:
        for e in new_user['error_msg']:
            messages.error(request, e)
        return redirect('/user/registration')
        
    else:
        # if the user logged in first
        try:
            cart = request.session['cart']
            if cart is None:
                print ('no cart items')
                request.session['user_id'] = new_user['new_user'].id
                return redirect ('/address/registration')
            # if the user put items in the cart before logging in
            else:
                print ('items in cart')
                current_cart = cart
                for i in current_cart:
                    product_instance = Product.objects.get(id = i['product'])
                    update_cart = Cart.objects.addToCart(new_user['new_user'], product_instance, i['quantity'])
                request.session.clear()
                request.session['user_id'] = new_user['new_user'].id
                return redirect('/address/registration')
        except:
            request.session['user_id'] = new_user['new_user'].id
            return redirect ('/address/registration')


def login(request): 
    # checks if the login credentials are correct
    new_user = User.objects.login(request.POST)
    if 'err_messages' in new_user:
        for e in new_user['err_messages']:
            messages.error(request, e)
        return redirect('/user/registration')
    else:
        # checks if the user had a cart open 
        try:
            print ('checking the cart')
            current_cart = request.session['cart']
            
            # get the user from database
        
            user = User.objects.get(id = new_user['logged_user'].id)
            for index, value in enumerate(current_cart):
                product = Product.objects.get(id= value['product'])
                Cart.objects.login_add(user.id, product.id, value['quantity']) 
            request.session.clear()
            request.session['user_id']= new_user['logged_user'].id
            return redirect('/')
            # if the user does not have session cart
        except:
            request.session.clear()
            request.session['user_id'] = new_user['logged_user'].id
            return redirect('/')


def edit_page(request):
    user = User.objects.get(id = request.session['user_id'])
    content = {
        'user': user,
    }
    return render(request, 'user/edit.html', content)


def edit(request):
    user = User.objects.get(id = request.session['user_id'])
    update_user = User.objects.edit(request.POST, user.id)
    if 'error_messages' in update_user:
        for e in update_user['error_messages']:
            messages.error(request, e)
        print ('view 4')
        return redirect('user/edit')
    else:
        print ('view 5')
        return redirect('/user/show')


def logout(request):
    request.session.clear()
    return redirect('/')
    

def show(request):
    if request.session['user_id'] is None:
        return redirect('/user/registration')
    else:
        user = User.objects.get(id= request.session['user_id'])
        try:
            address = Address.objects.filter(user= user.id)
            content = {
                'user': user,
                'address': address,
            }
            return render(request, 'user/show.html' , content)
        except:
            content = {
                'user': user,
            }
            return render(request, 'user/show.html', content)
        