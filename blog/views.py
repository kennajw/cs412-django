from django.shortcuts import render
from django.views.generic import ListView
from .models import *

# Create your views here.
# class-based view
class ShowAllView(ListView):
    ''' the view to show all articles '''
    model = Article # model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # context variable to use in the template
