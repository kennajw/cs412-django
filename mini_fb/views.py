from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
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

    def get_context_data(self, **kwargs: Any):
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)

        # create user_form
        user_form = UserCreationForm()
        context['user_form'] = user_form
        return context
    
    def form_valid(self, form):
        ''' handle the form submission, need to get the foreign key by
        attaching the profile to the user object '''

        # user form
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()

        profile = form.instance
        profile.user = user
        # save profile
        profile.save()

        # return super class
        return super().form_valid(form)

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    ''' a view to create a new status message and save it to the database '''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)
        pk = self.get_object().pk
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context
    
    def get_object(self):
        ''' return Profile of the user associated with it '''

        curr_user = self.request.user
        profile = Profile.objects.get(user=curr_user)
        return profile

    def form_valid(self, form):
        ''' handle the form submission, need to get the foreign key by
        attaching the profile to the status message object, can find the profile
        pk in the url (self.kwargs) '''
        print(form.cleaned_data)
        profile = self.get_object()
        form.instance.profile = profile
        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image()
            image.image = file
            image.message = sm
            image.save()
        return super().form_valid(form)
    
    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('login')

    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        ''' return the URL to redirect after successfully submitting the form '''

        return reverse('show_profile', kwargs={'pk': self.get_object().pk})
        ## note: this is not ideal because we are redircted to the main page

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' a view to update an existing profile and save it to the database '''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        ''' return Profile of the user associated with it '''

        curr_user = self.request.user
        profile = Profile.objects.get(user=curr_user)
        return profile
    
    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('login')

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    ''' a view to delete an existing status message in the database '''

    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status'

    def get_success_url(self) -> str:
        ''' return the URL to redirect after successfully submitting the form '''

        profile = self.object.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('login')

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    ''' a view to update an existing status message and save it to the database '''

    model = StatusMessage
    form_class = UpdateStatusForm
    context_object_name = 'status'
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self) -> str:
        ''' return the URL to redirect after successfully submitting the form '''

        profile = self.object.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('login')

class CreateFriendView(View):
    ''' a view to create a friend relation between two profiles '''

    def get_object(self):
        ''' return Profile of the user associated with it '''

        curr_user = self.request.user
        profile = Profile.objects.get(user=curr_user)
        return profile

    def dispatch(self, request, *args, **kwargs):
        ''' override dispatch method '''

        pk = self.get_object().pk
        otherpk = self.kwargs['other_pk']

        profile1 = Profile.objects.get(pk=pk)
        profile2 = Profile.objects.get(pk=otherpk)

        profile1.add_friend(profile2)

        return redirect('show_profile', pk=pk)
    
class ShowFriendSuggestionsView(DetailView):
    ''' show the details for friend suggestions for a profile '''

    model = Profile
    template_name = 'mini_fb/friend_suggestions.html' 
    context_object_name = 'profile'

    def get_object(self):
        ''' return Profile of the user associated with it '''

        curr_user = self.request.user
        profile = Profile.objects.get(user=curr_user)
        return profile

class ShowNewsFeedView(DetailView):
    ''' show the details for one profile '''
    model = Profile
    template_name = 'mini_fb/news_feed.html' ## reusing same template!!
    context_object_name = 'profile'

    def get_object(self):
        ''' return Profile of the user associated with it '''

        curr_user = self.request.user
        profile = Profile.objects.get(user=curr_user)
        return profile