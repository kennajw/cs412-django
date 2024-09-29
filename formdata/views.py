from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def show_form(request):
    '''show the contact form'''

    template_name = "formdata/form.html"

    return render(request, template_name)

def submit(request):
        '''handle the form submission. read the form data from the request and send it back to the template.'''
        
        template_name = 'formdata/confirmation.html'
        # print(request)

        # check that we have a POST request
        if request.POST:

            # print(request.POST)
            # read the form data into python variables
            name = request.POST['name']
            color = request.POST['color']

        # package the form ddata up as context variables for the template
        context = {
            'name' : name,
            'color' : color,
        }

        return render(request, template_name, context)

    ## handle the GET request
    # an 'okay' solution
    # HttpResponse('nope.')

    # better solution
    # template_name = "formdata/form.html"
    # return render(request, template_name)

    # an even better solution
    # return redirect("show_form")