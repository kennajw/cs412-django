from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
import random

# Create your views here.
def main(request):
    '''show the main restaurant page'''

    template_name = "restaurant/main.html"

    return render(request, template_name)

def order(request):
    '''show the order form'''

    template_name = "restaurant/order.html"

    # specials list and context variable
    specials = ['cold water', 'room temp. water', 'warm water']

    context = {
         'special' : specials[random.randint(0,2)],
    }

    return render(request, template_name, context)

def submit(request):
        '''handle the order submission. read the order data from the request and send it back to the template.'''
        
        template_name = 'restaurant/confirmation.html'

        # check that we have a POST request
        if request.POST:
            # read the form data into python variables
            # order details and total
            order = request.POST.getlist('order')
            total = 0

            for item in order:
                if item == "chicken tikka masala":
                    total = 13 + total
                elif item == "tandoori chicken":
                    total = 14 + total
                elif item == "naan":
                    total = 3 + total
                elif item == "garlic naan":
                    total = 4 + total
                else:
                    pass

            # customer information
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']

            # package the form ddata up as context variables for the template
            context = {
                'name' : name,
                'phone' : phone,
                'email' : email,
                'est_time' : (datetime.now() + timedelta(minutes = (random.randint(30, 60)))),
                'order' : order,
                'total' : total
            }

            return render(request, template_name, context)
        
        ## handle GET request on this URL
        # an "ok" solution...
        # return HttpResponse("Nope.")

        ## a "better" solution...
        # template_name = "formdata/form.html"
        # return render(request, template_name)
        
        # an even better solution: redirect to the correct URL:
        return redirect("order")
