from django.test import TestCase
from django.urls import reverse

from .models import Player, Score, Game, Turn, GamePlayer
from .views import StartGameForm

class PlayerModelTests(TestCase):
    def test_player_name(self):
        p = Player(name="Wil")
        self.assertIs(p.name, "Wil")

    def test_player_str(self):
        p = Player(name='Ryan')
        self.assertEquals(p.__str__(), 'Ryan')

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

class IndexViewTests(TestCase):
    def test_index_exists(self):
        response = self.client.get(reverse('scores:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_with_no_games(self):
        response = self.client.get(reverse('scores:index'))
        self.assertContains(response, 'No games are recorded')

    def test_index_with_a_game(self):
        g = Game(name="Family Night")
        g.save()
        response = self.client.get(reverse('scores:index'))
        self.assertContains(response, 'Family Night')

class GameViewTests(TestCase):
    def test_game_detail_exists(self):
        g = Game(name='Family Night')
        g.save()
        response = self.client.get(reverse("scores:game", args=(g.id,)))
        self.assertEqual(response.status_code, 200)

class PlayerListViewTests(TestCase):
    def test_player_list_exists(self):
        response = self.client.get(reverse("scores:player_list"))
        self.assertEqual(response.status_code, 200)

    def test_player_list_with_a_player(self):
        p = Player(name="Jupiter")
        p.save()
        response = self.client.get(reverse('scores:player_list'))
        self.assertContains(response, 'Jupiter')

class PlayerViewTests(TestCase):
    def test_player_view_exists(self):
        p = Player(name='Seth')
        p.save()
        response = self.client.get(reverse("scores:player", args=(p.id,)))
        self.assertEqual(response.status_code, 200)

class NewGameViewTests(TestCase):
    def test_new_game_view_exists(self):
        response = self.client.get(reverse('scores:start_game'))
        self.assertEqual(response.status_code, 200)

class StartGameFormTests(TestCase):
    def test_start_two_player_game(self):
        harold = Player(name='Harold')
        harold.save()
        maude = Player(name='Maude')
        maude.save()
        form = StartGameForm({
            'name': 'Movie Night',
            'player0': harold.pk,
            'player1': maude.pk,
        })
        self.assertTrue(form.is_valid())

class CreateGameTests(TestCase):
    def test_create_two_player_game_redirects_to_detail(self):
        stan = Player(name='Stan')
        stan.save()
        oliver = Player(name='Oliver')
        oliver.save()
        response = self.client.post(
            reverse('scores:create_game'),
            data={
                'name': 'Comedy Night',
                'player0': str(stan.pk),
                'player1': str(oliver.pk),
                'player2': '',
                'player3': '',
                'player4': '',
            }
        )
        self.assertEqual(response.status_code, 302)
