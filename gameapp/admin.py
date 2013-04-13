from gameapp.models import *
from django.contrib import admin

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'school']

class GamedataAdmin(admin.ModelAdmin):
	list_display = ['player','gameID','gamescore','question1','question2','question3','question4','question5','question6','question7','question8','question9','question10',
	'meter1','meter2','meter3','meter4','meter5','meter6','meter7','meter8','meter9','meter10']
	 
admin.site.register(Player,PlayerAdmin)
admin.site.register(Gamedata,GamedataAdmin)

