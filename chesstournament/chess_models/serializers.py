from rest_framework import serializers
from .models import (
    Referee,
    Player,
    Game,
    Tournament,
    Round,
    RankingSystem,
    RankingSystemClass,
)


class RefereeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referee
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class TournamentSerializer(serializers.ModelSerializer):

    rankingList = serializers.ListField(
        child=serializers.CharField(max_length=2),
        required=False
    )
    players = serializers.CharField(required=False)

    class Meta:
        model = Tournament
        fields = "__all__"

    def validate_rankingList(self, values):
        """
        Check that the ranking list is not empty.
        """
        # Check if all values are valid
        invalid_values = [v for v in values if v not in RankingSystem.values]
        if invalid_values:
            raise serializers.ValidationError(
                f"Invalid ranking system values: {', '.join(invalid_values)}"
            )

        # Assign the values into the database
        for value in values:
            search = RankingSystemClass.objects.filter(value=value)
            if len(search) == 0:
                RankingSystemClass.objects.create(value=value)

        return values

    def create(self, validated_data):
        rankingList = validated_data.pop("rankingList", [])
        players_csv = validated_data.pop("players", "")
        tournament = super().create(validated_data)

        # Add players
        if players_csv:
            players = players_csv.split("\n")
            for player_entry in players[1:]:
                player_entry = player_entry.strip()
                if not player_entry:
                    continue

                columns = player_entry.split(",")
                if len(columns) == 1:
                    lichess_username = columns[0].strip()
                    player, _ = Player.objects.get_or_create(
                        lichess_username=lichess_username
                    )
                elif len(columns) == 2:
                    name = columns[0].strip()
                    email = columns[1].strip()
                    player, _ = Player.objects.get_or_create(
                        name=name,
                        email=email
                    )
                else:
                    raise serializers.ValidationError(
                        f"Invalid player format: {player_entry}"
                    )

                tournament.players.add(player)

        # Add the ranking list items
        for current in rankingList:
            search = RankingSystemClass.objects.filter(value=current)
            if len(search):
                tournament.rankingList.add(search[0])

        return tournament

    def to_representation(self, instance):
        # res = super().to_representation(instance)
        res = {}
        res["id"] = instance.id
        res["name"] = instance.name
        res["start_date"] = instance.start_date

        rankingList = instance.rankingList.all()
        res["rankingList"] = []
        for ranking in rankingList:
            res["rankingList"].append(ranking.value)

        # res['rankingList'] = instance.rankingList.all()
        res["board_type"] = instance.board_type
        res["tournament_type"] = instance.tournament_type
        return res


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = "__all__"
