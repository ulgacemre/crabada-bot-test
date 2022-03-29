"""
Helpers to parse and validate the configuration variables
from the environment
"""

import typing
from web3 import Web3
from src.common.exceptions import InvalidConfig, MissingConfig
from src.common.types import (
    ConfigTeam,
    ConfigUser,
    Tus,
    TeamTask,
)
import os
from src.common.dotenv import getenv, parseFloat, parseInt
from typing import List, cast
from eth_typing import Address


def parseTeamConfig(teamNumber: int, userNumber: int) -> ConfigTeam:
    """
    Get the configuration of the given user's team from the environment
    """
    userPrefix = f"USER_{userNumber}"
    teamPrefix = f"{userPrefix}_TEAM_{teamNumber}"

    teamConfig: ConfigTeam = {
        "id": parseInt(teamPrefix),
        "userAddress": cast(Address, os.environ.get(f"{userPrefix}_ADDRESS")),
        "battlePoints": parseInt(f"{teamPrefix}_BATTLE_POINTS"),
        "task": cast(TeamTask, os.environ.get(f"{teamPrefix}_TASK", "mine")),
        "lootStrategyName": os.environ.get(f"{teamPrefix}_LOOT_STRATEGY", "LowestBp"),
        "reinforceStrategyName": os.environ.get(
            f"{teamPrefix}_REINFORCE_STRATEGY", "HighestBp"
        ),
        "reinforcementToPick": parseInt(f"{teamPrefix}_REINFORCEMENT_TO_PICK") or 1,
    }

    validateTeamConfig(teamConfig, teamNumber, userNumber)

    return teamConfig


def parseUserConfig(userNumber: int, teams: List[ConfigTeam]) -> ConfigUser:
    """
    Get the configuration of the given user from the environment

    TODO: Use something like Cerberus to make parsing sustainable
    """
    userPrefix = f"USER_{userNumber}"
    address = cast(Address, os.environ.get(f"{userPrefix}_ADDRESS"))
    reinforcementMaxPriceInTus = (
        parseFloat(f"{userPrefix}_REINFORCEMENT_MAX_PRICE") or 0
    )
    if not reinforcementMaxPriceInTus:  # for backward compatibility
        reinforcementMaxPriceInTus = (
            parseFloat(f"{userPrefix}_MAX_PRICE_TO_REINFORCE") or 0
        )

    userConfig: ConfigUser = {
        "address": address,
        "privateKey": os.environ.get(f"{userPrefix}_PRIVATE_KEY"),
        "reinforcementMaxPriceInTus": cast(Tus, reinforcementMaxPriceInTus),
        "reinforcementMaxPriceInTusWei": Web3.toWei(
            reinforcementMaxPriceInTus, "ether"
        ),
        "teams": [t for t in teams if t["userAddress"] == address],
    }

    validateUserConfig(userConfig, userNumber)

    return userConfig


def validateTeamConfig(team: ConfigTeam, teamNumber: int, userNumber: int) -> None:
    """
    Raise an exception if there's something wrong with a
    team config
    """
    if team["task"] not in typing.get_args(TeamTask):
        raise InvalidConfig(
            f"TASK parameter of team {teamNumber} of user {userNumber} must be one of {str(typing.get_args(TeamTask))}, but '{team['task']}' was given"
        )
    if team["reinforcementToPick"] <= 0 or team["reinforcementToPick"] > 100:
        raise InvalidConfig(
            f"REINFORCEMENT_TO_PICK parameter of team {teamNumber} of user {userNumber} must be an integer between 1 a and 100"
        )


def validateUserConfig(user: ConfigUser, userNumber: int) -> None:
    """
    Raise an exception if there's something wrong with a
    user's config
    """
    if not user["address"]:
        raise MissingConfig(f"User {userNumber} has no ADDRESS parameter given")
    maxPrice = user.get("reinforcementMaxPriceInTus")
    if not maxPrice or maxPrice <= 0:
        raise MissingConfig(
            f"User {userNumber} has no or invalid REINFORCEMENT_MAX_PRICE (must be a value greater than zero)"
        )
    if not user["teams"]:
        raise MissingConfig(f"User {userNumber} has no team configured")
