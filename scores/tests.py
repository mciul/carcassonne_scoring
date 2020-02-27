from django.test import TestCase

from .models import Player, Score, Game, Turn, GamePlayer

class PlayerModelTests(TestCase):
    def test_player_name(self):
        p = Player(name="Wil")
        self.assertIs(p.name, "Wil")

class ScoreModelTests(TestCase):
    def test_score_player(self):
        p = Player(name="Felicia")
        s = Score(player=p)
        self.assertIs(s.player, p)

    def test_score_event(self):
        s = Score(event='road')
        self.assertIs(s.event, 'road')

    def test_score_points(self):
        s = Score(points=2)
        self.assertIs(s.points, 2)

class GameModelTests(TestCase):
    def test_game_name(self):
        g = Game(name="Family Night")
        self.assertIs(g.name, "Family Night")

    def test_game_player_order(self):
        g = Game(name='test')
        g.save()
        p0 = Player(name='Wil')
        p0.save()
        p1 = Player(name='Felicia')
        p1.save()
        p2 = Player(name='Becca')
        p2.save()
        gp1 = GamePlayer(game=g, order=1, player=p1)
        gp1.save()
        gp0 = GamePlayer(game=g, order=0, player=p0)
        gp0.save()
        gp2 = GamePlayer(game=g, order=2, player=p2)
        gp2.save()
        self.assertEqual(g.player_order(), [p0, p1, p2])
    
class TurnModelTests(TestCase):
    def test_turn_number(self):
        t = Turn(number=1)
        self.assertIs(t.number, 1)

class GamePlayerTests(TestCase):
    def test_game_player_order(self):
        gp = GamePlayer(order=3)
        self.assertIs(gp.order, 3)
