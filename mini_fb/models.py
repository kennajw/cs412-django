from django.db import models

# Create your models here.
class Profile(models.Model):
    ''' encapsulate the profile of a user on mini-fb '''
    # data attributes of an article
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_pic = models.URLField(blank=True)

    def __str__(self):
        ''' return a string representation of this object '''
        return f'{self.first_name} {self.last_name}\'s Profile'
    
    def get_status_messages(self):
        ''' return a QuerySet of all status messages on this profile '''

        # use the ORM to retrieve comments for which the FK is this article
        comments = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return comments

class StatusMessage(models.Model):
    ''' encapsulates the status of a user profile on mini-fb '''
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        ''' return a string representation of this object '''
        return f'{self.message}'