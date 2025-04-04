from chess_models.models import Tournament, Player, Game, Round
from django.test import TestCase, tag, TransactionTestCase
from chess_models.models import (
    LichessAPIError,
    Scores,
    TournamentType,
    get_wins
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
            "The player trallegas101 is not meloon195", str(context.exception)
        )

    @tag("continua")
    def test_print_error(self):
        x = LichessAPIError(".")
        print(x)

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

