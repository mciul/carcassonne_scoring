from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy
from django import forms
from django.forms import ModelChoiceField

from .models import Game, Player, GamePlayer

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
    for i in range(5):
        k = "player%d" % i
        v = request.POST[k]
        if v != '':
            player_id = int(v)
            gp = GamePlayer(player_id=player_id, game_id=game.pk, order=i)
            gp.save()
            #TODO: handle invalid player id
    game.add_turn()
    return HttpResponseRedirect(reverse('scores:game', args={game.pk}))

def next_turn(request, game_id):
    game = Game.objects.get(pk=game_id)
    game.add_turn()
    return HttpResponseRedirect(reverse('scores:game', args=(game.pk,)))

def add_turn_score(request, game_id):
    game = Game.objects.get(pk=game_id)
    if 'add_monastery_score' in request.POST:
        add_monastery_score(request, game)
    elif 'add_road_score' in request.POST:
        add_road_score(request, game)
    elif 'add_city_score' in request.POST:
        add_city_score(request, game)
    return HttpResponseRedirect(reverse('scores:game', args=(game.pk,)))

def add_monastery_score(request, game):
    pid = request.POST['player']
    return game.current_turn().scores.create(
        event='monastery',
        player_id=pid,
        points=9
    )


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
