from typing import cast
from src.common.types import Tus
from src.helpers.general import secondOrNone, thirdOrNone
from src.strategies.reinforce.HighestMp import HighestMp
from src.common.clients import crabadaWeb2Client
from sys import argv

# VARS
gameId = secondOrNone(argv)
maxPrice = cast(Tus, int(thirdOrNone(argv) or 25))

if not gameId:
    print("Provide a game ID")
    exit(1)

game = crabadaWeb2Client.getMine(gameId)
strategy: HighestMp = HighestMp(crabadaWeb2Client).setParams(game, maxPrice)

# TEST FUNCTIONS
def test() -> None:

    print(">>> CRAB REINFORCEMENT WITH AUTOMATIC SELECTION")
    try:
        print(
            strategy.getCrab("MINING")
        )  # Will print note if mine is not reinforceable
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))

    print(">>> FIRST CRAB REINFORCEMENT")
    try:
        print(strategy.getCrab1())
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))

    print(">>> SECOND CRAB REINFORCEMENT")
    try:
        print(strategy.getCrab2())
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))


# EXECUTE
test()
