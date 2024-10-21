from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    ''' a form to add a new profile to the database '''

    class Meta:
        ''' associate this form with the profile model; select fields '''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_pic'] # which fields from the model should we use

class CreateStatusMessageForm(forms.ModelForm):
    ''' a form to add a new status message to the database '''

    class Meta:
        ''' associate this form with the status message model; select fields '''
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    ''' a form to update an existing profile in the database '''

    class Meta:
        ''' associate this form with the profile model; select fields '''
        model = Profile
        fields = ['city', 'email', 'profile_pic']