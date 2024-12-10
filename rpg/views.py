# rpg/views.py
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
        character.coins = 0
        character.exp = 0
        character.attack = 5
        character.enemies_defeated = 0

        # save character
        character.save()
        
        # achievement for new character
        ach = Achievement()
        ach.name = '1st time playing!'
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
        character.coins = 0
        character.exp = 0
        character.attack = 5
        character.enemies_defeated = 0

        # save the character to the db
        character.save()

        # achievement for new character
        ach = Achievement()
        ach.name = '1st time playing!'
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
            if (Inventory.objects.filter(char=character, itm=item).exists()):
                # find the inventory object that already exists for that item and character combo
                inv= Inventory.objects.get(char=character, itm=item)
                inv.quantity += 1
                inv.save()

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

        # call the super class context
        context = super().get_context_data(**kwargs)

        # get the in-line pks
        player_pk = self.kwargs['player_pk']
        enemy_pk = self.kwargs['enemy_pk']

        # get the objects from the ORM
        enemy = Enemy.objects.get(pk=enemy_pk)
        character = Character.objects.get(pk=player_pk)
        battle = Battle.objects.get(char=character, enemy=enemy)

        # add the context variables
        context['enemy'] = enemy
        context['battle'] = battle

        # return the context variables
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

        # call the super class context
        context = super().get_context_data(**kwargs)

        # get the in-line pks
        player_pk = self.kwargs['player_pk']
        enemy_pk = self.kwargs['enemy_pk']

        # get the objects from the ORM
        enemy = Enemy.objects.get(pk=enemy_pk)
        character = Character.objects.get(pk=player_pk)
        battle = Battle.objects.get(char=character, enemy=enemy)

        # add the context variables
        context['enemy'] = enemy
        context['battle'] = battle

        # return the context variables
        return context
    
class NewBattleView(LoginRequiredMixin, View):
    ''' a view for when a battle is started '''

    def dispatch(self, request, *args, **kwargs):
        ''' overwrite the default dispatch function '''

        # get the respective objects using in-line url pks
        c_pk = self.kwargs['player_pk']
        e_pk = self.kwargs['enemy_pk']

        # use the ORM to find those objects
        character = Character.objects.get(pk=c_pk)
        enemy = Enemy.objects.get(pk=e_pk)

        if (Battle.objects.filter(char=character, enemy=enemy).exists()):
            # redirect to player turn page
            return redirect('player', player_pk=c_pk, enemy_pk=e_pk)
        else:
            # create a new battle object
            battle = Battle()

            # fill the fields of the object
            battle.player_hp = character.hp
            battle.enemy_hp = enemy.hp
            battle.char = character
            battle.enemy = enemy

            # save the battle object
            battle.save()

            # after creating a new object, redirect to player turn page
            return redirect('player', player_pk=c_pk, enemy_pk=e_pk)
    
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
        battle = Battle.objects.get(char=character, enemy=enemy)

        # attack the enemy
        battle.enemy_hp = max(battle.enemy_hp - character.attack, 0)
        battle.save()

        if (battle.enemy_hp == 0):
            # if reward exp is over the level up threshold, level the character up and readjust
            if ((character.exp + enemy.exp_reward) >= character.get_total_exp()):
                character.exp = (character.exp + enemy.exp_reward) - character.get_total_exp()

                # level up
                character.level += 1
                character.hp += 10
                character.attack += 2
            # else, add the reward exp to current exp
            else:
                character.exp += enemy.exp_reward

            # add the reward coins to character's coins
            character.coins += enemy.coin_reward

            if (character.enemies_defeated == 0):
                # create a new achievement object
                ach = Achievement()

                # fill the fields
                ach.name = '1st enemy defeated!'
                ach.char = character
                ach.timestamp = datetime.now()

                # save the object
                ach.save()

            elif ((character.enemies_defeated + 1 ) % 5 == 0):
                # create a new achievement object
                ach = Achievement()

                # fill the fields
                ach.name = str(character.enemies_defeated + 1) + ' enemies defeated!'
                ach.char = character
                ach.timestamp = datetime.now()

                # save the object
                ach.save()
                
            # update number of enemies defeated and save
            character.enemies_defeated += 1
            character.save()

            # delete the battle
            battle.delete()
            
            # redirect to win page
            return redirect('win', pk=c_pk)
        else:
            # create a message for damage dealt
            message_string = 'you dealt ' + str(character.attack) + ' damage'
            messages.info(request, message_string)

            # redirect to enemy's turn
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
        battle = Battle.objects.get(char=character, enemy=enemy)

        # attack the player
        battle.player_hp = max(battle.player_hp - enemy.attack, 0)
        battle.save()

        # if character hp is 0, you lose :(
        if (battle.player_hp == 0):
            # delete the battle
            battle.delete()

            # redirect to lose page
            return redirect('lose', pk=c_pk)
        else:
            # create a message for damage sustained
            message_string = 'you sustained ' + str(enemy.attack) + ' damage'
            messages.info(request, message_string)

            # redirect to player's turn
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
        battle = Battle.objects.get(char=character, enemy=enemy)
        item = Inventory.objects.get(pk=i_pk)

        # conditional to figure out what type of item
        if (item.itm.hp != 0):
            # heal your character and save
            battle.player_hp = min(battle.player_hp + item.itm.hp, character.hp)
            battle.save()

            # since each consumable item only has 1 use, just decrease the quanity and save
            item.quantity -= 1
            item.save()

            # create a message saying you healed
            message_string = 'you healed ' + str(item.itm.hp) + ' hp'
            messages.info(request, message_string)

        elif (item.itm.attack != 0):
            # attack the enemy and save
            battle.enemy_hp = max(battle.enemy_hp - item.itm.attack, 0)
            battle.save()

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
        if (battle.enemy_hp == 0):
            # if reward exp is over the level up threshold, level the character up and readjust
            if ((character.exp + enemy.exp_reward) >= character.get_total_exp()):
                character.exp = (character.exp + enemy.exp_reward) - character.get_total_exp()

                # level up
                character.level += 1
                character.hp += 10
                character.attack += 2

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
                ach.name = '1st enemy defeated!'
                ach.char = character
                ach.timestamp = datetime.now()

                # save the achievement
                ach.save()

            # create a new achievement for every 5 enemies defeated
            elif ((character.enemies_defeated + 1 ) % 5 == 0):
                # create a new achievement model
                ach = Achievement()

                # fill the fields with data
                ach.name = str(character.enemies_defeated + 1) + ' enemies defeated!'
                ach.char = character
                ach.timestamp = datetime.now()

                # save the achievement
                ach.save()

            # delete the battle
            battle.delete()

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
    template_name = 'rpg/lose.html'
    context_object_name = 'character'

    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('rpglogin')