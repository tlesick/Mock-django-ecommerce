from django.db import models
from apps.Product import models as Product_models
from apps.User import models as User_models
from apps.Address import models as Address_models
from apps.Cart import models as Cart_models
from django.contrib.postgres.fields import ArrayField

class OrderManager(models.Manager):
    # user is the object itself
    def new_order(self, user):
        address = Address_models.Address.objects.get(user = user, preference= 0)
        tax = 0.0725
        tax_amount = 0
        cart = Cart_models.Cart.objects.filter(user= user.id)
        product_ids = []
        quantities = []
        rtotal = 0
        for i in cart:
            product_ids.append(int(i.product.id))
            quantities.append(int(i.quantity))
            rtotal += float(i.product.price) * float(i.quantity)
            i.delete()
        tax_amount = rtotal * tax
        
        Order.objects.create(
            user = user,
            quantity = quantities,
            total = (tax_amount + rtotal),
            tax = tax_amount,
            products = product_ids,
            address = address,
        )
        return


class Order(models.Model):
    user = models.ForeignKey(User_models.User, on_delete=models.CASCADE)
    quantity = ArrayField(models.IntegerField())
    total = models.DecimalField(max_digits=8, decimal_places=2)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    products = ArrayField(models.IntegerField())
    address = models.ForeignKey(Address_models.Address, on_delete=models.CASCADE)
    status = models.CharField(max_length= 50, default= 'Order Received')
    order_date = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager() #incase the order is cancelled or updated