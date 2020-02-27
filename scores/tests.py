from django.test import TestCase

from .models import Player

class PlayerModelTests(TestCase):
    def test_player_name(self):
        p = Player(name="Wil")
        self.assertIs(p.name, "Wil")
