from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.

quotes = ["I lived in Ireland for about four months and I got really in character and I was on all fours for four months and it was really painful, but beautiful, as well. And it was probably the most fulfilling part of my career and I’m so happy for everybody going to the Oscars even though I deserved the nomination more than anybody else because I was obviously a donkey for four months.", "I eat like Macaulay Culkin in Home Alone 2.", "Shoutout to my my people... Shoutout to Derry, shoutout to Cork, shoutout to Killarney, shoutout to Dublin..."]
images = ["/static/images/ayo-1.webp", "/static/images/ayo-2.webp", "/static/images/ayo-3.jpg"]

def quote(request):
    '''
    function to handle the URL request for /hw (main page)
    delegate rendering to the template hw/home.html
    '''

    # use this template to render response
    template_name = 'quotes/quote.html'

    #create a dictionary of context variables
    context = {
        "random_image" : images[random.randint(0,2)],
        "random_quote" : quotes[random.randint(0,2)],
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle the URL request for /hw/about (about page).
    Delegate rendering to the template hw/about.html.
    '''
    # use this template to render the response
    template_name = 'quotes/about.html'

    # delegate rendering work to the template
    return render(request, template_name)

def show_all(request):
    '''
    Function to handle the URL request for /hw/about (about page).
    Delegate rendering to the template hw/about.html.
    '''
    # use this template to render the response
    template_name = 'quotes/show_all.html'

    # create a dictionary of context variables for the template:
    context = {
        "image1" : images[0],
        "image2" : images[1],
        "image3" : images[2],
        "quote1" : quotes[0],
        "quote2" : quotes[1],
        "quote3" : quotes[2],
    }

    # delegate rendering work to the template
    return render(request, template_name, context)