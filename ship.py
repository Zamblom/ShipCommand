from __future__ import annotations

from typing import Any, Callable

import json
import re

import timed


class Ship:
    def __init__(self, ship_file: str) -> None:
        self.ship_file: str = ship_file
        with open(ship_file, "r") as file:
            data: str = file.read()
        self.data: timed.Timed = timed.Timed(json.loads(data))
        self.validate_abilities()

    def move_player_to_room(self, player: str, new_deck: str, new_room: str) -> None:
        deck, room = self.player_to_location(player)

        if [new_deck, new_room] not in self.data["decks"][deck]["rooms"][room]["connections"]:
            return

        while self.data["decks"][new_deck]["rooms"][new_room]["isLink"].get():
            new_deck, new_room = self.data["decks"][new_deck]["rooms"][new_room]["connections"][0]

        self.data["decks"][deck]["rooms"][room]["players"].remove(player)
        self.data["decks"][new_deck]["rooms"][new_room]["players"].append(player)

    def player_to_location(self, player: str) -> tuple[str, str]:
        for deck in self.data["decks"]:
            for room in self.data["decks"][deck]["rooms"]:
                if player in self.data["decks"][deck]["rooms"][room]["players"]:
                    return deck, room
        raise ValueError(f"Player [{player}] not Found")

    def get_connections_by_player(self, player: str) -> Any:
        deck, room = self.player_to_location(player)
        return self.data["decks"][deck]["rooms"][room]["connections"]

    def use_ability(self, player: str, ability: str, rolls: list[int]) -> bool:
        deck, room = self.player_to_location(player)
        if ability not in self.data["decks"][deck]["rooms"][room]["abilities"]:
            return False

        if not self.data["abilities"][ability]["enabled"]:
            return False

        for toggle, action in self.data["abilities"][ability]["actions"].get():
            if self.parse_requirement_or_action(toggle, rolls):
                self.parse_requirement_or_action(action, rolls)

        self.validate_abilities()

        return True

    def validate_abilities(self) -> None:
        for ability in self.data["abilities"].keys():
            self.data["abilities"][ability]["enabled"].set(
                self.parse_requirement_or_action(self.data["abilities"][ability]["requirement"].get(), [])
            )

    def parse_requirement_or_action(self, string: str, rolls: list[int]) -> Any:
        string = string.strip()

        if (query := re.search("^\\w+(?=[\\[(])", string)) is None:
            return string

        operator: str = query.group()
        parameter_space: str = r.group() if (r := re.search(f"(?<={operator}[\\[(]).*(?=[])]$)", string)) is not None else ""

        depth: int = 0
        parameters: list[Any] = []
        current_parameter: str = ""
        for i in parameter_space:
            if i == "," and depth == 0:
                parameters.append(self.parse_requirement_or_action(current_parameter, rolls))
                current_parameter = ""
            else:
                if i in "[(":
                    depth += 1
                elif i in "])":
                    depth -= 1
                if depth < 0:
                    raise ValueError(f"Invalid Value: \"{string}\"")
                current_parameter += i
        parameters.append(self.parse_requirement_or_action(current_parameter, rolls))

        methods: dict[str, Callable[[list[Any]], Any]] = {
            "ABILITY": lambda p: self.data["abilities"][p[0]].get(),
            "ACTIVATE": lambda p: p[0]["active"].set(True),
            "ACTIVE": lambda p: p[0]["active"].get(),
            "ADD_CONNECTION": lambda p: p[0]["connections"].append([p[1], p[2]]),
            "AMOUNT": lambda p: p[0]["amount"].get(),
            "AND": lambda p: p[0] and p[1],
            "BOOL": lambda p: {"TRUE": True, "FALSE": False}[p[0]],
            "CONDITION": lambda p: self.data["conditions"][p[0]].get(),
            "DEACTIVATE": lambda p: p[0]["active"].set(False),
            "EXPEND": lambda p: p[0]["amount"].set(p[0]["amount"].get() - p[1]),
            "GREATER_THAN": lambda p: p[0] > p[1],
            "INT": lambda p: int(p[0]),
            "NOT": lambda p: not p[0],
            "REMOVE_CONNECTION": lambda p: p[0]["connections"].remove([p[1], p[2]]),
            "RESOURCE": lambda p: self.data["resources"][p[0]].get(),
            "ROLL": lambda p: rolls[int(p[0])],
            "ROOM": lambda p: self.data["decks"][p[0]]["rooms"][p[1]].get(),
            "STRING": lambda p: p[0]
        }

        return methods[operator](parameters)
