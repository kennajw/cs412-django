# rpg/views.py
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, DetailView, View, TemplateView
from django.db.models.base import Model as Model
from django.http.response import HttpResponse as HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from datetime import datetime
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

    model = Character
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

        # get image
        file = self.request.FILES.getlist('img')
        character.img = file[0]

        # create base starting character info
        character.level = 1
        character.hp = 10
        character.mp = 10
        character.coins = 0
        character.exp = 0

        # save character
        character.save()
        
        # achievement for new character
        ach = Achievement()
        ach.name = 'new character created!'
        ach.char = character
        ach.timestamp = datetime.now()

        # save achievement
        ach.save()

        # return super class
        return redirect('gamehome', pk=character.pk)
    
class CreateCharacterView(LoginRequiredMixin, CreateView):
    ''' a view to create a new character and save it to the database '''

    model = Character
    form_class = CreateCharacterForm
    template_name = 'rpg/create_character.html'

    def form_valid(self, form):
        ''' handle the form submission, need to get the foreign key by attaching the profile to the user object '''

        # get what user filled out in the form
        character = form.instance

        # attach user to the character
        user = self.request.user
        character.user = user

        # get image
        file = self.request.FILES.getlist('img')
        character.img = file[0]

        # create base starting character info
        character.level = 1
        character.hp = 10
        character.mp = 10
        character.coins = 0
        character.exp = 0

        # save the character to the db
        character.save()

        # achievement for new character
        ach = Achievement()
        ach.name = 'new character created!'
        ach.char = character
        ach.timestamp = datetime.now()

        # save achievement
        ach.save()

        # return super class
        # return super().form_valid(form)
        return redirect('gamehome', pk=character.pk)
    
    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    

class CharactersView(LoginRequiredMixin, ListView):
    ''' show the list of characters associated with a user '''

    model = Character
    template_name = 'rpg/character_list.html'
    context_object_name = 'characters'

    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')

class HomeView(LoginRequiredMixin, DetailView):
    ''' show the home hub page for the game for a specific chosen character '''

    model = Character
    template_name = 'rpg/home.html'
    context_object_name = 'character'

    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')

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
    
    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    
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

    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    
class SettingsView(LoginRequiredMixin, TemplateView):
    ''' shows buttons for settings options such as updating a character, deleting a character, or logging out '''

    model = Character
    template_name = 'rpg/settings.html'
    context_object_name = 'character'

    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        character = Character.objects.get(pk=pk)
        context['character'] = character
        return context

class UpdateCharacterView(LoginRequiredMixin, UpdateView):
    ''' shows the page to update your character's name and image '''

    model = Character
    template_name = 'rpg/update.html'
    context_object_name = 'character'
    fields = ['name', 'img']

    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    
    # add rerouting after success
    def get_success_url(self) -> str:
        ''' return the URL to redirect after successfully submitting the form '''

        pk = self.kwargs['pk']
        return reverse('gamehome', kwargs={'pk': pk})

class DeleteCharacterView(LoginRequiredMixin, DeleteView):
    ''' shows the page to delete your character '''

    model = Character
    template_name = 'rpg/delete.html'
    context_object_name = 'character'

    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    
    # add rerouting after success
    def get_success_url(self) -> str:
        ''' return the URL to redirect after successfully submitting the form '''

        return reverse('play')
    
class ShopView(LoginRequiredMixin, ListView):
    ''' shows the page that the character can by items from the shop '''

    model = Item
    template_name = 'rpg/shop.html'
    context_object_name = 'item'

    # add login url
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        character = Character.objects.get(pk=pk)
        context['character'] = character
        return context
    
class BuyItemView(LoginRequiredMixin, View):
    ''' a view that adds an item to a character's inventory '''
    
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')

    def dispatch(self, request, *args, **kwargs):
        ''' overwrite the default dispatch function '''

        # get the respective objects using in-line url pks
        c_pk = self.kwargs['char_pk']
        i_pk = self.kwargs['item_pk']

        # use the ORM to find those objects
        character = Character.objects.get(pk=c_pk)
        item = Item.objects.get(pk=i_pk)

        # check if the character has enough coins to purchase the item
        if (character.coins >= item.price):
            found = character.in_inventory(item)

            if (found):
                # find the inventory object that already exists for that item and character combo
                inv_qs = Inventory.objects.filter(char=character, itm=item)
                inv = [inv for inv in inv_qs]
                inv[0].quantity += 1

                # subtract the price from the characters amount of coins
                character.coins = character.coins - item.price
                character.save()
            else:
                # find the inventory object that already exists for that item and character combo
                inv = Inventory()
                inv.char = character
                inv.itm = item
                inv.quantity = 1
                inv.save()

                # subtract the price from the characters amount of coins
                character.coins = character.coins - item.price
                character.save()
        # if the character does not have enough, return the message 'insufficient funds'
        else:
            messages.info(request, 'insufficient funds')

        # redirect back to shop page
        return redirect('shop', pk=c_pk)
    
class GameView(LoginRequiredMixin, ListView):
    ''' a view to select an opponent '''

    model = Enemy
    template_name = 'rpg/game_selection.html'
    context_object_name = 'enemy'

    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        character = Character.objects.get(pk=pk)
        context['character'] = character
        return context
    
class PlayerView(LoginRequiredMixin, DetailView):
    ''' a view to show the player UI during a battle (player's turn) '''

    model = Character
    template_name = 'rpg/player.html'
    context_object_name = 'character'

    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    
    def get_object(self):
        ''' return character currently playing '''

        player_pk = self.kwargs['player_pk']
        return Character.objects.get(pk=player_pk)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)
        enemy_pk = self.kwargs['enemy_pk']
        enemy = Enemy.objects.get(pk=enemy_pk)
        context['enemy'] = enemy
        return context
    
class EnemyView(LoginRequiredMixin, DetailView):
    ''' a view to show the player UI during a battle (enemy's turn) '''

    model = Character
    template_name = 'rpg/enemy.html'
    context_object_name = 'character'

    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')
    
    def get_object(self):
        ''' return character currently playing '''

        player_pk = self.kwargs['player_pk']
        return Character.objects.get(pk=player_pk)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''

        context = super().get_context_data(**kwargs)
        enemy_pk = self.kwargs['enemy_pk']
        enemy = Enemy.objects.get(pk=enemy_pk)
        context['enemy'] = enemy
        return context
    
class PlayerAttackView(LoginRequiredMixin, View):
    ''' a view that carries out the player attack '''
    
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')

    def dispatch(self, request, *args, **kwargs):
        ''' overwrite the default dispatch function '''

        # get the respective objects using in-line url pks
        c_pk = self.kwargs['player_pk']
        e_pk = self.kwargs['enemy_pk']

        # use the ORM to find those objects
        character = Character.objects.get(pk=c_pk)
        enemy = Enemy.objects.get(pk=e_pk)

        enemy.hp = max(enemy.hp - character.attack, 0)
        enemy.save()

        if (enemy.hp == 0):
            if ((character.exp + enemy.exp_reward) >= character.get_total_exp()):
                character.exp = (character.exp + enemy.exp_reward) - character.get_total_exp()
                character.level += 1
            else:
                character.exp += enemy.exp_reward

            character.coins += enemy.coin_reward

            if (character.enemies_defeated == 0):
                ach = Achievement()
                ach.name = 'first enemy defeated!'
                ach.char = character
                ach.timestamp = datetime.now()

                ach.save()

            elif ((character.enemies_defeated + 1 ) % 5 == 0):
                ach = Achievement()
                ach.name = str(character.enemies_defeated) + ' enemy defeated!'
                ach.char = character
                ach.timestamp = datetime.now()

                ach.save()
                
            character.enemies_defeated += 1
            character.hp = character.hp_total
            character.save()

            enemy.hp = enemy.total_hp
            enemy.save()

            return redirect('win', pk=c_pk)
        else:
            messages.info(request, 'you dealt', enemy.attack, 'damage')
            return redirect('enemy', player_pk=c_pk, enemy_pk=e_pk)

class EnemyAttackView(LoginRequiredMixin, View):
    ''' a view that carries out the enemy attack '''
    
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')

    def dispatch(self, request, *args, **kwargs):
        ''' overwrite the default dispatch function '''

        # get the respective objects using in-line url pks
        c_pk = self.kwargs['player_pk']
        e_pk = self.kwargs['enemy_pk']

        # use the ORM to find those objects
        character = Character.objects.get(pk=c_pk)
        enemy = Enemy.objects.get(pk=e_pk)

        character.hp = max(character.hp - enemy.attack, 0)
        character.save()

        # if character hp is 0, you lose :(
        if (character.hp == 0):
            # update the character stats
            character.hp = character.hp_total
            character.save()

            # update the enemy stats
            enemy.hp = enemy.total_hp
            enemy.save()

            return redirect('lose', pk=c_pk)
        else:
            messages.info(request, 'you sustained', enemy.attack, 'damage')
            return redirect('player', player_pk=c_pk, enemy_pk=e_pk)

class UseItemView(LoginRequiredMixin, View):
    ''' a view that uses an item '''
    
    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')

    def dispatch(self, request, *args, **kwargs):
        ''' overwrite the default dispatch function '''

        # get the respective objects using in-line url pks
        c_pk = self.kwargs['player_pk']
        e_pk = self.kwargs['enemy_pk']
        i_pk = self.kwargs['item_pk']

        # use the ORM to find those objects
        character = Character.objects.get(pk=c_pk)
        enemy = Enemy.objects.get(pk=e_pk)
        item = Inventory.objects.get(pk=i_pk)

        # conditional to figure out what type of item
        if (item.itm.hp != 0):
            # heal your character and save
            character.hp = min(character.hp + item.itm.hp, character.hp_total)
            character.save()

            # since each consumable item only has 1 use, just decrease the quanity and save
            item.quantity -= 1
            item.save()

            # create a message saying you healed
            messages.info(request, 'you healed')

        elif (item.itm.attack != 0):
            # attack the enemy and save
            enemy.hp = max(enemy.hp - item.itm.attack, 0)
            enemy.save()

            # subtract from item uses
            item.itm.uses -= 1
            item.itm.save()

            # if the item uses is 0, that means the weapon has broken so we must decrease the quantity
            if (item.itm.uses == 0):
                # decrease the quantity and save
                item.quantity -= 1
                item.save()

            # create a message for damage dealt
            message_string = 'you dealt ' + str(enemy.attack) + ' damage'
            messages.info(request, message_string)
        
        # if the quantity is 0, delete the object from the database
        if (item.quantity == 0):
            item.delete()
        
        # if enemy hp is 0, then you have won! update accordingly
        if (enemy.hp == 0):
            # if reward exp is over the level up threshold, level the character up and readjust
            if ((character.exp + enemy.exp_reward) >= character.get_total_exp()):
                character.exp = (character.exp + enemy.exp_reward) - character.get_total_exp()
                character.level += 1
                character.hp_total += 10
            # else, just add the reward exp onto current exp
            else:
                character.exp += enemy.exp_reward

            # add reward coins to character's coins
            character.coins += enemy.coin_reward

            # if this is the first enemy defeated, create a new achievement
            if (character.enemies_defeated == 0):
                # create a new achievement model
                ach = Achievement()

                # fill the fields with data
                ach.name = 'first enemy defeated!'
                ach.char = character
                ach.timestamp = datetime.now()

                # save the achievement
                ach.save()

            # create a new achievement for every 5 enemies defeated
            elif ((character.enemies_defeated + 1 ) % 5 == 0):
                # create a new achievement model
                ach = Achievement()

                # fill the fields with data
                ach.name = str(character.enemies_defeated) + ' enemy defeated!'
                ach.char = character
                ach.timestamp = datetime.now()

                # save the achievement
                ach.save()

            # update character stats
            character.enemies_defeated += 1
            character.hp = character.hp_total
            character.save()

            # update enemy states
            enemy.hp = enemy.total_hp
            enemy.save()

            # redirect to the win page
            return redirect('win', pk=c_pk)
        else:
            # redirect to the enemy turn page
            return redirect('enemy', player_pk=c_pk, enemy_pk=e_pk)

class WinView(LoginRequiredMixin, DetailView):
    ''' a view to show that the player has won '''

    model = Character
    template_name = 'rpg/win.html'
    context_object_name = 'character'

    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')

class LoseView(LoginRequiredMixin, DetailView):
    ''' a view to show that the player has lost '''

    model = Character
    template_name = 'rpg/win.html'
    context_object_name = 'character'

    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')