from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    ''' encapsulate the idea of on article by some author '''
    #every article has one user:
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # data attributes of an article
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        ''' return a string representation of this object '''
        return f'{self.title} by {self.author}'
    
    def get_comments(self):
        ''' return a QuerySet of all comments on this article '''

        # use the ORM to retrieve comments for which the FK is this article
        comments = Comment.objects.filter(article=self)
        return comments
    
    def get_absolute_url(self):
        ''' return the url that will display an instance of the article object '''

        # self.pk is the primary key to this article instance
        return reverse('article', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    ''' encapsulate the idea of a comment on an article'''

    # model the 1 to many relationship with Article (foreign key)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'