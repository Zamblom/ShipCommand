from __future__ import annotations

import datetime
import typing

import json
import re


class Timed:
    def __init__(self, parent: typing.Optional[Timed], item) -> None:
        self.parent: typing.Optional[Timed] = parent
        self.time: datetime.datetime = datetime.datetime.now()
        if type(item) in [bool, float, int, list, str]:
            self.value = item
        elif type(item) == dict:
            self.value = {k : Timed(self, v) for k, v in item.items()}
        else:
            raise TypeError(f"Non-time-able Type: {type(item)}")

    def set_time(self, tab=0):
        self.time = datetime.datetime.now()
        if self.parent is not None:
            self.parent.set_time(tab+1)

    def get(self):
        return self.value

    def set(self, value):
        self.set_time()
        self.value = value

    def __getitem__(self, indices):
        return self.value.__getitem__(indices)

    def __setitem__(self, key, value):
        self.value.__setitem__(key, value)
        self.set_time()
    def __repr__(self):
        return str(self)

    def __str__(self):
        return "<T>" + str(self.value)

    def __hash__(self):
        return hash(self.value)

    def __iter__(self):
        return self.value.__iter__()

    def append(self, *args, **kwargs):
        if not isinstance(self.value, list):
            raise TypeError(self, "is not List")
        self.value.append(*args, **kwargs)
        self.set_time()

    def remove(self, *args, **kwargs):
        if not isinstance(self.value, list):
            raise TypeError(self, "is not List")
        self.value.remove(*args, **kwargs)
        self.set_time()

    def get_updated(self, time: datetime.datetime, tab=0):
        if self.time > time:
            if isinstance(self.value, Timed):
                return self.value.get_updated(time, tab+1)
            if type(self.value) in [bool, float, int, list ,str]:
                return self.value
            if isinstance(self.value, dict):
                output = {}
                for k, v in self.value.items():
                    value = v.get_updated(time, tab+1)
                    if value is not None:
                        output[k] = value
                return output



class Ship:
    def __init__(self, ship_file: str) -> None:
        self.ship_file: str = ship_file
        with open(ship_file, "r") as file:
            data: str = file.read()
        self.data: Timed = Timed(None, json.loads(data))
        self.validate_abilities()


    def move_player_to_room(self, player: str, new_deck: str, new_room: str) -> None:
        deck, room = self.player_to_location(player)

        if [new_deck, new_room] not in self.data["decks"][deck]["rooms"][room]["connections"]:
            return

        while self.data["decks"][new_deck]["rooms"][new_room]["isLink"].get():
            new_deck, new_room = self.data["decks"][new_deck]["rooms"][new_room]["connections"][0]

        self.data["decks"][deck]["rooms"][room]["players"].remove(player)
        self.data["decks"][new_deck]["rooms"][new_room]["players"].append(player)

    def player_to_location(self, player: str):
        for deck in self.data["decks"]:
            for room in self.data["decks"][deck]["rooms"]:
                if player in self.data["decks"][deck]["rooms"][room]["players"]:
                    return deck, room

    def get_connections_by_player(self, player: str):
        deck, room = self.player_to_location(player)
        return self.data[deck]["rooms"][room]["connections"]

    def use_ability(self, player: str, ability: str) -> bool:
        deck, room = self.player_to_location(player)
        if ability not in self.data["decks"][deck]["rooms"][room]["abilities"]:
            return False

        if not self.data["abilities"][ability]["enabled"]:
            return False

        for action in self.data["abilities"][ability]["actions"].get():
            self.parse_requirement_or_action(action)

        self.validate_abilities()

        return True

    def validate_abilities(self):
        for ability in self.data["abilities"]:
            self.data["abilities"][ability]["enabled"].set(
                self.parse_requirement_or_action(
                    self.data["abilities"][ability]["requirement"].get()
                )
            )


    def parse_requirement_or_action(self, string) -> typing.Any:
        string = string.strip()

        if (query := re.search("^\\w+(?=[\\[(])", string)) is None:
            return string

        operator: str = query.group()
        parameter_space: str = re.search(f"(?<={operator}[\\[(]).*(?=[])]$)", string).group()

        depth: int = 0
        parameters: list[typing.Any] = []
        current_parameter: str = ""
        for i in parameter_space:
            if i == "," and depth == 0:
                parameters.append(self.parse_requirement_or_action(current_parameter))
                current_parameter = ""
            else:
                if i in "[(":
                    depth += 1
                elif i in "])":
                    depth -= 1
                if depth < 0:
                    raise ValueError(f"Invalid Value: \"{string}\"")
                current_parameter += i
        parameters.append(self.parse_requirement_or_action(current_parameter))

        methods: dict[str, typing.Callable] = {
            "ABILITY": lambda p: self.data["abilities"][p[0]].get(),
            "ACTIVATE": lambda p: p[0]["active"].set(True),
            "ACTIVE": lambda p: p[0]["active"].get(),
            "ADD_CONNECTION": lambda p: p[0]["connections"].append([p[1], p[2]]),
            "AMOUNT": lambda p: p[0]["amount"].get(),
            "AND": lambda p: p[0] and p[1],
            "CONDITION": lambda p: self.data["conditions"][p[0]].get(),
            "DEACTIVATE": lambda p: p[0]["active"].set(False),
            "EXPEND": lambda p: p[0]["amount"].set(p[0]["amount"].get() - p[1]),
            "GREATER_THAN": lambda p: p[0] > p[1],
            "INT": lambda p: int(p[0]),
            "NOT": lambda p: not p[0],
            "REMOVE_CONNECTION": lambda p: p[0]["connections"].remove([p[1], p[2]]),
            "RESOURCE": lambda p: self.data["resources"][p[0]].get(),
            "ROOM": lambda p: self.data["decks"][p[0]]["rooms"][p[1]].get(),
            "STRING": lambda p: p[0]
        }

        return methods[operator](parameters)