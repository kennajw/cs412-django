from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.
# class-based view
class ShowAllProfilesView(ListView):
    ''' the view to show all profiles '''
    model = Profile # model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template

class ShowProfilePageView(DetailView):
    ''' show the details for one profile '''
    model = Profile
    template_name = 'mini_fb/show_profile.html' ## reusing same template!!
    context_object_name = 'profile'