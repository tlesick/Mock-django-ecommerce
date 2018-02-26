from django.db import models
from apps.Product import models as Product_models
from apps.User import models as User_models



class CartManager(models.Manager):
    def login_add(self, user, product, quantity):
        obj_user = User_models.User.objects.get(id = user)
        obj_product = Product_models.Product.objects.get(id = product)
        try: 
            checkinCart = Cart.objects.get(product = product, user= user)
            if bool(checkinCart):
                print ('item already in cart')
                checkinCart.quantity = checkinCart.quantity + float(quantity) 
                checkinCart.subtotal = checkinCart.quantity * float(checkinCart.product.price)
                checkinCart.save()
                return 
        # if a new item is being added to the cart
        except:
            
            find_product = Product_models.Product.objects.get(id= product)
            find_user = User_models.User.objects.get(id=user)
            subtotal = float(find_product.price) * float(quantity)
            cart = Cart.objects.create(
                        product= find_product, 
                        user= find_user, 
                        quantity=quantity,
                        subtotal= subtotal)
            print ('new item added to cart')
            return 
    # data is coming back as objects
    def add(self, product, quantity, user):
        # check if the item already exists in the cart
        try:
            print ('model 1-1')
            checkincart = Cart.objects.get(product = product.id, user= user.id) 
            print ('model 1-2')
            if len(checkincart) > 1:
                print ('model 1-3')
                checkincart.quantity += quantity
                print ('model 1-4')
                checkincart.save()
                print ('model 1-5')
                return
        except:
            print ('model 2-1')
            print (product)
            print (product.price)
            print (quantity)
            subtotal = float(product.price) * float(quantity)
            print ('model 2-2')
            new_item = Cart.objects.create(
                product = product,
                user = user,
                quantity = quantity,
                subtotal = subtotal,
            )
            return

    def remove(self, cart_id):

        item_to_remove = Cart.objects.get(id=cart_id)
        item_to_remove.delete()
        return

class Cart(models.Model):
    product = models.ForeignKey(Product_models.Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(User_models.User, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits= 7, decimal_places=2) #good till 100k
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CartManager()