from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django import forms
from django.forms import ModelChoiceField

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

class StartGameForm(forms.Form):
    name = forms.CharField()
    player0 = ModelChoiceField(queryset=Player.objects.all())
    player1 = ModelChoiceField(queryset=Player.objects.all())
    player2 = ModelChoiceField(queryset=Player.objects.all())
    player3 = ModelChoiceField(queryset=Player.objects.all())
    player4 = ModelChoiceField(queryset=Player.objects.all())

class NewGameView(generic.FormView):
    template_name = 'scores/start_game.html'
    form_class = StartGameForm
    success_url = reverse_lazy('scores:game')

class PlayerListView(generic.ListView):
    template_name = 'scores/player_list.html'

    def get_queryset(self):
        """
        Return all players
        """
        return Player.objects.all()

class PlayerView(generic.DetailView):
    model = Player
    template_name = 'scores/player.html'
