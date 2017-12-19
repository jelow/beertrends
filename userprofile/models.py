from django.db import models
from beerdata.models import Beer, Brewery
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):


    user = models.OneToOneField(User, related_name='profile')
    beer_wishlist = models.ManyToManyField(Beer)
    brewery_watchlist = models.ManyToManyField(Brewery)

    def __str__(self):
        return "%s's profile" % self.user

# Automatically create a UserProfile when a User is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Notification(models.Model):


    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    seen = models.BooleanField()
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
