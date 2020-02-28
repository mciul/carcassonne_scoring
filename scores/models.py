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
    ended = models.BooleanField(default=False)

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

    def is_ended(self):
        return self.ended

    def current_turn(self):
        #TODO: handle the case when there are no turns
        return self.turn_set.order_by('number').reverse()[0]

    def score_completed_monastery(self, player_id):
        #TODO: handle the case when there are no turns here too?
        return self.current_turn().scores.create(
            event='monastery',
            player_id=player_id,
            points=9
        )

    def score_incomplete_monastery(self, player_id, tiles):
        return self.final_scores.create(
            event='monastery',
            player_id=player_id,
            points=int(tiles)
        )

    def score_completed_road(self, player_id, tiles):
        return self.current_turn().scores.create(
            event='road',
            player_id=player_id,
            points=int(tiles)
        )

    def score_incomplete_road(self, player_id, tiles):
        return self.final_scores.create(
            event='road',
            player_id=player_id,
            points=int(tiles)
        )

    def score_completed_city(self, player_id, tiles, coats_of_arms):
        return self.current_turn().scores.create(
            event='city',
            player_id=player_id,
            points=(int(tiles) + int(coats_of_arms))*2
        )

    def score_incomplete_city(self, player_id, tiles, coats_of_arms):
        return self.final_scores.create(
            event='city',
            player_id=player_id,
            points=int(tiles) + int(coats_of_arms)
        )

    def total_scores(self):
        return [ [p, self.total_score(p)] for p in self.player_order() ]

    def total_score(self, player):
        total = 0
        for t in self.turn_set.all():
            for s in t.scores.filter(player_id = player.pk):
                total += s.points
        return total

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
