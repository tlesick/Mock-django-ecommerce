from django.shortcuts import render, redirect
from apps.User.models import *
from .models import *
# if the user is not logged in there will be an error, shouldn't be possible
def registration(request):
    print (request.session['user_id'])
    user = User.objects.get(id= request.session['user_id'])
    content = {
         'user': user,
     }
    return render(request, 'address/registration.html', content)

def register(request):
    new_address = Address.objects.addAddress(request.POST, request.session['user_id'])
    if 'error_msg' in new_address:
        for e in new_address['error_msg']:
            messages.error(request, e)
        return redirect('/address/registration')
    else:
        # new address is added could show it
        return redirect("/user/show")

def edit(request, address_id):
    address = Address.objects.get(id = address_id)
    user = User.objects.get(id= request.session['user_id'])
    content = {
        'user': user,
        'address': address,
    }
    return render(request, 'address/edit.html', content)


def update(request, address_id):
    data = request.POST
    print (data['street'])
    print (data['city'])
    print (data['state'])
    print (data['zip_code'])
    update_address = Address.objects.update(request.POST, address_id)
    return redirect('/user/show')

# the element that is selected with a 0, find it and replace with a 1, but don't save
# find another the previous element with 1
def preference_change(request, address_id):
    user = User.objects.get(id = request.session['user_id'])
    find_old = Address.objects.get(user = user.id, preference = 1)
    find_old.preference = 0
    find_old.save()
    new_preferred = Address.objects.get(user = user.id, id= address_id)
    new_preferred.preference = 1
    new_preferred.save()
    print (new_preferred.preference)
    print (find_old.preference)
    
    return redirect('/user/show')