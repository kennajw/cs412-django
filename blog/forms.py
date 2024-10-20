## write the CreateCommentForm
# blog/forms.py

from django import forms
from .models import Comment, Article

class CreateCommentForm(forms.ModelForm):
    ''' a form to add a comment to the database '''

    class Meta:
        ''' associate this form with the comment model; select fields '''
        model = Comment
        fields = ['author', 'text', ] # which fields from the model should we use

class CreateArticleForm(forms.ModelForm):
    ''' a form to add a new article to the database '''

    class Meta:
        ''' associate this html form with the article data model '''
        model = Article
        fields = ['title', 'author', 'text', 'image_file']