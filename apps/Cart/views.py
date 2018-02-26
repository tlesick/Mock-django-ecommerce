from django.shortcuts import render, redirect
from .models import *
from apps.Product.models import *
from apps.User.models import *


def update(request, product_id):
    # if the user is logged in:
    try:

        user = User.objects.get(id = request.session['user_id'])
        product = Product.objects.get(id = product_id)
        quantity = request.POST['quantity']
        cart = Cart.objects.add(product, quantity, user)
        print("User logged in and new item added to cart")
        return redirect('/cart/show')
    # if the user is not logged in:
    except:
        print ("User not in session")       
        product = Product.objects.get(id = product_id)
        quantity = request.POST['quantity']
        
        # if the user is not logged in
        try: 
            current_cart = request.session['cart']
            print ("Anon-user has cart")
             # if the user is not logged in and already has items in the cart
            if len(current_cart) > 0:
                print ('cart isnt empty')
                for index,i in enumerate(current_cart): 
                    # if same product already exists in the cart increase quantity
                    if i['product'] == product.id:
                        i['quantity'] = int(i['quantity']) + int(quantity)
                        # the previous subtotal doesn't matter
                        i['subtotal'] = int(i['quantity']) * int(product.price)
                        request.session['cart'] = current_cart
                        print ('anon-user has cart, has same product, increased quantity')
                        return redirect('/cart/show')
                        # if the entire cart has been searched and the item isn't in cart, append
                    elif (i['product'] != product.id) and index == len(current_cart)-1:
                        subtotal = int(product.price) * int(quantity)
                        add_item = {
                        'product': product.id,
                        'quantity': quantity,
                        'subtotal': subtotal,
                        }
                        current_cart.append(add_item)
                        request.session['cart'] = current_cart
                        print ('anon-user has cart, but new item added')
                        return redirect('/cart/show')
                    else: 
                        # keeps the loop going
                        print ('** incase it breaks here for some reason **')
                        continue
                # if the user is not logged in and does not already ahve items in the cart

            else:
                print ('anon-user has cart that is empty')
                
                subtotal = (float(product.price)) * (float(quantity))
                subtotal = '${:,.2f}'.format(subtotal)
                add_item = [{
                        'product': product.id,
                        'quantity': quantity,
                        'subtotal': subtotal,
                        }]
                request.session['cart'] = add_item
                return redirect('/cart/show')
            # if this is the first item to be added to the cart session:
        except:
            subtotal = float(product.price) * float(quantity)
            add_item = [{
                'product': product.id,
                'quantity': quantity,
                'subtotal': subtotal,
            }]
            request.session['cart'] = add_item
            print ('anon-user has no cart, new cart made with product')
            return redirect('/cart/show')

def show(request):
    #  if the user is logged in
    try:
        logged_user = User.objects.get(id = request.session['user_id'])
        cart= Cart.objects.filter(user = logged_user.id)
        total = 0
        for i in cart:
            total += (float(i.quantity) * float(i.product.price))
        if total != 0:
            total = '${:,.2f}'.format(total)
        
            content = {
                'user':logged_user,
                'cart':cart,
                'total': total,
                }
                
            return render(request, 'cart/show.html', content)
        else:
            content = {
                'user': logged_user,
            }
            return render(request, 'cart/show', content)
        # key=stripe_keys['publishable_key']
    # if the user is not logged in 
    except:
        try:
            print ('user is not logged in')
            current_cart = (request.session['cart']) 
            products = []
            if len(current_cart) > 0:
                total = 0
                for i in current_cart:
                    product_id = i['product'] 
                    product = Product.objects.get(id=product_id)
                    i['product'] = product
                    total += (float(product.price) * float(i['quantity']))

                total = '${:,.2f}'.format(total)

                content = {
                    'total': total,
                    'ns_cart': current_cart,    
                }
                print ('current cart')

                return render(request, "cart/show.html", content)
            else:
                return render(request, 'cart/show.html')
        except:
            print ('user did not have a cart')
            return render(request, 'cart/show.html')

def delete(request, product_id):
    print ('Cart - Delete')
    try:
        current_cart = request.session['cart']
        for index, value in enumerate(current_cart):
            if int(value['product']) == int(product_id):  
                current_cart.pop(index)
            else:      
                continue
        request.session['cart'] = current_cart
        return redirect('/cart/show')
    
    except:
        print ('cart from database')
        user = User.objects.get(id=request.session['user_id'])
        Cart.objects.remove(product_id)
        return redirect('/cart/show')
