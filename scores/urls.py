from django.urls import path

from . import views

app_name='scores'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('game/<int:pk>/', views.GameView.as_view(), name='game'),
    path('player/', views.PlayerListView.as_view(), name='player_list'),
]
