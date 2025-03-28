from django.db import models
from django.contrib.auth.models import User

from .player import Player
from .other_models import Referee
from .constants import (TournamentType,
						TournamentSpeed,
						TournamentBoardType,
						RankingSystem,
						Scores)

class RankingSystemClass(models.Model):
	value = models.CharField(
		max_length=2,
		choices=RankingSystem.choices,
		primary_key=True
	)

class Tournament(models.Model):
	# Tournament name. Can be null or blank, and must be unique
	name = models.CharField(max_length=128, null=True, blank=True, unique=True)

	# Admin user reference. Can be null
	administrativeUser = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)

	# Players references
	players = models.ManyToManyField(to=Player, through='TournamentPlayers', blank=True) # null=True has no effects

	# Referee reference
	referee = models.ForeignKey(to=Referee, null=True, on_delete=models.CASCADE)

	# Start date
	start_date = models.DateField(auto_now=True, null=True)

	# End date
	end_date = models.DateField(null=True)

	# Max time (seconds) to update the results from Lichess
	max_update_time = models.IntegerField(default=43200)

	# Bool to check if the admin can modify a match
	only_administrative = models.BooleanField(default=False)

	# Tournament type, options of TournamentType
	tournament_type = models.CharField(choices=TournamentType.choices, max_length=2)

	# Tournament speed, options of TournamentSpeed
	tournament_speed = models.CharField(choices=TournamentSpeed.choices, max_length=2)

	# Tournament board type, options by TournamentBoardType
	board_type = models.CharField(choices=TournamentBoardType.choices, max_length=3)

	# Points got by win
	win_points = models.FloatField(default=1.0)

	# Points got by draw
	draw_points = models.FloatField(default=0.5)

	# Points got by lose
	lose_points = models.FloatField(default=0.0)

	# Time control used on the tournament
	timeControl = models.CharField(max_length=32, default="15+0")

	# Number of rounds for swiss
	number_of_rounds_for_swiss = models.IntegerField(default=0)

	# List of classification system, associated with a tournament through the tournament ranking system
	rankingList = models.ManyToManyField(to=RankingSystemClass, blank=True) # null=True has no effects

	def __str__(self):
		return f"tournament_{self.id:02d}"

	def getPlayers(self, sorted=False):
		# Get all the players	
		players = self.players.all()

		# Check if the sorted is set
		if not sorted:
			return list(players)

		# Map to avoid if-elif-elif...
		rating_type_mapping = {
			TournamentSpeed.BLITZ: "blitz",
			TournamentSpeed.RAPID: "rapid",
			TournamentSpeed.CLASSICAL: "classical",
			TournamentSpeed.BULLET: "bullet",
		}

		# Check the tournament speed
		rating_type = rating_type_mapping.get(self.tournament_speed, "bullet")

		# Check what classification must be used (lichess or fide)
		if self.board_type == TournamentBoardType.LICHESS:
			rating_attr = f"lichess_rating_{rating_type}"
		else:
			rating_attr = f"fide_rating_{rating_type}"

		# Sort players by the classification
		return sorted(players, key=lambda player: getattr(player, rating_attr, 0), reverse=True)

	def getPlayersCount(self):
		return self.players.all().count()
	
	def cleanRankingList(self):
		self.rankingList.clear()
	
	def addToRankingList(self, rankingSystem):
		createdRankingSystem = RankingSystemClass.objects.create(value=rankingSystem)
		self.rankingList.add(createdRankingSystem)

	def getRoundCount(self):
		from .round import Round
		return Round.objects.filter(tournament=self).count()

	def get_number_of_rounds_with_games(self):
		# Get the tournament rounds
		from .round import Round
		from .game import Game
		rounds = Round.objects.filter(tournament=self).all()

		# For each round, check if any game has finished
		count = 0
		for round in rounds:
			# Get all the games
			games = Game.objects.filter(round=round).all()

			# Check if anyone has finished
			for game in games:
				if game.finished:
					count += 1
					break
		return count
	
	def get_latest_round_with_games(self):
		from .round import Round
		from .game import Game
		rounds = Round.objects.filter(tournament=self).all()
		
		# Iterate on the rounds
		last_round = None
		last_date = None
		for round in rounds:
			games = Game.objects.filter(round=round).all()

			# Check the round games
			for game in games:
				# If it has a more recent date, save it
				if last_date is None or last_date < game.update_date:
					last_date = game.update_date
					last_round = round
		
		return last_round

class TournamentPlayers(models.Model):
	# Tournament id
	tournament = models.ForeignKey(to=Tournament, null=False, blank=False, on_delete=models.CASCADE)

	# Player id
	player = models.ForeignKey(to=Player, null=False, blank=False, on_delete=models.CASCADE)

	# Date when the player enter the tournament
	date = models.DateTimeField(auto_now=True)

	class Meta:
			unique_together = ('tournament', 'player')

# TODO:

def get_wins(tournament: Tournament, player: Player):		# returns the points, the wins and the times played as black
	from .round import Round
	from .game import Game
	countWins = 0
	points = 0
	countBlack = 0
	for round in Round.objects.filter(tournament=tournament).all():
		for game in Game.objects.filter(round=round).all():
			#check if he wins as black, as white or loses
			if player not in [game.black, game.white] or game.finished is False or game.result == Scores.NOAVAILABLE:
				continue

			if game.result == Scores.DRAW:
				points += tournament.draw_points
			elif game.white == player and game.result == Scores.WHITE:
				points += tournament.win_points
				countWins += 1
			elif game.black == player and game.result == Scores.BLACK:
				points += tournament.win_points
				countWins += 1
			elif game.result == Scores.BYE_H:
				points += 0.5
			elif game.result == Scores.BYE_F:
				points += 1
			elif game.result == Scores.BYE_U:
				points += 1
			elif game.result == Scores.BYE_Z:
				points += 0
			elif game.result == Scores.FORFEITWIN:
				points += tournament.win_points


			else:
				points += tournament.lose_points

			if game.black == player:
				countBlack += 1

	return points, countWins, countBlack

def getScores(tournament: Tournament):
	result_dict = dict()

	# Get the players
	players = tournament.getPlayers()

	# Get the methods to check
	rankingList = tournament.rankingList.all()

	for player in players:
		result_dict[player] = {}

		score, _, _ = get_wins(tournament, player)
		result_dict[player][RankingSystem.PLAIN_SCORE] = score

	return result_dict

# TODO: 
def getBlackWins(tournament, results):
	# hacer un diccionario
	_, wins, blackTimes = get_wins(tournament, player)
	WINS = RankingSystem.WINS.value
	BLACKTIMES = RankingSystem.BLACKTIMES.value
	result_dict = dict()
	return_dicts = dict()
	for player in

# TODO: 
def getRanking(tournament):
	pass