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