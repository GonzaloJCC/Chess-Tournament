from rest_framework import serializers
from .models import (
    Referee,
    Player,
    Game,
    Tournament,
    Round,
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
    class Meta:
        model = Tournament
        fields = "__all__"

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
