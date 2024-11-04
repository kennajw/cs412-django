from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ''' encapsulate the profile of a user on mini-fb '''
    # data attributes of an article
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_pic = models.URLField(blank=True)
    #every profile has one user:
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        ''' return a string representation of this object '''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        ''' return a QuerySet of all status messages on this profile '''

        # use the ORM to retrieve comments for which the FK is this article
        comments = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return comments
    
    def get_friends(self):
        ''' return a list of all friends for a profile '''
        friendp1 = Friend.objects.filter(profile1=self)
        friendp2 = Friend.objects.filter(profile2=self)
        friendsp1 = [profile.profile2 for profile in friendp1]
        friendsp2 = [profile.profile1 for profile in friendp2]

        if (friendsp1 == []):
            friends = friendsp2
        elif (friendsp2 == []):
            friends = friendsp1
        else:
            friends = friendsp1.extends(friendsp2)
        return friends
    
    def add_friend(self, other):
        ''' add a friend relation between two profiles '''

        if (self == other):
            return
        elif (other in self.get_friends()):
            return
        else:
            friend = Friend()
            friend.profile1 = self
            friend.profile2 = other
            friend.save()

    def get_friend_suggestions(self):
        ''' return a list of possible friends for a profile '''

        allq = Profile.objects.all()
        all = [profile for profile in allq]
        friends = self.get_friends()
        suggestions = []

        for suggestion in all:
            if ((suggestion != self) & (suggestion not in friends)):
                suggestions.append(suggestion)
        
        return suggestions

    def get_news_feed(self):
        ''' return a list of status messages of the profile and friends' profiles '''

        friends = self.get_friends()
        statself = StatusMessage.objects.filter(profile=self)
        statfriends = StatusMessage.objects.none()

        for friend in friends:
            statfriends = statfriends | StatusMessage.objects.filter(profile=friend)
        
        stat = statself | statfriends
        stat = stat.order_by('-timestamp')

        return stat

    
    def get_absolute_url(self):
        ''' return the URL to redirect after successfully submitting the form '''
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    ''' encapsulates the status of a user profile on mini-fb '''
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        ''' return a string representation of this object '''
        return f'{self.message}'
    
    def get_images(self):
        ''' return a QuerySet of all images on this status message '''
        images = Image.objects.filter(message=self)
        return images
    
class Image(models.Model):
    ''' encapsulates the idea of an image file '''
    image = models.ImageField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

    def __str__(self):
        ''' return a string representation of this object '''
        return f'{self.message}'
    
class Friend(models.Model):
    ''' encapsulates the idea of a friend relation '''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, blank=False, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, blank=False, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' return a string representation of this object '''
        return f'{self.profile1} & {self.profile2}'