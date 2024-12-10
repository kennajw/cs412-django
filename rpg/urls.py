# rpg/urls.py
# description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.MenuView.as_view(), name="play"),
    path(r'menu/', views.MenuOptionsView.as_view(), name='menu'),
    path(r'login/', auth_views.LoginView.as_view(template_name='rpg/login.html'), name="rpglogin"),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='rpg/logout.html'), name="rpglogout"),
    path(r'create_account/', views.CreateAccountView.as_view(), name='create_account'),
    path(r'create_character/', views.CreateCharacterView.as_view(), name='create_character'),
    path(r'new_game/', views.NewOptionsView.as_view(), name='new_options'),
    path(r'characters/', views.CharactersView.as_view(), name='character_list'),
    path(r'gamehome/<int:pk>/', views.HomeView.as_view(), name='gamehome'),
    path(r'inventory/<int:pk>/', views.InventoryView.as_view(), name='inventory'),
    path(r'achievements/<int:pk>/', views.AchievementsView.as_view(), name='achievements'),
    path(r'settings/<int:pk>/', views.SettingsView.as_view(), name='settings'),
    path(r'update_character/<int:pk>/', views.UpdateCharacterView.as_view(), name='update'),
    path(r'delete_character/<int:pk>/', views.DeleteCharacterView.as_view(), name='delete'),
    path(r'shop/<int:pk>/', views.ShopView.as_view(), name='shop'),
    path(r'buy/<int:char_pk>/<int:item_pk>', views.BuyItemView.as_view(), name='buy'),
    path(r'selection/<int:pk>/', views.GameView.as_view(), name='selection'),
    path(r'player_turn/<int:player_pk>/<int:enemy_pk>/', views.PlayerView.as_view(), name='player'),
    path(r'enemy_turn/<int:player_pk>/<int:enemy_pk>/', views.EnemyView.as_view(), name='enemy'),
    path(r'player_attack/<int:player_pk>/<int:enemy_pk>/', views.PlayerAttackView.as_view(), name='player_attack'),
    path(r'enemy_attack/<int:player_pk>/<int:enemy_pk>/', views.EnemyAttackView.as_view(), name='enemy_attack'),
    path(r'use_item/<int:player_pk>/<int:enemy_pk>/<int:item_pk>/', views.UseItemView.as_view(), name='use_item'),
    path(r'win/<int:pk>/', views.WinView.as_view(), name='win'),
    path(r'lose/<int:pk>/', views.LoseView.as_view(), name='lose'),
    path(r'new_battle/<int:player_pk>/<int:enemy_pk>/', views.NewBattleView.as_view(), name='new_battle')
]