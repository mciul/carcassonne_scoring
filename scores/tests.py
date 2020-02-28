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

    def test_game_player_order_with_one_player(self):
        # this could arguably raise an error since one-player games
        # technically aren't allowed. But for now, I'll leave
        # it as a TODO
        g = Game(name='test')
        g.save()
        p0 = Player(name='Trisha')
        p0.save()
        g.add_player(p0.pk)
        self.assertEqual(len(g.player_order()), 1)

    def test_add_turn_returns_turn_zero_first_time(self):
        g = Game(name='test')
        g.save()
        p1 = Player(name='Fonz')
        p1.save()
        g.add_player(p1.pk)
        p2 = Player(name='Mork')
        p2.save()
        g.add_player(p2.pk)
        got = g.add_turn()
        expected = g.turn_set.get(number=0)
        self.assertEqual(got, expected)

    def test_add_turn_returns_turn_three_fourth_time(self):
        g = Game(name='test')
        g.save()
        p1 = Player(name='Fonz')
        p1.save()
        g.add_player(p1.pk)
        p2 = Player(name='Mork')
        p2.save()
        g.add_player(p2.pk)
        for i in range(3):
            g.add_turn()
        got = g.add_turn()
        expected = g.turn_set.get(number=3)
        self.assertEqual(got, expected)

    def test_current_turn_returns_last_turn_added(self):
        g = Game(name='test')
        g.save()
        p1 = Player(name='Fonz')
        p1.save()
        g.add_player(p1.pk)
        p2 = Player(name='Mork')
        p2.save()
        g.add_player(p2.pk)
        expected = g.add_turn()
        self.assertEqual(g.current_turn(), expected)

    # TODO: test behavior when there are no turns

    def test_turn_number_is_minus_one_with_no_turns(self):
        g = Game(name='test')
        self.assertEqual(g.turn_number(), -1)

    def test_turn_number_is_last_turn_number(self):
        g = Game(name='test')
        g.save()
        p = Player(name='Winston')
        p.save()
        g.add_player(p.pk)
        t = g.turn_set.create(number=41, player=p)
        g.turn_set.create(number=12, player=p)
        self.assertEqual(g.turn_number(), 41)

    def test_current_player_is_first_player_on_first_turn(self):
        g = Game(name='x')
        g.save()
        p1 = Player(name='Scott')
        p1.save()
        g.add_player(p1.pk)
        p2 = Player(name='Jean')
        p2.save()
        g.add_player(p2.pk)
        p3 = Player(name='Charles')
        p3.save()
        g.add_player(p3.pk)
        g.add_turn()
        self.assertEqual(g.current_player(), p1)

    def test_current_player_is_third_three_players_sixth_turn(self):
        g = Game(name='x')
        g.save()
        p1 = Player(name='Scott')
        p1.save()
        g.add_player(p1.pk)
        p2 = Player(name='Jean')
        p2.save()
        g.add_player(p2.pk)
        p3 = Player(name='Charles')
        p3.save()
        g.add_player(p3.pk)
        for i in range(6):
            g.add_turn()
        self.assertEqual(g.current_player(), p3)

    def test_next_player_is_second_player_on_first_turn(self):
        g = Game(name='x')
        g.save()
        p1 = Player(name='Scott')
        p1.save()
        g.add_player(p1.pk)
        p2 = Player(name='Jean')
        p2.save()
        g.add_player(p2.pk)
        p3 = Player(name='Charles')
        p3.save()
        g.add_player(p3.pk)
        g.add_turn()
        self.assertEqual(g.next_player(), p2)

class TurnModelTests(TestCase):
    def test_turn_number(self):
        t = Turn(number=1)
        self.assertIs(t.number, 1)

    def test_turn_str(self):
        g = Game()
        g.save()
        p = Player()
        p.save()
        t = Turn(number=1, game_id=g.pk, player_id=p.pk)
        expected = "number=1, game_id=%d, player_id=%d" % (
            g.pk, p.pk
        )
        self.assertEqual(t.__str__(), expected)

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
        p = Player(name='Homer')
        p.save()
        g.add_player(p.pk)
        response = self.client.get(reverse("scores:game", args=(g.id,)))
        self.assertEqual(response.status_code, 200)

    def test_game_detail_lists_players(self):
        john = Player(name="John")
        john.save()
        paul = Player(name="Paul")
        paul.save()
        george = Player(name="George")
        george.save()
        ringo = Player(name="Ringo")
        ringo.save()
        g = Game(name='Beat Night')
        g.save()
        for i, p in enumerate([john, paul, george, ringo]):
            gp = GamePlayer(player_id=p.pk, game_id=g.pk, order=i)
            gp.save()
        response = self.client.get(reverse("scores:game", args=(g.pk,)))
        self.assertContains(response, "John, Paul, George, Ringo")

    def test_game_detail_shows_turn_number(self):
        g = Game(name='test')
        g.save()
        p = Player(name='Arthur')
        p.save()
        g.add_player(p.pk)
        t = g.turn_set.create(number=42, player=p)
        response = self.client.get(reverse("scores:game", args=(g.pk,)))
        self.assertContains(response, "Turn 42")

    def test_game_detail_shows_current_player(self):
        g = Game(name='test')
        g.save()
        p = Player(name='Arthur')
        p.save()
        g.add_player(p.pk)
        response = self.client.get(reverse("scores:game", args=(g.pk,)))
        self.assertContains(response, "Arthur's turn")

    def test_game_detail_has_next_turn_button(self):
        g = Game(name='test')
        g.save()
        p = Player(name='Arthur')
        p.save()
        g.add_player(p.pk)
        response = self.client.get(reverse("scores:game", args=(g.pk,)))
        expected = '<input type="submit" value="Next Turn">'
        self.assertContains(response, expected, html=True)


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
    def test_create_two_player_game_redirects(self):
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
        game = Game.objects.get(name='Comedy Night')
        self.assertRedirects(response, reverse('scores:game', args=(game.pk,)))

    def test_create_two_player_game_orders_players(self):
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
        game = Game.objects.get(name='Comedy Night')
        players = game.player_order()
        self.assertEqual(players, [stan, oliver])

    def test_create_game_with_turn_number_zero(self):
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
        game = Game.objects.get(name='Comedy Night')
        self.assertEqual(game.turn_number(), 0)

class NextTurnTests(TestCase):
    def test_next_turn_adds_turn(self):
        harold = Player(name='Harold')
        harold.save()
        maude = Player(name='Maude')
        maude.save()
        g = Game(name='Movie Night')
        g.save()
        g.add_player(harold.pk)
        g.add_player(maude.pk)
        g.add_turn()
        response = self.client.post(
            reverse('scores:next_turn', args=[g.pk,]),
        )
        self.assertEqual(g.turn_number(), 1)

class AddTurnScoreTests(TestCase):
    def test_add_monastery_score(self):
        harold = Player(name='Harold')
        harold.save()
        maude = Player(name='Maude')
        maude.save()
        g = Game(name='Movie Night')
        g.save()
        g.add_player(harold.pk)
        g.add_player(maude.pk)
        g.add_turn()
        response = self.client.post(
            reverse('scores:add_turn_score', args=[g.pk,]),
            data={
                'add_monastery_score': "Completed Monastery",
                'player': str(harold.pk)
            }
        )
        s = g.current_turn().scores.get(player_id=harold.pk)
        self.assertEqual(s.points, 9)

    def test_add_road_score(self):
        harold = Player(name='Harold')
        harold.save()
        maude = Player(name='Maude')
        maude.save()
        g = Game(name='Movie Night')
        g.save()
        g.add_player(harold.pk)
        g.add_player(maude.pk)
        g.add_turn()
        response = self.client.post(
            reverse('scores:add_turn_score', args=[g.pk,]),
            data={
                'add_road_score': "Completed Road",
                'player': str(maude.pk),
                'tiles': "2",
            }
        )
        s = g.current_turn().scores.get(player_id=maude.pk)
        self.assertEqual(s.points, 2)
