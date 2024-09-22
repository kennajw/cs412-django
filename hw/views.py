from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
# def home(request):
#     '''handle the main URL for the hw app'''

#     response_text = '''
#     <html>
#     <h1>Hello, world!<h1>
#     <p>this is our first django web app<p>
#     <html>
#     '''

#     return HttpResponse(response_text)

def home(request):
    '''
    function to handle the URL request for /hw (main page)
    delegate rendering to the template hw/home.html
    '''

    # use this template to render response
    t_name = 'hw/home.html'

    #create a dictionary of context variables
    context = {
        "current_time" : time.ctime(),
        "letter1" : chr(random.randint(65, 90)), # letter from a-z
        "letter2" : chr(random.randint(65, 90)), # letter from a-z
        "number" : random.randint(1, 10), # number from 1-10
    }

    # delegate rendering work to the template
    return render(request, t_name, context)

def about(request):
    '''
    Function to handle the URL request for /hw/about (about page).
    Delegate rendering to the template hw/about.html.
    '''
    # use this template to render the response
    template_name = 'hw/about.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)