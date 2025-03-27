from django.db import models
from .player import Player
from .round import Round
from .constants import Scores
from .tournament import Tournament
from .other_models import LichessAPIError

import requests

# swissByes not needed, implements ROUNDROBIN case with an even number of players
def create_rounds(tournament: Tournament, swissByes=[]):
    # Get the players and their ids
    players = tournament.players.all()
    players_ids = sorted([player.id for player in players])

    # Select the omve and fixed players
    fixed_player = players_ids[-1]
    moved_players = players_ids[:-1]

    # Iterate, creating duels
    rounds = []
    for i in range(len(players_ids) - 1):
        duels = [fixed_player, moved_players[0]]
        for j in range(1, len(moved_players) // 2 + 1):
            duels.append((fixed_player, moved_players[-j]))
        rounds.append(duels)
        moved_players = [moved_players[-1]] + moved_players[:-1]
    
    # Return the list of the created rounds
    return rounds


class Game(models.Model):

    # White player, deleting on cascade deletes the player games
    white = models.ForeignKey(to=Player, null=True, on_delete=models.CASCADE, related_name="white")

    # Black player
    black = models.ForeignKey(to=Player, null=True, on_delete=models.CASCADE, related_name="black")

    # If the game ended, if true players can not edit the game
    finished = models.BooleanField(default=False)

    # The tournament round
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
            raise LichessAPIError(f"Error fetching game data: {response.status_code}")

        data = response.json()

        # Fixing the inconsistent quotes
        white_player = data['players']['white']['userId']
        if white_player != self.white.lichess_username:
            raise LichessAPIError(f"The player {self.white.lichess_username} is not {white_player}")

        black_player = data['players']['black']['userId']
        if black_player != self.black.lichess_username:
            raise LichessAPIError(f"The player {self.black.lichess_username} is not {black_player}")

        if data['winner'] == 'white':
            game_result = Scores.WHITE
        elif data['winner'] == 'black':
            game_result = Scores.BLACK
        else:
            game_result = Scores.DRAW

        # TODO: Update data?

        return game_result, white_player, black_player

    def __str__(self):
        white_data = f'{str(self.white)}({self.white.id})'
        black_data = f'{str(self.black)}({self.black.id})'
        return f'{white_data} vs {black_data} = {self.result.label}'