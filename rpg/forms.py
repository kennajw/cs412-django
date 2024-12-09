from django import forms
from .models import Character

class CreateCharacterForm(forms.ModelForm):
    ''' a form to add a new profile to the database '''

    class Meta:
        ''' associate this form with the profile model; select fields '''
        model = Character
        fields = ['name', 'img'] 

class UpdateProfileForm(forms.ModelForm):
    ''' a form to update an existing profile in the database '''

    class Meta:
        ''' associate this form with the profile model; select fields '''
        model = Character
        fields = ['name', 'img']