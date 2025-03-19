from django.db import models
from django.contrib.auth.models import User

from .player import Player
from .round import Round
from .game import Game
from .other_models import Referee
from .constants import (TournamentType,
						TournamentSpeed,
						TournamentBoardType,
						RankingSystem)

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
	
	def addToRankingList(self, rankingSystem: RankingSystem.value):
		createdRankingSystem = RankingSystemClass.objects.create(value=rankingSystem)
		self.rankingList.add(createdRankingSystem)

	def getRoundCount(self):
		return Round.objects.filter(tournament=self).count()

	def get_number_of_rounds_with_games(self):
		# Get the tournament rounds
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
		rounds = Round.objects.filter(tournament=self).all()
		
		# Iterate on the rounds
		last_round = None
		last_date = None
		for round in rounds:
			games = Game.objects.filter(round=round).all()

			# Check the round games
			for game in games:
				modified_date = game.update_date != game.start_date

				# If it has a more recent date, save it
				if last_date is None or \
				(modified_date and last_date < game.update_date):
					last_date = game.update_date
					last_round = round
		
		return last_round

class TournamentPlayers(models.Model):
	# Tournament id
	tournament_id = models.ForeignKey(to=Tournament, null=False, blank=False, on_delete=models.CASCADE)

	# Player id
	player_id = models.ForeignKey(to=Player, null=False, blank=True, on_delete=models.CASCADE)

	# Date when the player enter the tournament
	date = models.DateTimeField(auto_now=True)