from chess_models.models import Tournament, Player, Game, Round
from chess_models.serializers import TournamentSerializer
from django.test import TestCase, tag, TransactionTestCase
from chess_models.models import (
    LichessAPIError,
    Scores,
    TournamentType,
    get_wins,
    create_rounds,
    RankingSystem,
    RankingSystemClass
)
from chess_models.models.constants import (
    TournamentSpeed,
    TournamentBoardType,
)


class ExtraTests(TestCase):

    @tag("continua")
    def test_check_lichess_user_exists(self):
        """Return false if player does not exist in lichess"""

        # Create a player with no lichess username
        player = Player.objects.create(
            name="John Doe", email="john@example.com"
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
        self.assertIn(str(x), '.')

    @tag("continua")
    def test_bye(self):
        tournament = Tournament.objects.create(
            name="Test Tournament", win_points=1,
            draw_points=0.5, lose_points=0
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
            player = Player.objects.create(
                name=f"Player {count}"
            )
            count += 1
            players.append(player)

        # Create the tournaments
        cls.tournaments = []
        for i in range(6):
            tournament = Tournament.objects.create(
                name=f"Test Tournament {i}",
            )

            max_players = i*2+4
            for player in players:
                if player.id > max_players:
                    break
                tournament.players.add(player)

            tournament.save()
            cls.tournaments.append(tournament)

    @tag("continua")
    def test_001_create_round_4(self):
        """Test the creation of a round with 4 players"""
        result = [
            [[1, 4], [2, 3]],
            [[4, 3], [1, 2]],
            [[2, 4], [3, 1]]
        ]

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
            [[3, 6], [4, 2], [5, 1]]
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
            [[4, 8], [5, 3], [6, 2], [7, 1]]
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
            name="Test Tournament", win_points=1,
            draw_points=0.5, lose_points=0
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
            name="Test Tournament", win_points=1,
            draw_points=0.5, lose_points=0
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
            name="Test Tournament", win_points=1,
            draw_points=0.5, lose_points=0
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
        tournament_name = 'tournament_01'
        tournament = Tournament.objects.create(
            name=tournament_name,
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.RAPID)

        player1 = Player.objects.create(lichess_username="luizz04")
        tournament.players.add(player1)

        r = create_rounds(tournament)
        self.assertEqual(r, [])


class TournamentSerializerTest(TestCase):
    @tag("continua")
    def test_to_representation_with_valid_choices(self):
        rankingSystem = RankingSystem.BUCHHOLZ
        ranking = RankingSystemClass.objects.create(
            value=rankingSystem)

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
