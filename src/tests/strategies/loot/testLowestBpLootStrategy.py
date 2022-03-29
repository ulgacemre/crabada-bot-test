from src.common.config import users
from src.helpers.general import findInList, firstOrNone
from src.strategies.loot.LowestBpLootStrategy import LowestBpLootStrategy
from src.common.clients import crabadaWeb2Client

# VARS
userAddress = users[0]["address"]
teamId = users[0]["teams"][0]["id"]
teams = crabadaWeb2Client.listTeams(userAddress)
team = findInList(teams, "team_id", teamId)  # type: ignore

if not team:
    print("Error getting team with ID " + str(teamId))
    exit(1)

strategy: LowestBpLootStrategy = LowestBpLootStrategy(crabadaWeb2Client).setParams(team)

# TEST FUNCTIONS
def testLowestBpStrategy() -> None:

    print(">>> IS STRATEGY APPLICABLE?")
    print(strategy.isApplicable())

    print(">>> CHOSEN MINE")
    try:
        print(strategy.getMine())
    except Exception as e:
        print("ERROR RAISED: " + e.__class__.__name__ + ": " + str(e))


# EXECUTE
testLowestBpStrategy()
