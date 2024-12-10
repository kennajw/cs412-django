# rpg/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Character(models.Model):
    ''' encapsulate the character of a user in the rpg '''

    # character information
    name = models.TextField(blank=False)
    img = models.ImageField(blank=False)
    level = models.IntegerField(blank=False)
    hp = models.IntegerField(blank=False)
    coins = models.IntegerField(blank=False)
    exp = models.IntegerField(blank=False)
    attack = models.IntegerField(blank=False)
    enemies_defeated = models.IntegerField(blank=False)

    # user foreign key (handled by django)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
    
    def get_total_exp(self):
        ''' return the total exp needed before leveling up '''

        # get current level
        level = self.level
        # calculate total exp need
        exp_needed = level * 100

        #return exp needed
        return exp_needed
    
    def get_inventory(self):
        ''' return a QuerySet of all inventory items for this character '''

        # use the ORM to retrieve comments for which the FK is this article
        items = Inventory.objects.filter(char=self)
        items = items.filter(quantity__gt=0)
        items = items.filter(itm__uses__gt=0)
        return items 
    
    def get_achievements(self):
        ''' return a QuerySet of all achievements for this character '''

        # use the ORM to retrieve comments for which the FK is this article
        achievements = Achievement.objects.filter(char=self)
        return achievements

class Item(models.Model):
    ''' encapsulate the items of a user in the rpg '''

    # item information
    name = models.TextField(blank=False)
    type = models.TextField(blank=False)
    img = models.ImageField(blank=False)
    hp = models.IntegerField(blank=False)
    attack = models.IntegerField(blank=False)
    uses = models.IntegerField(blank=False)
    description = models.TextField(blank=False)
    price = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.name}'

class Inventory(models.Model):
    ''' encapsulate the inventory of a user in the rpg '''

    # inventory information
    quantity = models.IntegerField(blank=False)

    # foreign keys
    char = models.ForeignKey(Character, on_delete=models.CASCADE)
    itm = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.char}\'s {self.itm} ({self.quantity})'

class Achievement(models.Model):
    ''' encapsulate the achievements of a user in the rpg '''

    # achievment information
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField()

    # foreign key
    char = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.char}'

class Enemy(models.Model):
    ''' encapsulate the enemy in the rpg '''

    # enemy information
    name = models.TextField(blank=False)
    img = models.ImageField(blank=False)
    difficulty = models.TextField(blank=False)
    hp = models.IntegerField(blank=False)
    attack = models.IntegerField(blank=False)
    coin_reward = models.IntegerField(blank=False)
    exp_reward = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.name} - {self.difficulty}'

class Battle(models.Model):
    ''' encapsulate a battle between a character and an enemy in the rpg '''

    # battle information
    enemy_hp = models.IntegerField(blank=False)
    player_hp = models.IntegerField(blank=False) 

    # foreign keys
    char = models.ForeignKey(Character, on_delete=models.CASCADE)
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.char} vs. {self.enemy}' 