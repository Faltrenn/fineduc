from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    cellphone = models.CharField(max_length=11)
    state = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=20, blank=True)


    image = models.ImageField(upload_to="profile-images", blank=True)

    
    bio = models.TextField(blank=True)
    link_youtube = models.CharField(max_length=150, blank=True)
    link_instagram = models.CharField(max_length=150, blank=True)
    link_facebook = models.CharField(max_length=150, blank=True)
    link_linkedin = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.name


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=250)
    amount = models.FloatField()

    def __str__(self) -> str:
        return f"{self.user.username}_req"
