from __future__ import annotations
import typing

import json
import re


class Ability:
    def __init__(self, ship: Ship, name: str, requirements: str, actions: list[str]) -> None:
        self.ship: Ship = ship
        self.name: str = name
        self.requirements: str = requirements
        self.actions: list[str] = actions

        self.enabled: bool = False
        self.check_requirements()

    def check_requirements(self):
        self.enabled = self.parse(self.requirements)

    def activate(self):
        [self.parse(action) for action in self.actions]
        print(self, self.enabled)

    def parse(self, string: str) -> typing.Any:
        string = string.lstrip(" ").rstrip(" ")

        if (query := re.search("^\\w+(?=[\\[(])", string)) is None:
            return string

        operator: str = query.group()
        parameter_space: str = re.search(f"(?<={operator}[\\[(]).*(?=[])]$)", string).group()

        depth: int = 0
        parameters: list[typing.Any] = []
        current_parameter: str = ""
        for i in parameter_space:
            if i == "," and depth == 0:
                parameters.append(self.parse(current_parameter))
                current_parameter = ""
            else:
                if i in "[(":
                    depth += 1
                elif i in "])":
                    depth -= 1
                if depth < 0:
                    raise ValueError(f"Invalid Value: \"{string}\"")
                current_parameter += i
        parameters.append(self.parse(current_parameter))

        methods: dict[str, typing.Callable] = {
            "ABILITY": lambda p: self.ship.abilities[p[0]],
            "ACTIVATE": lambda p: p[0].activate(),
            "ACTIVE": lambda p: p[0].active,
            "ADD_CONNECTION": lambda p: p[0].connections.add(p[1]),
            "AMOUNT": lambda p: p[0].amount,
            "AND": lambda p: p[0] and p[1],
            "CONDITION": lambda p: self.ship.conditions[p[0]],
            "DEACTIVATE": lambda p: p[0].deactivate(),
            "EXPEND": lambda p: p[0].expend(p[1]),
            "GREATER_THAN": lambda p: p[0] > p[1],
            "INT": lambda p: int(p[0]),
            "NOT": lambda p: not p[0],
            "REMOVE_CONNECTION": lambda p: p[0].connections.discard(p[1]),
            "RESOURCE": lambda p: self.ship.resources[p[0]],
            "ROOM": lambda p: self.ship.rooms[p[0]],
            "STRING": lambda p: p[0]
        }

        return methods[operator](parameters)

    def jsonable(self) -> dict[str, str | bool]:
        return {"name": self.name, "enabled": self.enabled}


class Condition:
    def __init__(self, name: str, active: bool) -> None:
        self.name: str = name
        self.active: bool = active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class Resource:
    def __init__(self, name: str, amount: int, max_amount: int) -> None:
        self.name: str = name
        self.amount: int = amount
        self.max_amount: int = max_amount

    def expend(self, amount: int):
        self.amount = max(0, self.amount - amount)


class Room:
    def __init__(self, connections: set, abilities: typing.Optional[list[str]] = None, link: str = "") -> None:
        abilities = [] if abilities is None else abilities

        self.connections: set[str] = connections
        self.abilities: list[str] = abilities
        self.link: str = link
        self.players: list[str] = []

    def add_player(self, player: str) -> bool:
        if player in self.players:
            return False

        self.players.append(player)
        return True

    def remove_player(self, player: str) -> bool:
        if player not in self.players:
            return False

        self.players.remove(player)
        return True

    def has_players(self) -> bool:
        return len(self.players) > 0

    def has_link(self) -> bool:
        return self.link != ""


class Ship:
    def __init__(self, abilities_file: str, conditions_file: str, resources_file: str) -> None:
        self.abilities_file: str = abilities_file
        self.conditions_file: str = conditions_file
        self.resources_file: str = resources_file

        self.rooms: dict[str, Room] = {
            "gunTurretB": Room({"hatchFromGunTurretB"}),
            "hatchFromGunTurretB": Room(set(), link="corridor"),
            "gunTurretC": Room({"hatchFromGunTurretC"}),
            "hatchFromGunTurretC": Room(set(), link="corridor"),
            "corridor": Room({"ladderToDeckA", "gunBayB", "gunBayC", "gunBayD"}),
            "gunBayC": Room(set(), link="gunTurretB"),
            "gunBayB": Room(set(), link="gunTurretB"),
            "gunBayD": Room({"corridor"}),
            "ladderToDeckA": Room(set(), link="hallway"),
            "sledBay": Room({"hallway", "hatchToSledA", "hatchToSledB"}),
            "engineersQuarter": Room({"hallway", "cargoHold"}),
            "cargoHold": Room({"hallway", "engineersQuarter"}),
            "medBay": Room({"hallway"}),
            "cockpit": Room({"security"}, abilities=["evasiveManoeuvres", "deployFlares", "enterWarp"]),
            "brig": Room({"monitoring"}),
            "monitoring": Room({"hallway", "brig"}, abilities=["lockBrigCell", "unlockBrigCell"]),
            "livingArea": Room({"hallway", "workshop", "messHall", "crewQuarters"}),
            "messHall": Room({"livingArea"}),
            "crewQuarters": Room({"livingArea"}),
            "workshop": Room({"hallway", "livingArea"}),
            "hallway": Room({"sledBay", "engineersQuarter", "cargoHold", "medBay", "security", "monitoring", "livingArea", "workshop", "ladderToDeckB", "hatchToGunTurretA"}),
            "security": Room({"hallway", "cockpit"}),
            "ladderToDeckB": Room(set(), link="corridor"),
            "hatchToGunTurretA": Room(set(), link="hallway"),
            "hatchToSledA": Room(set(), link="hallway"),
            "hatchToSledB": Room(set(), link="hallway"),
        }

        self.abilities: dict[str: Ability] = {}
        self.conditions: dict[str: Condition] = {}
        self.resources: dict[str: Resource] = {}

        self.load_conditions()
        self.load_resources()
        self.load_abilities()

    def move_player_to_room(self, player: str, new_room: str) -> bool:
        current_room: str = self.get_room_by_player(player)

        if new_room not in self.rooms[current_room].connections:
            return False

        while self.rooms[new_room].has_link():
            new_room = self.rooms[new_room].link

        if not self.rooms[current_room].remove_player(player):
            return False

        if not self.rooms[new_room].add_player(player):
            if not self.rooms[current_room].add_player(player):
                raise RuntimeError(f"Removed [{player}] from [{current_room}] but could not add to [{new_room}] or restore.")
            return False

        return True

    def get_room_by_player(self, player: str) -> str:
        for room_name, room in self.rooms.items():
            if player in room.players:
                return room_name

    def get_connections_by_player(self, player: str) -> list[str]:
        return list(self.rooms[self.get_room_by_player(player)].connections)

    def validate_abilities(self) -> None:
        for ability in self.abilities.values():
            ability.check_requirements()

    def use_ability(self, player: str, ability: str) -> None:
        # TODO: Check if Ability accessible from same Room as Player
        if self.abilities[ability].enabled:
            self.abilities[ability].activate()
        self.validate_abilities()

    def get_rooms_with_players(self) -> dict[str, list[str]]:
        return {room_name: room.players for room_name, room in self.rooms.items() if room.has_players()}

    def get_abilities(self) -> dict[str, dict[str, str | bool]]:
        return {name: data.jsonable() for name, data in self.abilities.items()}

    def get_conditions(self) -> dict[str, dict[str, bool]]:
        return {name: {"active": data.active} for name, data in self.conditions.items()}

    def get_resources(self) -> dict[str, dict[str, int]]:
        return {name: {"amount": data.amount, "maxAmount": data.max_amount} for name, data in self.resources.items()}

    def load_abilities(self):
        with open(self.abilities_file, "r") as file:
            json_abilities: str = file.read()
        for name, data in json.loads(json_abilities).items():
            self.abilities[name] = Ability(self, data["name"], data["requirements"], data["actions"])

    def load_conditions(self):
        with open(self.conditions_file, "r") as file:
            json_conditions: str = file.read()
        for name, data in json.loads(json_conditions).items():
            self.conditions[name] = Condition(data["name"], data["active"])

    def load_resources(self):
        with open(self.resources_file, "r") as file:
            json_resources: str = file.read()
        for name, data in json.loads(json_resources).items():
            self.resources[name] = Resource(data["name"], data["amount"], data["maxAmount"])