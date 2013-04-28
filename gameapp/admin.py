from gameapp.models import *
from django.contrib import admin

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'school']
    
class GamedataAdmin(admin.ModelAdmin):
	list_display = ['player_id','school','gameID','gamescore','questions','meters']
	 
admin.site.register(Player,PlayerAdmin)
admin.site.register(Gamedata,GamedataAdmin)

