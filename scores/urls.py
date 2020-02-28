from django.urls import path

from . import views

app_name='scores'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('game/<int:pk>/', views.GameView.as_view(), name='game'),
    path('player/', views.PlayerListView.as_view(), name='player_list'),
    path('player/<int:pk>/', views.PlayerView.as_view(), name='player'),
    path('start_game', views.NewGameView.as_view(), name='start_game'),
    path('create_game', views.create_game, name='create_game'),
    path('game/<int:game_id>/next_turn', views.next_turn, name='next_turn'),
    path('game/<int:game_id>/end', views.end_game, name='end_game'),
    path(
        'game/<int:game_id>/add_turn_score',
        views.add_turn_score,
        name='add_turn_score'
    ),
]
