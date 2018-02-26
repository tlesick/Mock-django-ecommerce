from django.db import models
from apps.User import models as User_models

class addressManager(models.Manager):
    def addAddress(self, data, user_id):
        user_address = User_models.User.objects.get(id = user_id)
        errors = []
        # validates the entrty
        if len(data['street']) < 1:
            errors.append("street field is missing")
        if len(data['city']) < 1:
            errors.append("city field is missing")
        if len(data['state']) <1:
            errors.append("State field is missing")
            # check if the address is correct
        if len(data['zip_code']) < 1:
            errors.append("Zip Code Field is Missing")
        # looks if the same address already exists
        current_addresses = Address.objects.filter(
                street= data['street'], 
                city= data['city'],
                state= data['state'], 
                zip_code = data['zip_code'],
                user= user_address)
        print (current_addresses)
        if len(current_addresses) > 0:
            errors.append("You already have that address")                
        if errors:
            return {'error_msg':errors}
        else:
            other_addresses = Address.objects.filter(user= user_id)
            if len(other_addresses) > 0:
                preference = 1
                added_address = Address.objects.create(
                street= data['street'], 
                city= data['city'],
                state= data['state'], 
                zip_code = data['zip_code'],
                user= user_address,
                preference = preference,
            )  
            else:
                added_address = Address.objects.create(
                street= data['street'], 
                city= data['city'],
                state= data['state'], 
                zip_code = data['zip_code'],
                user= user_address,
                )

            return {'new_address': added_address}


    def update(self, postdata, address_id):
        address_changed = Address.objects.get(id = address_id)
        if len(postdata['street']) > 1:
            address_changed.street = postdata['street']
            address_changed.save()
        if len(postdata['city']) > 1:
            address_changed.city = postdata['city']
            address_changed.save()
        if len(postdata['state']) > 1:
            address_changed.state = postdata['state']
            address_changed.save()
        if len(postdata['zip_code']) > 1:
            address_changed.zip_code = postdata['zip_code']
            address_changed.save()        
        else:
            return         
        


class Address(models.Model):
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 2)
    zip_code = models.CharField(max_length = 5, default= 00000)
    user = models.ForeignKey(User_models.User, on_delete=models.CASCADE)
    # preference 1 indicates preferred
    preference = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = addressManager()