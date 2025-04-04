from django.contrib import admin
from .models import Game, Player, Round, Tournament, Referee

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Round)
admin.site.register(Tournament)
admin.site.register(Referee)
