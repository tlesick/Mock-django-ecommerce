from django.shortcuts import render, redirect
from apps.User.models import *
from apps.Product.models import *
from apps.Cart.models import *
from apps.Address.models import *
from apps.Order.models import *
from .models import *
import stripe
from e_commerce import settings
from django.http import HttpResponse
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    # if the user is logged in
    try:
        user = User.objects.get(id = request.session['user_id'])
        cart = Cart.objects.filter(user= user.id)
        # grab the preferred address which will be the only 1
        address = Address.objects.get(user = user.id, preference= 1)
        rtotal = 0
        for i in cart:
            rtotal +=float(i.product.price) * float(i.quantity)
        total = '${:,.2f}'.format(rtotal)


        
        content = {
            'user': user,
            'cart': cart,
            'address': address,
            'total': total,
            'stripe_key': settings.STRIPE_PUBLIC_KEY,
        }
        

        return render(request, 'order/checkout.html', content)
    except:
        content = {
            'error': ["Please Login to Checkout"]
        }
        return render(request, 'user/registration.html', content)
     

#     Set your secret key: remember to change this to your live secret key in production
# # See your keys here: https://dashboard.stripe.com/account/apikeys  

# they need to select the address that they are going to use
# need a method for which address is selected
        # lets the keep the order number simple, but just getting the last element in the orderhistory, increamenting
        # it by one and using that number for the entire order
def processPayment(request):
    user = User.objects.get(id = request.session['user_id'])
    cart = Cart.objects.filter(user=user.id)
    
    rtotal = 0

    for i in cart:
        rtotal +=float(i.product.price) * float(i.quantity)
    # rtotal *= 100
    

    # token = request.POST.get['stripeToken']
    # try:
      
    #     charge = stripe.Charge.create(
    #     amount  = int(rtotal),
    #     currency = "usd",
    #     source = token,
    #     description = "Test",
    #     )


        # stripe.Charge.retrieve(charge.id)
    Order.objects.new_order(user)
    return redirect('/')

    # except stripe.error.CardError as e:
    #     # Since it's a decline, stripe.error.CardError will be caught
    #     body = e.json_body
    #     err  = body.get('error', {})
    #     print ("Status is: {}".format(e.http_status))
    #     print ("Type is: {}".format(err.get('type')))
    #     print ("Code is: {}".format(err.get('code')))
    #     # param is '' in this case
    #     print ("Param is: {}" .format(err.get('param')))
    #     print ("Message is: {}".format(err.get('message')))
    #     return redirect('/order/checkout')
    # except stripe.error.RateLimitError as e:
    # # Too many requests made to the API too quickly
    #     pass
    #     return ('/order/checkout')
    # except stripe.error.InvalidRequestError as e:
    #     body = e.json_body
    #     err  = body.get('error', {})
    #     print ("Status is: {}".format(e.http_status))
    #     print ("Type is: {}".format(err.get('type')))
    #     print ("Code is: {}".format(err.get('code')))
    #     # param is '' in this case
    #     print ("Param is: {}" .format(err.get('param')))
    #     print ("Message is: {}".format(err.get('message')))
    #     return ('/order/checkout')
    # except stripe.error.AuthenticationError as e:
    #     # Authentication with Stripe's API failed
    #     # (maybe you changed API keys recently)
    #     return ('/order/checkout')
    # except stripe.error.APIConnectionError as e:
    #     return ('/order/checkout')
    # except stripe.error.StripeError as e:
    #     # Display a very generic error to the user, and maybe send
    #     # yourself an email
    #     return('/order/checkout')
    # except Exception as e:
    #     # Something else happened, completely unrelated to Stripe
        # return ('/order/checkout')
# watch out for naming the same name

def show(request):
    user = User.objects.get(id= request.session['user_id'])
    orders = Order.objects.filter(user= user.id)  
    
    order_package = {}
    count = 0
    # package containing the subtotals
    
    for i in orders:
        p_subtotals = []
        order_package[count] = [i]
        products = []
        quantities = []
    # go through the array in orders i.products
        for j in i.products:
            find_product = Product.objects.get(id=j)
            products.append(find_product)
        order_package[count].append(products)
    # go through the array in orders i.quantity
        for key,value in enumerate(i.quantity):
            subtotal = 0
            subtotal = float(products[key].price) * float(value)
            subtotal = '${:,.2f}'.format(subtotal)
            quantities.append(value)
            p_subtotals.append(subtotal)
        order_package[count].append(quantities)
        order_package[count].append(p_subtotals)
        count += 1    
    content = {
        'user': user,
        'orders':order_package,
    }
    
   
    
    return render(request, 'order/show.html', content)
