from django.db import models
from django.contrib.auth.models import User
from datetime import date

#This is a test of the migration
class Player(models.Model):
    name = models.CharField(max_length=255)

    age = models.IntegerField(default=3)


    height = models.IntegerField(default=2)

    def __str__(self):
    	return self.name


class Skills(models.Model):

    shooting= models.IntegerField(default=2)
    defense = models.IntegerField(default=2)
    passing = models.IntegerField(default=2)
    rebounding = models.IntegerField(default=2)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
