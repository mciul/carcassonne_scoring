from django.shortcuts import render
from django.views import generic

from .models import Game, Player

class IndexView(generic.ListView):
    template_name = 'scores/index.html'

    def get_queryset(self):
        """
        Return all games
        """
        return Game.objects.all()


class GameView(generic.DetailView):
    model = Game
    template_name = 'scores/game.html'

class PlayerListView(generic.ListView):
    template_name = 'scores/player_list.html'

    def get_queryset(self):
        """
        Return all players
        """
        return Player.objects.all()

