from django.db import models
from .player import Player
from .round import Round
from constants import Scores

import requests

# swissByes not needed, implements ROUNDROBIN case with an even number of players
def create_rounds(tournament, swissByes=[]):
    ... # TODO: this function


class Game(models.Model):

    # White player, deleting on cascade deletes the player games
    white = models.ForeignKey(to=Player, null=True, on_delete=models.CASCADE)

    # Black player
    black = models.ForeignKey(to=Player, null=True, on_delete=models.CASCADE)

    # If the game ended, if true players can not edit the game
    finished = models.BooleanField(default=False)

    # The tournament round, delete mode = ? # TODO: deletemode?
    round = models.ForeignKey(to=Round, null=False, on_delete=models.CASCADE)

    # The start date and time of the game
    start_date = models.DateTimeField(auto_now_add=True)

    # Date and time of the last update
    update_date = models.DateTimeField(auto_now=True)

    # The result of the match, the possible values are defined in Scores.choices
    result = models.CharField(default=Scores.NOAVAILABLE, max_length=1)

    # The ranking order of the game, can be null
    rankingOrder = models.IntegerField(default=0, null=True)

    # Returns the game result, the white player and the black player
    def get_lichess_game_result(self, game_id):

        response = requests.get(f'https://lichess.org/api/game/{game_id}')

        if response.status_code != 200:
            # Handle unsuccessful response
            raise Exception(f"Error fetching game data: {response.status_code}")

        data = response.json()

        # Fixing the inconsistent quotes
        white_player = data['players']['white']
        black_player = data['players']['black']

        if data['winner'] == 'white':
            game_result = Scores.WHITE
        elif data['winner'] == 'black':
            game_result = Scores.BLACK
        else:
            game_result = Scores.DRAW

        return game_result, white_player, black_player

    def __str__(self):
    	return f"{self.rankingOrder}"