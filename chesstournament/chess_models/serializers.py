from rest_framework import serializers
from .models import (
	Referee,
	Player,
	Game,
	Tournament,
	Round,
	RankingSystemClass
)

class RefereeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Referee
		fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
		fields = '__all__'

class TournamentSerializer(serializers.ModelSerializer):

	# Save the players as a string that will be formatted
	players = serializers.CharField(required=False, allow_blank=True)

	# Save the list of the ranking list as an array
	rankingList = serializers.PrimaryKeyRelatedField(
		queryset=RankingSystemClass.objects.all(),
		many=True,
		required=False
	)

	class Meta:
		model = Tournament
		fields = [
			'name',
			'only_administrative',
			'tournament_type',
			'board_type',
			'win_points',
			'draw_points',
			'lose_points',
			'tournament_speed',
			'rankingList',
			'players',
		]
	
	def validate_name(self, value):
		if Tournament.objects.filter(name=value).exists():
			raise serializers.ValidationError("Tournament with this name already exists.")
		return value

class RoundSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Round
		fields = '__all__'
