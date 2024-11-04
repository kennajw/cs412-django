## blog/urls.py
## description: URL patterns for the  blog app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'show_all', views.ShowAllView.as_view(), name="show_all_articles"),
    path('',views.RandomArticleView.as_view(), name='random'),
    path('article/<int:pk>', views.ArticlePageView.as_view(), name='article'),
    path('article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'),
    path(r'create_article', views.CreateArticleView.as_view(), name='create_article'),
    path(r'login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name="login_blog"),
    path(r'logout/', auth_views.LogoutView.as_view(next_page='show_all_articles'), name="logout_blog"),
    path('register/', views.RegistrationView.as_view(), name='register'),
]