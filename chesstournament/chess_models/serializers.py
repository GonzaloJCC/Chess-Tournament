from rest_framework import serializers
from .models import (
	Referee,
	Player,
	Game,
	Tournament,
	Round
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
	class Meta:
		model = Tournament
		fields = '__all__'

class RoundSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Round
		fields = '__all__'
