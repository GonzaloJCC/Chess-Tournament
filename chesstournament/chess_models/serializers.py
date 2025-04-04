from rest_framework import serializers
from .models import (
	Referee,
	Player,
	Game,
	Tournament,
	Round,
	RankingSystemClass,

	TournamentBoardType,
	TournamentPlayers
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
		"""
		Check that any tournament with the same name exist.
		"""
		if Tournament.objects.filter(name=value).exists():
			raise serializers.ValidationError("Tournament with this name already exists.")
		return value
	
	def validate(self, data):
		board_type: str = data.get('board_type')
		player_csv: str = data.get('players')
		parsed_players = []

		if not player_csv or len(player_csv.split()) == 0:
			data['parsed_players'] = []
			return data

		# Divide the string into lines
		lines = player_csv.strip().splitlines()
		if not lines:
			raise serializers.ValidationError("Invalid player CSV format")
		if len(lines) < 2:
			raise serializers.ValidationError("No usernames provided")
		users_data = [line.strip() for line in lines[1:] if line.strip()]

		
		# Depending on the board, we stop the information in one way or another
		if board_type == TournamentBoardType.LICHESS:
			
			# Check if all the users are registered on the database
			found_players = Player.objects.filter(lichess_username__in=users_data)
			if not found_players or found_players.count() != len(users_data):
				raise serializers.ValidationError("No players found with the provided usernames")
			
			# Save the players
			parsed_players = list(found_players)

			
		elif board_type == TournamentBoardType.OTB:
			for row in users_data:
				name, email = row.split(',')
				name = name.strip()
				email = email.strip()

				player = Player.objects.filter(name=name, email=email).first()
				if not player:
					raise serializers.ValidationError(
						f"Player with name '{name}' and email '{email}' not found"
					)
				
				parsed_players.append(player)
		else:
			raise serializers.ValidationError("Invalid board type")

		# Save the players
		data['parsed_players'] = parsed_players
		return data
	
	def create(self, validated_data):
		# Get the players
		parsed_players = validated_data.pop('parsed_players', [])
		validated_data.pop('players', None)

		# Get the ranking list
		ranking_list = validated_data.pop('rankingList', [])

		# Get the auth user
		request = self.context.get('request')
		auth_user = request.user if request else None

		# Create the tournament
		tournament = Tournament.objects.create(administrativeUser=auth_user, **validated_data)

		# Add the ranking list
		tournament.rankingList.set(ranking_list)

		# Add the players
		for player in parsed_players:
			TournamentPlayers.objects.create(tournament=tournament, player=player)
		
		return tournament
	
	def to_representation(self, instance):
		# res = super().to_representation(instance)
		res = {}
		res['id'] = instance.id
		res['name'] = instance.name
		res['start_date'] = instance.start_date

		rankingList = instance.rankingList.all()
		res['rankingList'] = []
		for ranking in rankingList:
			res['rankingList'].append(ranking.value)

		# res['rankingList'] = instance.rankingList.all()
		res['board_type'] = instance.board_type
		res['tournament_type'] = instance.tournament_type
		return res

class RoundSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Round
		fields = '__all__'
