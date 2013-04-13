from django.db import models

# Create your models here.

class Player(models.Model):
	id = models.AutoField(primary_key=True)
	school = models.CharField(max_length=80)

class Gamedata(models.Model):
	player = models.ForeignKey(Player, null=True)
	
	gameID = models.FloatField(max_length=1)
	gamescore = models.IntegerField(max_length=3)
	
	question1 = models.IntegerField(max_length=3)
	question2 = models.IntegerField(max_length=3)
	question3 = models.IntegerField(max_length=3)
	question4 = models.IntegerField(max_length=3)
	question5 = models.IntegerField(max_length=3)
	question6 = models.IntegerField(max_length=3)
	question7 = models.IntegerField(max_length=3)
	question8 = models.IntegerField(max_length=3)
	question9 = models.IntegerField(max_length=3)
	question10 = models.IntegerField(max_length=3)
	
	meter1 = models.IntegerField(max_length=3)
	meter2 = models.IntegerField(max_length=3)
	meter3 = models.IntegerField(max_length=3)
	meter4 = models.IntegerField(max_length=3)
	meter5 = models.IntegerField(max_length=3)
	meter6 = models.IntegerField(max_length=3)
	meter7 = models.IntegerField(max_length=3)
	meter8 = models.IntegerField(max_length=3)
	meter9 = models.IntegerField(max_length=3)
	meter10 = models.IntegerField(max_length=3)
	
	def player_id(self):
		return self.player.id
	player_id.short_description = 'Player ID'
	
	def school(self):
		return self.player.school
	school.short_description = 'School'