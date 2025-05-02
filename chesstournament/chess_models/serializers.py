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
        return values

    def create(self, validated_data):
        rankingList = validated_data.pop("rankingList", [])
        tournament = super().create(validated_data)

        # Add the ranking list items
        for current in rankingList:
            ranking = RankingSystemClass.objects.create(
                tournament=tournament,
                value=current
            )
            tournament.rankingList.add(ranking)

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
