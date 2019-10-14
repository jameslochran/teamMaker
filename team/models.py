from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Player(models.Model):
    name = models.CharField(max_length=255)
    # younger = 1 # less than 30 years of age
    # young = 2 # between 30 and 40
    # middle = 3 # between 40 and 50
    # middle_plus = 4 # between 50 and 60
    # old = 5 # 60 plus
    #
    # age_choices = (
    #     (younger, 'Younger'),
    #     (young, 'Young'),
    #     (middle, 'Middle'),
    #     (middle_plus, 'Middle_plus'),
    #     (old,'Old')
    #      )
    age = models.IntegerField(default=3)

    # tall = 1 # above 6'2"
    # average = 2 # between 6'1" and 5'10"
    # short = 3 # below 5'9"
    #
    # height_choices = (
    #     (tall, 'Tall'),
    #     (average, 'Average' ),
    #     (short, 'Short')
    # )

    height = models.IntegerField(default=2)

    def __str__(self):
    	return self.name


class Skills(models.Model):
    # excellent = 1
    # average = 2
    # developing = 3
    # skill_choices = (
    #     (excellent, 'Excellent'),
    #     (average, 'Average'),
    #     (developing, 'Developing'),
    # )
    shooting= models.IntegerField(default=2)
    defense = models.IntegerField(default=2)
    passing = models.IntegerField(default=2)
    rebounding = models.IntegerField(default=2)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
