# rpg/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, TemplateView
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from typing import Any
from .forms import *
from .models import *

# Create your views here.
class MenuView(TemplateView):
    ''' generic template view for main menu page '''

    template_name='rpg/menu.html'

class MenuOptionsView(TemplateView):
    ''' generic template view for menu options page '''

    template_name='rpg/menu_options.html'

class NewOptionsView(TemplateView):
    ''' generic template view for menu options page '''

    template_name='rpg/new_options.html'

class CreateAccountView(CreateView):
    ''' a view to create a new profile and save it to the database '''

    form_class = CreateCharacterForm
    template_name = "rpg/create_account.html"

    def get_context_data(self, **kwargs: Any):
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)

        # create user_form
        user_form = UserCreationForm()
        context['user_form'] = user_form
        return context
    
    def form_valid(self, form):
        ''' handle the form submission, need to get the foreign key by attaching the profile to the user object '''

        # user form
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()

        # get what user filled out in the form
        character = form.instance

        #attach user to the character
        character.user = user

        # create base starting character info
        character.level = 1
        character.hp = 10
        character.mp = 10
        character.coins = 0
        character.exp = 0

        # save character
        character.save()

        # return super class
        return redirect('gamehome', pk=character.pk)
    
class CreateCharacterView(LoginRequiredMixin, CreateView):
    ''' a view to create a new character and save it to the database '''

    form_class = CreateCharacterForm
    template_name = 'rpg/create_character.html'

    def form_valid(self, form):
        ''' handle the form submission, need to get the foreign key by attaching the profile to the user object '''

        # get what user filled out in the form
        character = form.instance

        # attach user to the character
        user = self.request.user
        character.user = user

        # create base starting character info
        character.level = 1
        character.hp = 10
        character.mp = 10
        character.coins = 0
        character.exp = 0

        # save the character to the db
        character.save()

        # return super class
        return redirect('gamehome', pk=character.pk)

class CharactersView(LoginRequiredMixin, ListView):
    ''' show the list of characters associated with a user '''

    model = Character
    template_name = 'rpg/character_list.html'
    context_object_name = 'characters'

class HomeView(LoginRequiredMixin, DetailView):
    ''' show the home hub page for the game for a specific chosen character '''

    model = Character
    template_name = 'rpg/home.html'
    context_object_name = 'character'

class InventoryView(LoginRequiredMixin, ListView):
    ''' show the list of inventory items that your character has '''

    model = Inventory
    template_name = 'rpg/inventory.html'
    context_object_name = 'inventory'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        character = Character.objects.get(pk=pk)
        context['character'] = character
        return context
    
class AchievementsView(LoginRequiredMixin, ListView):
    ''' show the list of achievements that your character has completed '''

    model = Achievement
    template_name = 'rpg/achievements.html'
    context_object_name = 'achievement'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        character = Character.objects.get(pk=pk)
        context['character'] = character
        return context