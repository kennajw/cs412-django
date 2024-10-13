## blog/urls.py
## description: URL patterns for the  blog app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'show_all', views.ShowAllView.as_view(), name="show_all_articles"),
    path('',views.RandomArticleView.as_view(), name='random'),
    path('article/<int:pk>', views.ArticlePageView.as_view(), name='article'),
    path('article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'),
]