from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy
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
    players = Player.objects.all()
    player0 = ModelChoiceField(label = "First Player", queryset=players)
    player1 = ModelChoiceField(label = "Second Player", queryset=players)
    player2 = ModelChoiceField(label = "Third Player", queryset=players,
            required=False)
    player3 = ModelChoiceField(label = "Fourth Player", queryset=players,
            required=False)
    player4 = ModelChoiceField(label = "Fifth Player", queryset=players,
            required=False)
    #TODO: prevent duplicate players
    #TODO: force game name to be unique

def create_game(request):
    name = request.POST['name']
    game = Game(name=name)
    game.save()
    return HttpResponseRedirect(reverse('scores:game', args={game.pk}))

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
