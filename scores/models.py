from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Score(models.Model):
    event = models.CharField(max_length=10) # road, city, monastery, or field
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

class Game(models.Model):
    name = models.CharField(max_length=200)
    final_scores = models.ManyToManyField(Score, blank=True)

    def player_order(self):
        gps = self.gameplayer_set.order_by('order')
        return [ gp.player for gp in gps ]

    def turn_number(self):
        turns = self.turn_set.order_by('number')
        if len(turns) == 0:
            return -1
        else:
            return turns.reverse()[0].number

    def current_player(self):
        players = self.player_order()
        player_count = len(players)
        turn = self.turn_number()
        return players[turn % player_count]

    def next_player(self):
        players = self.player_order()
        player_count = len(players)
        turn = self.turn_number()
        return players[(turn + 1) % player_count]

    def add_player(self, player_id):
        player_count = GamePlayer.objects.filter(game_id = self.pk).count()
        gp = GamePlayer(
            game_id=self.pk,
            player_id=player_id,
            order=player_count + 1
        )
        gp.save()

    def add_turn(self):
        return self.turn_set.create(
            player_id = self.next_player().pk,
            number = self.turn_number() + 1
        )

class Turn(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    scores = models.ManyToManyField(Score)

    def __str__(self):
        return "number=%d, game_id=%d, player_id=%d" % (
            self.number, self.game_id, self.player_id
        )

class GamePlayer(models.Model):
    order = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
