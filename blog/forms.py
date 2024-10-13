## write the CreateCommentForm
# blog/forms.py

from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    ''' a form to add a comment to the database '''

    class Meta:
        ''' associate this form with the comment model; select fields '''
        model = Comment
        fields = ['author', 'text', ] # which fields from the model should we use
