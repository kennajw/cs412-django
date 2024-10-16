from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse
from typing import Any
from .forms import *
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

class CreateProfileView(CreateView):
    ''' a view to create a new profile and save it to the database '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

class CreateStatusMessageView(CreateView):
    ''' a view to create a new status message and save it to the database '''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        ''' handle the form submission, need to get the foreign key by
        attaching the profile to the status message object, can find the profile
        pk in the url (self.kwargs) '''
        print(form.cleaned_data)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        ''' return the URL to redirect after successfully submitting the form '''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
        ## note: this is not ideal because we are redircted to the main page
