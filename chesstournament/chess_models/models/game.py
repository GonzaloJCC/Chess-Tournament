from django.db import models
from .player import Player
from .round import Round
from .constants import Scores, ScoresFromValue
from .tournament import Tournament
from .other_models import LichessAPIError

import requests

# swissByes not needed,
# implements ROUNDROBIN case with an even number of players
def create_rounds(tournament: Tournament, swissByes=[]):
    players = tournament.players.all()
    players_count = len(players)

    if players_count % 2 != 0 or players_count < 2:
        return []

    players_id = sorted([player.id for player in players])
    fixed = players_id[-1]
    others = players_id[:-1]

    schedule = []
    num_rounds = players_count - 1
    rot = players_count // 2 - 1

    for r in range(num_rounds):
        round = []

        # Save the fixed player. Check if he is white ot black
        if r % 2 == 0:
            first_pair = [others[0], fixed]
        else:
            first_pair = [fixed, others[0]]
        round.append(first_pair)
        
        # Rest of players
        L = others[1:]
        m = len(L)
        for i in range(m // 2):
            pair = [L[i], L[-(i + 1)]]
            round.append(pair)
        schedule.append(round)
        
        # Rote the positions
        rot_amt = rot % len(others)
        others = others[-rot_amt:] + others[:-rot_amt]

    # Create the rounds
    round_count = 0
    for round_data in schedule:
        round_count += 1

        # Create the round
        round = Round.objects.create(
            name=f'Round {round_count}',
            tournament=tournament
        )

        # Insert the games on the round
        for game_data in round_data:
            # Create the game
            game = Game.objects.create(
                white=Player.objects.get(id=game_data[0]),
                black=Player.objects.get(id=game_data[1]),
                round=round
            )
            game.save()

        # Save the round
        round.save()

    # Return the data
    return schedule


class Game(models.Model):

    # White player, deleting on cascade deletes the player games
    white = models.ForeignKey(
        to=Player, null=True, on_delete=models.CASCADE, related_name="white"
    )

    # Black player
    black = models.ForeignKey(
        to=Player, null=True, on_delete=models.CASCADE, related_name="black"
    )

    # If the game ended, if true players can not edit the game
    finished = models.BooleanField(default=False)

    # The tournament round
    round = models.ForeignKey(to=Round, null=False, on_delete=models.CASCADE)

    # The start date and time of the game
    start_date = models.DateTimeField(auto_now_add=True)

    # Date and time of the last update
    update_date = models.DateTimeField(auto_now=True)

    # The result of the match,
    # the possible values are defined in Scores.choices
    result = models.CharField(default=Scores.NOAVAILABLE, max_length=1)

    # The ranking order of the game, can be null
    rankingOrder = models.IntegerField(default=0, null=True)

    # Returns the game result, the white player and the black player
    def get_lichess_game_result(self, game_id):

        response = requests.get(f"https://lichess.org/api/game/{game_id}")

        if response.status_code != 200:
            # Handle unsuccessful response
            raise LichessAPIError(
                f"Error fetching game data: {response.status_code}"
            )

        data = response.json()

        # Fixing the inconsistent quotes
        white_player = data["players"]["white"]["userId"]
        if white_player != self.white.lichess_username:
            raise LichessAPIError(
                f"The player {self.white.lichess_username}"
                f" is not {white_player}"
            )

        black_player = data["players"]["black"]["userId"]
        if black_player != self.black.lichess_username:
            raise LichessAPIError(
                f"The player {self.black.lichess_username}"
                f" is not {black_player}"
            )

        if data.get("winner") is not None:
            if data["winner"] == "white":
                game_result = Scores.WHITE
            elif data["winner"] == "black":
                game_result = Scores.BLACK
        elif data["status"] == "draw":
            game_result = Scores.DRAW

        return game_result, white_player, black_player

    def __str__(self):
        if self.white is None:
            white_data = "BYE"
        else:
            white_data = f"{str(self.white)}({self.white.id})"

        if self.black is None:
            black_data = "BYE"
        else:
            black_data = f"{str(self.black)}({self.black.id})"

        x = ScoresFromValue.get(self.result, "NOT_DEFINED")

        return f"{white_data} vs {black_data} = {x}"
