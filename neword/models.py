from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Words(models.Model):
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

class UserWords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

class UserWordsNums(models.Model):
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)