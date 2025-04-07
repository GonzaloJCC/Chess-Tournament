from django.test import TestCase, tag, TransactionTestCase

from rest_framework import status
from rest_framework.test import APIClient

from chess_models.models import (
    Player,
    Game,
    Round,
    Scores,
    Tournament,
    TournamentType,
    RankingSystem,
    RankingSystemClass,
    TournamentSpeed,
    TournamentBoardType,
    LICHESS_USERS,
    LichessAPIError,
    get_wins,
    create_rounds,
)
from chess_models.serializers import TournamentSerializer
from django.contrib.auth.models import User
from chess_models.management.commands.constants import (
    playerListCasita,
    casitaResults
)


from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch

URLTOURNAMENT = "/api/v1/tournaments/"
URLCREATETOURNAMENT = "/api/v1/tournament_create/"
URLSEARCH = "/api/v1/searchTournaments/"
GETPLAYERS = "/api/v1/get_players/"
GETROUNDSRESULTS = "/api/v1/get_round_results/"
ADMINUPDATEGAME = "/api/v1/admin_update_game/"


class ExtraTests(TestCase):

    @tag("continua")
    def test_check_lichess_user_exists(self):
        """Return false if player does not exist in lichess"""

        # Create a player with no lichess username
        player = Player.objects.create(
            name="John Doe",
            email="john@example.com"
        )

        # Assert False
        self.assertFalse(player.check_lichess_user_exists())

    @tag("continua")
    def test_game_get_result_from_lichess_black(self):
        """given a lichess game_id get the result of the game
        This function should connect to the lichess API
        """
        tournament_name = "tournament_01"
        tournament1 = Tournament.objects.create(
            name=tournament_name,
            tournament_type=TournamentType.DOUBLEROUNDROBIN
        )
        # create round
        round_name = "round_01"
        round1 = Round.objects.create(name=round_name, tournament=tournament1)

        players = []
        player = Player.objects.create(lichess_username="luizz04")
        # tournament1.players.add(player)
        players.append(player)
        player = Player.objects.create(lichess_username="lexorg55")
        # tournament1.players.add(player)
        players.append(player)

        game = Game.objects.create(round=round1)
        game.white = players[0]
        game.black = players[1]
        game.save()
        winner, white, black = game.get_lichess_game_result("lOuw2i6r")
        self.assertEqual(white, players[0].lichess_username)
        self.assertEqual(black, players[1].lichess_username)
        self.assertEqual(winner.lower(), Scores.DRAW.value)

        game.white = players[1]
        game.black = players[0]
        game.save()
        winner, white, black = game.get_lichess_game_result("Df4Kwb96abwJ")
        self.assertEqual(winner.lower(), Scores.BLACK.value)

        ######################################################################

        tournament_name = "tournament_013"
        tournament13 = Tournament.objects.create(
            name=tournament_name,
            tournament_type=TournamentType.DOUBLEROUNDROBIN
        )
        round_name = "round_013"
        round13 = Round.objects.create(
            name=round_name, tournament=tournament13
        )
        player2 = Player.objects.create(lichess_username="trallegas101")
        game = Game.objects.create(round=round13)
        game.white = players[1]
        game.black = player2

        with self.assertRaises(LichessAPIError) as context:
            game.get_lichess_game_result("hYBj9cvA8TTC")
        self.assertIn(
            "Players for game hYBj9cvA8TTC are different",
            str(context.exception)
        )

    @tag("continua")
    def test_print_error(self):
        x = LichessAPIError(".")
        self.assertIn(str(x), ".")

    @tag("continua")
    def test_bye(self):
        tournament = Tournament.objects.create(
            name="Test Tournament",
            win_points=1, draw_points=0.5, lose_points=0
        )
        round1 = Round.objects.create(name="Round 1", tournament=tournament)

        player1 = Player.objects.create(lichess_username="luizz04")
        player2 = Player.objects.create(lichess_username="Player2")

        Game.objects.create(
            white=player1,
            black=player2,
            round=round1,
            finished=True,
            result=Scores.BYE_H,
        )
        Game.objects.create(
            white=player1,
            black=player2,
            round=round1,
            finished=True,
            result=Scores.BYE_F,
        )
        Game.objects.create(
            white=player1,
            black=player2,
            round=round1,
            finished=True,
            result=Scores.BYE_Z,
        )

        points, wins, black_games = get_wins(tournament, player1)
        self.assertEqual(points, 1.5)  # 0.5 + 1 + 0
        self.assertEqual(wins, 0)
        self.assertEqual(black_games, 0)


class CreateRoundTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create the people
        players = []
        count = 1
        for i in range(14):
            player = Player.objects.create(name=f"Player {count}")
            count += 1
            players.append(player)

        # Create the tournaments
        cls.tournaments = []
        for i in range(6):
            tournament = Tournament.objects.create(
                name=f"Test Tournament {i}",
            )

            max_players = i * 2 + 4
            for player in players:
                if player.id > max_players:
                    break
                tournament.players.add(player)

            tournament.save()
            cls.tournaments.append(tournament)

    @tag("continua")
    def test_001_create_round_4(self):
        """Test the creation of a round with 4 players"""
        result = [[[1, 4], [2, 3]], [[4, 3], [1, 2]], [[2, 4], [3, 1]]]

        create_round = create_rounds(self.tournaments[0])
        self.assertEqual(create_round, result)

    @tag("continua")
    def test_002_create_round_6(self):
        """Test the creation of a round with 6 players"""

        result = [
            [[1, 6], [2, 5], [3, 4]],
            [[6, 4], [5, 3], [1, 2]],
            [[2, 6], [3, 1], [4, 5]],
            [[6, 5], [1, 4], [2, 3]],
            [[3, 6], [4, 2], [5, 1]],
        ]

        create_round = create_rounds(self.tournaments[1])
        self.assertEqual(create_round, result)

    @tag("continua")
    def test_003_create_round_8(self):
        """Test the creation of a round with 8 players"""

        result = [
            [[1, 8], [2, 7], [3, 6], [4, 5]],
            [[8, 5], [6, 4], [7, 3], [1, 2]],
            [[2, 8], [3, 1], [4, 7], [5, 6]],
            [[8, 6], [7, 5], [1, 4], [2, 3]],
            [[3, 8], [4, 2], [5, 1], [6, 7]],
            [[8, 7], [1, 6], [2, 5], [3, 4]],
            [[4, 8], [5, 3], [6, 2], [7, 1]],
        ]

        create_round = create_rounds(self.tournaments[2])
        self.assertEqual(create_round, result)

    @tag("continua")
    def test_004_create_round_10(self):
        """Test the creation of a round with 10 players"""

        result = [
            [[1, 10], [2, 9], [3, 8], [4, 7], [5, 6]],
            [[10, 6], [7, 5], [8, 4], [9, 3], [1, 2]],
            [[2, 10], [3, 1], [4, 9], [5, 8], [6, 7]],
            [[10, 7], [8, 6], [9, 5], [1, 4], [2, 3]],
            [[3, 10], [4, 2], [5, 1], [6, 9], [7, 8]],
            [[10, 8], [9, 7], [1, 6], [2, 5], [3, 4]],
            [[4, 10], [5, 3], [6, 2], [7, 1], [8, 9]],
            [[10, 9], [1, 8], [2, 7], [3, 6], [4, 5]],
            [[5, 10], [6, 4], [7, 3], [8, 2], [9, 1]],
        ]

        create_round = create_rounds(self.tournaments[3])
        self.assertEqual(create_round, result)

    @tag("continua")
    def test_005_create_round_12(self):
        """Test the creation of a round with 12 players"""

        result = [
            [[1, 12], [2, 11], [3, 10], [4, 9], [5, 8], [6, 7]],
            [[12, 7], [8, 6], [9, 5], [10, 4], [11, 3], [1, 2]],
            [[2, 12], [3, 1], [4, 11], [5, 10], [6, 9], [7, 8]],
            [[12, 8], [9, 7], [10, 6], [11, 5], [1, 4], [2, 3]],
            [[3, 12], [4, 2], [5, 1], [6, 11], [7, 10], [8, 9]],
            [[12, 9], [10, 8], [11, 7], [1, 6], [2, 5], [3, 4]],
            [[4, 12], [5, 3], [6, 2], [7, 1], [8, 11], [9, 10]],
            [[12, 10], [11, 9], [1, 8], [2, 7], [3, 6], [4, 5]],
            [[5, 12], [6, 4], [7, 3], [8, 2], [9, 1], [10, 11]],
            [[12, 11], [1, 10], [2, 9], [3, 8], [4, 7], [5, 6]],
            [[6, 12], [7, 5], [8, 4], [9, 3], [10, 2], [11, 1]],
        ]

        create_round = create_rounds(self.tournaments[4])
        self.assertEqual(create_round, result)

    @tag("continua")
    def test_006_create_round_14(self):
        """Test the creation of a round with 14 players"""

        result = [
            [[1, 14], [2, 13], [3, 12], [4, 11], [5, 10], [6, 9], [7, 8]],
            [[14, 8], [9, 7], [10, 6], [11, 5], [12, 4], [13, 3], [1, 2]],
            [[2, 14], [3, 1], [4, 13], [5, 12], [6, 11], [7, 10], [8, 9]],
            [[14, 9], [10, 8], [11, 7], [12, 6], [13, 5], [1, 4], [2, 3]],
            [[3, 14], [4, 2], [5, 1], [6, 13], [7, 12], [8, 11], [9, 10]],
            [[14, 10], [11, 9], [12, 8], [13, 7], [1, 6], [2, 5], [3, 4]],
            [[4, 14], [5, 3], [6, 2], [7, 1], [8, 13], [9, 12], [10, 11]],
            [[14, 11], [12, 10], [13, 9], [1, 8], [2, 7], [3, 6], [4, 5]],
            [[5, 14], [6, 4], [7, 3], [8, 2], [9, 1], [10, 13], [11, 12]],
            [[14, 12], [13, 11], [1, 10], [2, 9], [3, 8], [4, 7], [5, 6]],
            [[6, 14], [7, 5], [8, 4], [9, 3], [10, 2], [11, 1], [12, 13]],
            [[14, 13], [1, 12], [2, 11], [3, 10], [4, 9], [5, 8], [6, 7]],
            [[7, 14], [8, 6], [9, 5], [10, 4], [11, 3], [12, 2], [13, 1]],
        ]

        create_round = create_rounds(self.tournaments[5])
        self.assertEqual(create_round, result)


class TournamentModelTestExtension(TransactionTestCase):
    """test related with tournaments that involve the creation of games"""

    reset_sequences = True

    def setUp(self):
        from chess_models.management.commands.populate import Command

        self.command = Command()
        self.command.cleanDataBase()
        self.players = [
            "Alyx",
            "Bruno",
            "Charline",
            "David",
            "Elene",
            "Franck",
            "Genevieve",
            "Irina",
            "Jessica",
            "Lais",
            "Maria",
            "Nick (W)",
            "Opal",
            "Paul",
            "Reine",
            "Stephan",
        ]

    @tag("continua")
    def test_tournament_getPlayers_copied(self):
        """Test function getPlayers that returns a list of players"""
        resultsDict = {name: [i + 1] for i, name in enumerate(self.players)}
        self.command.readInputFile(
            "chess_models/management/commands/tie-breaking-swiss.trf"
        )
        self.command.insertData()
        tournament = Tournament.objects.get(
            name="tie-breaking exercises swiss"
        )
        tournament.tournament_speed = TournamentSpeed.CLASSICAL
        tournament.tournament_type = TournamentType.SWISS
        tournament.board_type = TournamentBoardType.OTB
        tournament.cleanRankingList()
        tournament.save()
        playersList = tournament.getPlayers(sorted=True)
        for player in playersList:
            player.fide_rating_classical = resultsDict[player.name][0]
            player.save()

        tournament.board_type = TournamentBoardType.LICHESS
        tournament.save()

        playersList_lichess = tournament.getPlayers(sorted=True)
        for player in playersList_lichess:
            player.lichess_rating_classical = resultsDict[player.name][0]
            player.save()

        # Asegurar que la lista no está vacía
        self.assertGreater(
            len(playersList), 0, "La lista de jugadores no debería estar vacía"
        )
        self.assertGreater(
            len(playersList_lichess),
            0,
            "La lista de jugadores de Lichess no debería estar vacía",
        )

        # Asegurar que los jugadores están ordenados correctamente
        fide_ratings = [player.fide_rating_classical for player in playersList]
        lichess_ratings = [
            player.lichess_rating_classical for player in playersList_lichess
        ]
        self.assertEqual(
            fide_ratings,
            sorted(fide_ratings, reverse=False),
            "Los jugadores FIDE no están ordenados correctamente",
        )
        self.assertEqual(
            lichess_ratings,
            sorted(lichess_ratings, reverse=False),
            "Los jugadores Lichess no están ordenados correctamente",
        )

    @tag("continua")
    def test_str_game_with_bye(self):
        tournament = Tournament.objects.create(
            name="Test Tournament",
            win_points=1, draw_points=0.5, lose_points=0
        )
        round1 = Round.objects.create(name="Round 1", tournament=tournament)

        player1 = Player.objects.create(lichess_username="luizz04")

        game = Game.objects.create(
            white=player1,
            black=None,
            round=round1,
            finished=True,
            result=Scores.WHITE,
        )
        expected_str = f"{str(player1)}({player1.id}) vs BYE = White"
        self.assertEqual(str(game), expected_str)

    @tag("continua")
    def test_str_game_with_bye2(self):
        tournament = Tournament.objects.create(
            name="Test Tournament",
            win_points=1, draw_points=0.5, lose_points=0
        )
        round1 = Round.objects.create(name="Round 1", tournament=tournament)

        player1 = Player.objects.create(lichess_username="luizz04")

        game = Game.objects.create(
            white=None,
            black=player1,
            round=round1,
            finished=True,
            result=Scores.WHITE,
        )
        expected_str = f"BYE vs {str(player1)}({player1.id}) = White"
        self.assertEqual(str(game), expected_str)

    @tag("continua")
    def test_get_game(self):
        tournament = Tournament.objects.create(
            name="Test Tournament",
            win_points=1, draw_points=0.5, lose_points=0
        )
        round1 = Round.objects.create(name="Round 1", tournament=tournament)

        player1 = Player.objects.create(lichess_username="luizz04")

        game = Game.objects.create(
            white=None,
            black=player1,
            round=round1,
            finished=True,
            result=Scores.WHITE,
        )
        self.assertEqual(tournament.getGames()[0], game)

    @tag("continua")
    def test_create_rounds_not_even(self):
        tournament_name = "tournament_01"
        tournament = Tournament.objects.create(
            name=tournament_name,
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.RAPID,
        )

        player1 = Player.objects.create(lichess_username="luizz04")
        tournament.players.add(player1)

        r = create_rounds(tournament)
        self.assertEqual(r, [])


class TournamentSerializerTest(TestCase):
    @tag("continua")
    def test_to_representation_with_valid_choices(self):
        rankingSystem = RankingSystem.BUCHHOLZ
        ranking = RankingSystemClass.objects.create(value=rankingSystem)

        tournament = Tournament.objects.create(
            name="Test Tournament",
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.BLITZ,
            board_type=TournamentBoardType.LICHESS,
        )
        tournament.rankingList.add(ranking)

        # Serialize
        serializer = TournamentSerializer()
        res = serializer.to_representation(tournament)
        # Check
        self.assertEqual(res["id"], tournament.id)
        self.assertEqual(res["name"], "Test Tournament")
        self.assertEqual(res["board_type"], TournamentBoardType.LICHESS)
        self.assertEqual(res["tournament_type"], TournamentType.ROUNDROBIN)
        self.assertEqual(res["rankingList"], [RankingSystem.BUCHHOLZ])


###########################################################################
###########################################################################
###########################################################################
###########################################################################


class GameViewSetUpdateInvalidTest(APITestCase):
    def setUp(self):
        # Crear jugadores
        self.white = Player.objects.create(
            name="Player White", lichess_rating_rapid=1200
        )
        self.black = Player.objects.create(
            name="Player Black", lichess_rating_rapid=1300
        )

        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            win_points=1, draw_points=0.5, lose_points=0
        )
        self.round = Round.objects.create(
            name="Round 1", tournament=self.tournament
        )

        # Crear juego sin terminar, asociando la ronda creada
        self.game = Game.objects.create(
            white=self.white,
            black=self.black,
            finished=False,
            round=self.round,
        )

        # Obtener la URL del endpoint detail
        self.url = reverse("game-detail", args=[self.game.id])

    @tag("continua")
    def test_update_with_invalid_data_returns_400(self):
        # Datos inválidos: "result" con un valor no permitido
        invalid_data = {
            "result": "NOT_VALID"  # suponiendo que el
            # serializer tiene `choices` en result
        }

        response = self.client.patch(
            self.url, data=invalid_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("result", response.data)


class CreateRoundAPIViewTest(TransactionTestCase):
    """Test the round API"""

    reset_sequences = True

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.create_round_url = "/api/v1/create_round/"
        # reset sequences used in primary keys

    @tag("continua")
    def test_001_create_round(self):  # OK
        """check create_round method
        It should create a round with games and
        NO results.
        Input: tournament_id
        """
        # reset DB sequences
        tournament = Tournament.objects.create(
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.LICHESS,
        )
        tournament.addToRankingList(RankingSystem.WINS.value)
        # create players
        NoItems = 10
        for i in range(NoItems):
            player = Player.objects.create(lichess_username=LICHESS_USERS[i])
            # add players to tournament
            tournament.players.add(player)
        # create rounds/games
        self.client.force_authenticate(user=self.user)
        data = {
            # 'swissByes':  [1, 2, 3],
        }
        response = self.client.post(self.create_round_url, data)
        # print("response", response)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # @tag("continua")
    # def test_002_create_round2(self):  # OK
    #     """ check create_round method
    #     It should create a round with games and
    #     NO results.
    #     Input: tournament_id
    #     """
    #
    #     # create rounds/games
    #     self.client.force_authenticate(user=self.user)
    #     data = {'tournament_id': -1111111,
    #             # 'swissByes':  [1, 2, 3],
    #             }
    #     response = self.client.post(
    #         self.create_round_url, data)
    #     # print("response", response)
    #     data = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_003_0players(self):  # OK
        """check create_round method
        It should create a round with games and
        NO results.
        Input: tournament_id
        """
        # reset DB sequences
        tournament = Tournament.objects.create(
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.LICHESS,
        )
        tournament_id = tournament.id
        tournament.addToRankingList(RankingSystem.WINS.value)

        # create rounds/games
        self.client.force_authenticate(user=self.user)
        data = {
            "tournament_id": tournament_id,
            # 'swissByes':  [1, 2, 3],
        }
        response = self.client.post(self.create_round_url, data)
        # print("response", response)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_004_lenrounds0(self):  # OK
        """check create_round method
        It should create a round with games and
        NO results.
        Input: tournament_id
        """
        # reset DB sequences
        tournament = Tournament.objects.create(
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.LICHESS,
        )
        tournament_id = tournament.id
        tournament.addToRankingList(RankingSystem.WINS.value)
        # create players
        NoItems = 1
        for i in range(NoItems):
            player = Player.objects.create(lichess_username=LICHESS_USERS[i])
            # add players to tournament
            tournament.players.add(player)
        # create rounds/games
        self.client.force_authenticate(user=self.user)
        data = {
            "tournament_id": tournament_id,
            # 'swissByes':  [1, 2, 3],
        }
        response = self.client.post(self.create_round_url, data)
        # print("response", response)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_005_no_tournament(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.create_round_url, data={"tournament_id": 999999999}
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["result"], False)


class TournamentAPITest(TransactionTestCase):
    """Test the tournament API"""

    reset_sequences = True

    def setUp(self):
        # I do not think deleted is needed
        # since the system should reset the database
        # before each test
        Tournament.objects.all().delete()
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="user1", password="testpassword"
        )

    @tag("continua")
    def test_004_SearchTournamentsAPIView(self):  # OK
        # test the search tournament API

        # create several tournaments
        NoItemsX = 5
        NoItemsY = 4
        for x in range(1, NoItemsX + 1):
            for y in range(1, NoItemsY + 1):
                Tournament.objects.create(
                    name=f"tournament_{x:02d}_{y:02d}",
                    tournament_type=TournamentType.SWISS,
                    tournament_speed=TournamentSpeed.CLASSICAL,
                    board_type=TournamentBoardType.LICHESS,
                )
        # call search with a POST
        data = {}
        response = self.client.post(URLSEARCH, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetRankingAPIViewTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        from chess_models.management.commands.populate import Command

        self.client = APIClient()
        self.create_get_ranking_url = "/api/v1/get_ranking/"
        command = Command()
        command.cleanDataBase()
        command.readInputFile(
            "chess_models/management/commands/tie-breaking-swiss.trf"
        )
        command.insertData()  # Insert data into the database
        self.tournament_name = "tie-breaking exercises swiss"
        # read tournament frok database
        self.tournament = Tournament.objects.get(name=self.tournament_name)

    @tag("continua")
    def test_001_getRanking_no_tournament(self):  # OK
        """retrieve ranking
        rank by score, wins and blacktimes
        """
        self.tournament.cleanRankingList()
        self.tournament.addToRankingList(RankingSystem.WINS.value)
        self.tournament.addToRankingList(RankingSystem.BLACKTIMES.value)
        # data = {'tournament_id': tournament_id}

        response = self.client.get(self.create_get_ranking_url + f"{0}/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_002_getRanking_no_ranking(self):  # OK
        """retrieve ranking
        rank by score, wins and blacktimes
        """
        tournament = Tournament.objects.create(
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.LICHESS,
        )
        tournament_id = tournament.id
        tournament.addToRankingList(RankingSystem.WINS.value)
        self.tournament.cleanRankingList()
        # data = {'tournament_id': tournament_id}
        response = self.client.get(
            self.create_get_ranking_url + f"{tournament_id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_003_lichess_username(self):  # OK
        """retrieve ranking
        rank by score, wins and blacktimes
        """
        tournament_id = self.tournament.id
        self.tournament.cleanRankingList()
        self.tournament.addToRankingList(RankingSystem.WINS.value)
        self.tournament.addToRankingList(RankingSystem.BLACKTIMES.value)
        player1 = Player.objects.create(lichess_username="luizz04")
        self.tournament.players.add(player1)
        # data = {'tournament_id': tournament_id}

        response = self.client.get(
            self.create_get_ranking_url + f"{tournament_id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateTournamentAPIViewTest(TransactionTestCase):
    """Test the tournament API"""

    reset_sequences = True

    def setUp(self):
        # I do not think delete is needed
        # since the system should reset the database
        # before each test
        Tournament.objects.all().delete()
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="user1", password="testpassword"
        )

    @tag("continua")
    def test_001_create_tournament(self):  # OK
        """Create a new tournament"""
        self.client.force_authenticate(user=self.user1)
        tournament_name = "tournament_1"
        data = {
            "name": tournament_name,
            "tournament_type": TournamentType.SWISS,
            "tournament_speed": TournamentSpeed.CLASSICAL,
            "board_type": TournamentBoardType.LICHESS,
            "players":
            "lichess_username\neaffelix\noliva21\nrmarabini\nzaragozana",
        }
        response = self.client.post(URLCREATETOURNAMENT, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag("continua")
    def test_002_request_without_perms(self):
        """Make a request without being logged in"""
        # Create a new tournament
        tournament_name = "tournament_1"
        data = {
            "name": tournament_name,
            "tournament_type": TournamentType.SWISS,
            "tournament_speed": TournamentSpeed.CLASSICAL,
            "board_type": TournamentBoardType.LICHESS,
            "players":
            "lichess_username\neaffelix\noliva21\nrmarabini\nzaragozana",
        }
        response = self.client.post(URLCREATETOURNAMENT, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("continua")
    def test_003_request_without_data(self):
        """Make a request without being logged in"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(URLCREATETOURNAMENT)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_004_save_repeated_tournament(self):
        """Make a request without being logged in"""
        self.client.force_authenticate(user=self.user1)
        tournament_name = "tournament_1"
        data = {
            "name": tournament_name,
            "tournament_type": TournamentType.SWISS,
            "tournament_speed": TournamentSpeed.CLASSICAL,
            "board_type": TournamentBoardType.LICHESS,
            "players":
            "lichess_username\neaffelix\noliva21\nrmarabini\nzaragozana",
        }
        response = self.client.post(URLCREATETOURNAMENT, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(URLCREATETOURNAMENT, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_005_create_tournament_exception(self):
        """Test exception handling during tournament creation"""
        self.client.force_authenticate(user=self.user1)
        data = {
            "name": "tournament_name",
            "tournament_type": TournamentType.SWISS,
            "tournament_speed": TournamentSpeed.CLASSICAL,
            "board_type": TournamentBoardType.LICHESS,
            "players":
            "lichess_username\neaffelix\noliva21\nrmarabini\nzaragozana",
        }
        with patch.object(
            TournamentSerializer,
            "save", side_effect=Exception("Mocked exception")
        ):
            response = self.client.post(URLCREATETOURNAMENT, data)
            self.assertEqual(
                response.status_code, status.HTTP_400_BAD_REQUEST
            )
            self.assertIn(
                "Error creating tournament:", response.data["message"]
            )


class GetPlayers(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        # I do not think delete is needed
        Tournament.objects.all().delete()
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="user1", password="testpassword"
        )

    @tag("continua")
    def test_000_get_Players_no_tournament(self):  # OK
        """Create a new tournament"""
        self.client.force_authenticate(user=self.user1)
        tournament_name = "tournament_1"
        data = {
            "name": tournament_name,
            "tournament_type": TournamentType.SWISS,
            "tournament_speed": TournamentSpeed.CLASSICAL,
            "board_type": TournamentBoardType.LICHESS,
            "players":
            "lichess_username\neaffelix\noliva21\nrmarabini\nzaragozana",
        }
        response = self.client.post(URLTOURNAMENT, data)
        response = self.client.get(GETPLAYERS + f"{0}/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetRoundResultsAPIViewTest(TransactionTestCase):
    """Test the tournament API"""

    reset_sequences = True

    def setUp(self):
        # I do not think delete is needed
        # since the system should reset the database
        # before each test
        Tournament.objects.all().delete()
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="user1", password="testpassword"
        )

    @tag("continua")
    def test_001_get_round_results(self):  # OK
        """Get round results"""
        self.client.force_authenticate(user=self.user1)
        tournament_name = "tournament_1"
        data = {
            "name": tournament_name,
            "tournament_type": TournamentType.SWISS,
            "tournament_speed": TournamentSpeed.CLASSICAL,
            "board_type": TournamentBoardType.LICHESS,
            "players":
            "lichess_username\neaffelix\noliva21\nrmarabini\nzaragozana",
        }
        response = self.client.post(URLTOURNAMENT, data)
        tournament_id = response.data["id"]
        response = self.client.get(GETROUNDSRESULTS + f"{tournament_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("continua")
    def test_002_get_round_results_no_tournament(self):  # OK
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            GETROUNDSRESULTS + "99999999/"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateLichessGameAPIView(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.update_lichess_game_url = "/api/v1/update_lichess_game/"

    @tag("continua")
    def test_001_updateLichessGames_no_gameid(self):  # OK
        """update lichess game"""
        # create tournament
        tournament = Tournament.objects.create(
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.LICHESS,
        )
        # create players
        for username, id in playerListCasita:
            player = Player.objects.create(id=id, lichess_username=username)
            # add players to tournament
            tournament.players.add(player)
        # create rounds/games
        swissByes = []
        create_rounds(tournament, swissByes)
        # Now there is a problem, the algorithm use to create
        # the games is not the same as the one used in lichess
        # so we may need to swap some of the players

        # update games
        for game in tournament.getGames():
            white = game.white.lichess_username
            black = game.black.lichess_username
            # print(white, black, game)
            try:
                (lichess_game_id, result) = casitaResults[(white, black)]
            # OK the created games are not like the ones
            # in lichess let us swap users
            except Exception:
                (lichess_game_id, result) = casitaResults[(black, white)]
                game.white, game.black = game.black, game.white
                game.save()

            data = {"lichess_game_id": lichess_game_id}

            url = self.update_lichess_game_url
            response = self.client.post(url, data)
            data = response.json()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_002_not_game(self):  # OK
        """update lichess game"""
        # create tournament
        tournament = Tournament.objects.create(
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.LICHESS,
        )
        # create players
        for username, id in playerListCasita:
            player = Player.objects.create(id=id, lichess_username=username)
            # add players to tournament
            tournament.players.add(player)
        # create rounds/games
        swissByes = []
        create_rounds(tournament, swissByes)
        # Now there is a problem, the algorithm use to create
        # the games is not the same as the one used in lichess
        # so we may need to swap some of the players

        # update games
        for game in tournament.getGames():
            white = game.white.lichess_username
            black = game.black.lichess_username
            # print(white, black, game)
            try:
                (lichess_game_id, result) = casitaResults[(white, black)]
            # OK the created games are not like the ones
            # in lichess let us swap users
            except Exception:
                (lichess_game_id, result) = casitaResults[(black, white)]
                game.white, game.black = game.black, game.white
                game.save()

            data = {"game_id": 11111111111, "lichess_game_id": lichess_game_id}

            url = self.update_lichess_game_url
            response = self.client.post(url, data)
            data = response.json()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_003_game_finished(self):  # OK
        """update lichess game"""
        tournament_name = "tournament_01"
        tournament1 = Tournament.objects.create(
            name=tournament_name,
            tournament_type=TournamentType.DOUBLEROUNDROBIN
        )
        # create round
        round_name = "round_01"
        round1 = Round.objects.create(name=round_name, tournament=tournament1)

        players = []
        player = Player.objects.create(lichess_username="luizz04")
        # tournament1.players.add(player)
        players.append(player)
        player = Player.objects.create(lichess_username="lexorg55")
        # tournament1.players.add(player)
        players.append(player)

        game = Game.objects.create(round=round1)
        game.finished = True
        game.white = players[0]
        game.black = players[1]
        game.save()
        game_id = game.id

        data = {
            "game_id": game_id,
        }

        url = self.update_lichess_game_url
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_004_game_no_lichess_game_id(self):  # OK
        """update lichess game"""
        tournament_name = "tournament_01"
        tournament1 = Tournament.objects.create(
            name=tournament_name,
            tournament_type=TournamentType.DOUBLEROUNDROBIN
        )
        # create round
        round_name = "round_01"
        round1 = Round.objects.create(name=round_name, tournament=tournament1)

        players = []
        player = Player.objects.create(lichess_username="luizz04")
        # tournament1.players.add(player)
        players.append(player)
        player = Player.objects.create(lichess_username="lexorg55")
        # tournament1.players.add(player)
        players.append(player)

        game = Game.objects.create(round=round1)
        game.finished = False
        game.white = players[0]
        game.black = players[1]
        game.save()
        game_id = game.id

        data = {
            "game_id": game_id,
        }

        url = self.update_lichess_game_url
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateOTBGameAPIViewTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.update_otb_game_url = "/api/v1/update_otb_game/"

    @tag("continua")
    def test_001_updateOTBGames(self):  # OK
        """update OTB game by white player"""
        # create tournament
        tournament = Tournament.objects.create(
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.OTB,
        )
        # create players
        for username, id in playerListCasita:
            name = username
            email = f"{username}@example.com"
            player = Player.objects.create(id=id, name=name, email=email)
            # add players to tournament
            tournament.players.add(player)
        # create rounds/games
        swissByes = []
        create_rounds(tournament, swissByes)

        # update games
        for i, game in enumerate(tournament.getGames()):
            name = game.white.name
            email = game.white.email
            if i % 2 == 0:
                result = Scores.BLACK.value
            else:
                result = Scores.WHITE.value

            data = {"name": name, "email": email, "otb_result": result}

            url = self.update_otb_game_url
            response = self.client.post(url, data)
            data = response.json()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_002_try_otbresult(self):  # OK
        """update OTB game by white player"""
        # create tournament
        tournament = Tournament.objects.create(
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.OTB,
        )
        # create players
        for username, id in playerListCasita:
            name = username
            email = f"{username}@example.com"
            player = Player.objects.create(id=id, name=name, email=email)
            # add players to tournament
            tournament.players.add(player)
        # create rounds/games
        swissByes = []
        create_rounds(tournament, swissByes)

        # update games
        for i, game in enumerate(tournament.getGames()):
            name = game.white.name
            email = game.white.email
            game_id = game.id
            if i % 2 == 0:
                result = Scores.BLACK.value
            else:
                result = Scores.WHITE.value

            result = "invalid_result"
            data = {
                "game_id": game_id,
                "name": name,
                "email": email,
                "otb_result": result,
            }
            url = self.update_otb_game_url
            response = self.client.post(url, data)
            data = response.json()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_003_not_game(self):  # OK
        """update OTB game by white player"""
        # create tournament
        tournament = Tournament.objects.create(
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.OTB,
        )
        # create players
        for username, id in playerListCasita:
            name = username
            email = f"{username}@example.com"
            player = Player.objects.create(id=id, name=name, email=email)
            # add players to tournament
            tournament.players.add(player)
        # create rounds/games
        swissByes = []
        create_rounds(tournament, swissByes)

        # update games
        for i, game in enumerate(tournament.getGames()):
            name = game.white.name
            email = game.white.email
            if i % 2 == 0:
                result = Scores.BLACK.value
            else:
                result = Scores.WHITE.value

            data = {
                "game_id": 0,
                "name": name,
                "email": email,
                "otb_result": result
            }
            url = self.update_otb_game_url
            response = self.client.post(url, data)
            data = response.json()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_004_change_game_status(self):

        # Create a game
        tournament = Tournament.objects.create(
            name="Test Tournament",
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.OTB,
        )

        for username, id in playerListCasita:
            name = username
            email = f"{username}@example.com"
            player = Player.objects.create(id=id, name=name, email=email)
            # add players to tournament
            tournament.players.add(player)

        create_rounds(tournament)
        game = tournament.getGames()[0]
        game.finished = True
        game.save()

        data = {
            "game_id": game.id,
            "name": game.white.name,
            "email": game.white.email,
            "otb_result": Scores.WHITE.value,
        }
        response = self.client.post(self.update_otb_game_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AdminUpdateGameAPIViewTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        # I do not think delete is needed
        # since the system should reset the database
        # before each test
        Tournament.objects.all().delete()
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="user1", password="testpassword"
        )

    @tag("continua")
    def test_001_no_params_sent(self):
        # Test with no parameters sent
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(ADMINUPDATEGAME, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_002_result_invent(self):
        # Test with invalid result
        self.client.force_authenticate(user=self.user1)

        # Create a game
        tournament = Tournament.objects.create(
            name="Test Tournament",
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.CLASSICAL,
            board_type=TournamentBoardType.OTB,
        )

        for username, id in playerListCasita:
            name = username
            email = f"{username}@example.com"
            player = Player.objects.create(id=id, name=name, email=email)
            # add players to tournament
            tournament.players.add(player)

        create_rounds(tournament)
        game = tournament.getGames()[0]

        data = {"game_id": game.id, "otb_result": "invalid_result"}
        response = self.client.post(ADMINUPDATEGAME, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_003_no_game_found(self):
        self.client.force_authenticate(user=self.user1)
        data = {"game_id": 999999, "otb_result": Scores.WHITE.value}
        response = self.client.post(ADMINUPDATEGAME, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Game does not exist", response.data["message"])
