import typing

import typeguard

import quantity


class Room:
    @typeguard.typechecked
    def __init__(self, connections: typing.Optional[list[str]] = None, abilities: typing.Optional[list[str]] = None, link: str = "") -> None:
        connections = [] if connections is None else connections
        abilities = [] if abilities is None else abilities

        self.connections: list[str] = connections
        self.abilities: list[str] = abilities
        self.link: str = link
        self.players: list[str] = []

    @typeguard.typechecked
    def add_player(self, player: str) -> bool:
        if player in self.players:
            return False

        self.players.append(player)
        return True

    @typeguard.typechecked
    def remove_player(self, player: str) -> bool:
        if player not in self.players:
            return False

        self.players.remove(player)
        return True

    @typeguard.typechecked
    def has_players(self) -> bool:
        return len(self.players) > 0

    @typeguard.typechecked
    def has_link(self) -> bool:
        return self.link != ""


class Ship:
    @typeguard.typechecked
    def __init__(self) -> None:
        self.rooms: dict[str, Room] = {
            "gunTurretB": Room(connections=["hatchFromGunTurretB"]),
            "hatchFromGunTurretB": Room(link="corridor"),
            "gunTurretC": Room(connections=["hatchFromGunTurretC"]),
            "hatchFromGunTurretC": Room(link="corridor"),
            "corridor": Room(connections=["ladderToDeckA", "gunBayB", "gunBayC", "gunBayD"]),
            "gunBayC": Room(link="gunTurretB"),
            "gunBayB": Room(link="gunTurretB"),
            "gunBayD": Room(connections=["corridor"]),
            "ladderToDeckA": Room(link="hallway"),
            "sledBay": Room(connections=["hallway", "hatchToSledA", "hatchToSledB"]),
            "engineersQuarter": Room(connections=["hallway", "cargoHold"]),
            "cargoHold": Room(connections=["hallway", "engineersQuarter"]),
            "medBay": Room(connections=["hallway"]),
            "cockpit": Room(connections=["security"], abilities=["evasiveManoeuvres", "deployFlares", "enterWarp"]),
            "brig": Room(connections=["monitoring"]),
            "monitoring": Room(connections=["hallway", "brig"], abilities=["lockBrigCell", "unlockBrigCell"]),
            "livingArea": Room(connections=["hallway", "workshop", "messHall", "crewQuarters"]),
            "messHall": Room(connections=["livingArea"]),
            "crewQuarters": Room(connections=["livingArea"]),
            "workshop": Room(connections=["hallway", "livingArea"]),
            "hallway": Room(connections=["sledBay", "engineersQuarter", "cargoHold", "medBay", "security", "monitoring", "livingArea", "workshop", "ladderToDeckB", "hatchToGunTurretA"]),
            "security": Room(connections=["hallway", "cockpit"]),
            "ladderToDeckB": Room(link="corridor"),
            "hatchToGunTurretA": Room(link="hallway"),
            "hatchToSledA": Room(link="hallway"),
            "hatchToSledB": Room(link="hallway"),
        }

        self.abilities: dict[str, bool] = {
            "evasiveManoeuvres": True,
            "deployFlares": True,
            "enterWarp": True,
            "lockBrigCell": True,
            "unlockBrigCell": False
        }

        self.conditions: dict[str, bool] = {
            "evasive": False,
            "heatSeeking": True,
            "targetLocked": True,
        }

        self.resources: dict[str, quantity.Quantity] = {
            "fuel": quantity.Quantity(6, 6),
            "flares": quantity.Quantity(5, 5)
        }

    @typeguard.typechecked
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

    @typeguard.typechecked
    def get_room_by_player(self, player: str) -> str:
        for room_name, room in self.rooms.items():
            if player in room.players:
                return room_name

    @typeguard.typechecked
    def get_connections_by_player(self, player: str) -> list[str]:
        return self.rooms[self.get_room_by_player(player)].connections

    @typeguard.typechecked
    def validate_abilities(self) -> None:
        self.abilities["deployFlares"] = not self.resources["flares"].is_empty()
        self.abilities["enterWarp"] = not self.resources["fuel"].is_empty()

    @typeguard.typechecked
    def use_ability(self, player: str, ability: str) -> bool:
        if not self.abilities[ability]:
            return False

        current_room: str = self.get_room_by_player(player)

        match ability:
            case "evasiveManoeuvres":
                # Set condition[target_locked], Clear condition[target_locked]
                if current_room not in ["cockpit"]:
                    return False

                self.conditions["evasive"] = True
                self.conditions["targetLocked"] = False

                self.abilities["evasiveManoeuvres"] = False

            case "enterWarp":
                # Expend 1 resource[fuel], Set condition[enter_warp]
                if current_room not in ["cockpit"]:
                    return False

                if not self.resources["fuel"].expend(1):
                    return False

            case "deployFlares":
                # Expend 1 resource[flare], Clear condition[heat_seeking]
                if current_room not in ["cockpit"]:
                    return False

                if not self.resources["flares"].expend(1):
                    return False

                self.conditions["heatSeeking"] = False

            case "lockBrigCell":
                # Remove connection[monitoring -> brig], Remove connection[brig -> monitoring]
                if current_room not in ["monitoring"]:
                    return False

                if "brig" not in self.rooms["monitoring"].connections:
                    return False

                if "monitoring" not in self.rooms["brig"].connections:
                    return False

                self.rooms["monitoring"].connections = ["hallway"]
                self.rooms["brig"].connections = []

                self.abilities["lockBrigCell"] = False
                self.abilities["unlockBrigCell"] = True

            case "unlockBrigCell":
                # Add connection[monitoring -> brig], Add connection[brig -> monitoring]
                if current_room not in ["monitoring"]:
                    return False

                if "brig" in self.rooms["monitoring"].connections:
                    return False

                if "monitoring" in self.rooms["brig"].connections:
                    return False

                self.rooms["monitoring"].connections = ["hallway", "brig"]
                self.rooms["brig"].connections = ["monitoring"]

                self.abilities["unlockBrigCell"] = False
                self.abilities["lockBrigCell"] = True

        self.validate_abilities()
        return True

    @typeguard.typechecked
    def get_rooms_with_players(self) -> dict[str, list[str]]:
        return {room_name: room.players for room_name, room in self.rooms.items() if room.has_players()}

    @typeguard.typechecked
    def get_abilities(self) -> dict[str, dict[str, bool]]:
        return {ability: {"enabled": enabled} for ability, enabled in self.abilities.items()}

    @typeguard.typechecked
    def get_conditions(self) -> dict[str, dict[str, bool]]:
        return {condition: {"active": active} for condition, active in self.conditions.items()}

    @typeguard.typechecked
    def get_resources(self) -> dict[str, dict[str, int]]:
        return {resource_name: {"amount": resource.amount, "maxAmount": resource.max_amount} for resource_name, resource in self.resources.items()}
