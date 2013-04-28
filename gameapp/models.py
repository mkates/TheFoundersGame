from django.db import models

# Create your models here.

class Player(models.Model):
	id = models.AutoField(primary_key=True)
	school = models.CharField(max_length=80)

class Gamedata(models.Model):
	player = models.ForeignKey(Player, null=True)
	
	gameID = models.FloatField(max_length=1)
	gamescore = models.IntegerField(max_length=3)
	
	questions = models.CharField(max_length=80)
	meters = models.CharField(max_length=80)
	
	def player_id(self):
		return self.player.id
	player_id.short_description = 'Player ID'
	
	def school(self):
		return self.player.school
	school.short_description = 'School'