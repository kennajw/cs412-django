from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
import random

# Create your views here.
# class-based view
class ShowAllView(ListView):
    ''' the view to show all articles '''
    model = Article # model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # context variable to use in the template

class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    # pick one article at random:
    def get_object(self):
        '''Return one Article object chosen at random.'''
        all_articles = Article.objects.all()
        return random.choice(all_articles)
    
class ArticlePageView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html' ## reusing same template!!
    context_object_name = 'article'