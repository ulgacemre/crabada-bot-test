from typing import Any, List
from src.libs.CrabadaWeb2Client.types import CrabForLending, Game
from src.strategies.reinforce.ReinforceStrategy import ReinforceStrategy
from src.helpers.general import nthOrLastOrNone
from src.helpers.price import weiToTus


class HighestBp(ReinforceStrategy):
    """
    Pick the crab with the highest battle point value and that
    costs less than maxPrice.

    If the reinforcementToPick mechanism is active, it avoids
    choosing highly requested crabs that could result in failed
    txs.
    """

    def query(self, game: Game) -> dict[str, Any]:
        return {
            "limit": 100,  # TODO: make it an argument
            "orderBy": "price",
            "order": "asc",
        }

    def process(self, game: Game, crabs: List[CrabForLending]) -> List[CrabForLending]:
        affordableCrabs = [c for c in crabs if weiToTus(c["price"]) < self.maxPrice1]
        return sorted(affordableCrabs, key=lambda c: (-c["battle_point"], c["price"]))

    def pick(self, game: Game, crabs: List[CrabForLending]) -> CrabForLending:
        """
        Pick the n-th crab or, if there are fewer than n, the last one
        """
        n = self.teamConfig["reinforcementToPick"]
        return nthOrLastOrNone(crabs, n - 1)
