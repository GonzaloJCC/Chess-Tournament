# Import classes like
# 	<<from .file_with_modelX import modelX # noqa F104>>
# It is important to add "# noqa F401" at the end of the import to informs
# flake8 to ignore the fact that the model is never use in this file

from .constants import *
from .player import Player # noqa F104
from .other_models import Referee, LichessAPIError
from .tournament import Tournament, RankingSystemClass
from .round import Round
from .game import Game, create_rounds