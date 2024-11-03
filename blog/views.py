from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from .forms import *
from .models import *
import random

# Create your views here.
# class-based view
class ShowAllView(ListView):
    ''' the view to show all articles '''
    model = Article # model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # context variable to use in the template

    def dispatch(self, *args, **kwargs):
        ''' implement this method to add some debug tracing '''

        print(f"ShowAllView.dispatch; request.user={self.request.user}")
        # let the superclass version of this method do its work:
        return super().dispatch(*args, **kwargs)

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

class CreateCommentView(CreateView):
    ''' a view to create a new comment and save it to the database '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ''' build the dict of context data for this view '''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        context['article'] = article
        return context

    def form_valid(self, form):
        ''' handle the form submission, need to get the foreign key by
        attaching the article tothe comment object, can find the article
        pk in the url (self.kwargs) '''
        print(form.cleaned_data)
        article = Article.objects.get(pk=self.kwargs['pk'])
        form.instance.article = article
        return super().form_valid(form)

    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        ''' return the URL t oredirect after successfully submitting the form '''
        # return reverse('show_all')
        return reverse('article', kwargs={'pk': self.kwargs['pk']})
        ## note: this is not ideal because we are redircted to the main page

class CreateArticleView(LoginRequiredMixin, CreateView):
    ''' a view class to create a new article instance '''

    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def get_login_url(self) -> str:
        ''' return the url of the login page '''
        return reverse('login')

    def form_valid(self, form):
        ''' this method is called as part of the form processing '''

        print(f'CreateArticleView.form_valid(): form.cleaned_data={form.cleaned_data}')

        # find the user who is logged in
        user = self.request.user

        # attach that user as a fk to the new article instance
        form.instance.user = user

        # let the superclass do the real work
        return super().form_valid(form)