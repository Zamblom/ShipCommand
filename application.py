import os
import typing

import json
import typeguard

import player
import ship


class Application:
    @typeguard.typechecked
    def __init__(self):
        self.GET: dict[str, tuple[typing.Callable, list[any]]] = {
            "/": (self.get_landing_page, ["landing_page.html"]),
            "/main": (self.get_main, ["main.html"]),
            "/override": (self.get_override, ["override.html"]),
            "/main.css": (self.get_css, ["main.css"]),
            "/dice.css": (self.get_css, ["dice.css"]),
            "/common.js": (self.get_js, ["common.js"]),
            "/helpers.js": (self.get_js, ["helpers.js"]),
            "/updateHandlers.js": (self.get_js, ["updateHandlers.js"]),
            "/customElements.js": (self.get_js, ["customElements.js"]),
            "/main.js": (self.get_js, ["main.js"]),
            "/override.js": (self.get_js, ["override.js"]),
            "/dice.js": (self.get_js, ["dice.js"]),
            "/favicon.ico": (self.get_image, ["image/ico", "favicon.ico"]),
            "/deck_a.png": (self.get_image, ["image/png", "deck_a.png"]),
            "/deck_b.png": (self.get_image, ["image/png", "deck_b.png"]),
            "/api/player_statistics": (self.api_player_statistics, []),
            "/api/state": (self.api_state, []),
            "/api/move_to_room": (self.api_move_to_room, []),
            "/api/use_ability": (self.api_use_ability, [])
        }

        self.default_header: str = "\r\n".join([
            "HTTP/1.1 200 OK",
            "Content-Type: {data_type}; charset=utf-8",
            "\r\n"
        ])

        self.players: dict[str, player.Player] = {
            file.strip(".pdf"): player.Player(file.strip(".pdf")) for file in os.listdir("players") if
            os.path.isfile(f"players/{file}")
        }

        self.ship: ship.Ship = ship.Ship()

        for person in self.players:
            self.ship.rooms["cockpit"].add_player(person)

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def request_error(self) -> tuple[bytes, bytes]:
        header: bytes = "\r\n".join([
            "HTTP/1.1 404 NOT FOUND",
            "Content-Type: text/data; charset=utf-8",
            "\r\n"
        ]).encode()

        payload: bytes = "404 NOT FOUND - Get Fucked James ;)\nCan't Believe you Broke My Shit AGAIN".encode("utf-8")

        return header, payload

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def get_landing_page(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = self.default_header.replace("{data_type}", "text/html").encode("utf-8")

        filename: str = data[0]
        with open("./html/" + filename, "r") as file:
            decoded_payload: str = file.read()

        players: str = ""
        for person, details in self.players.items():
            players += "<a href='/main?player=" + person + "'>" + details.name + "</a><br>"

        decoded_payload = decoded_payload.replace("{players}", players)

        return header, decoded_payload.encode("utf-8")

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def get_main(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [player], cookies -> [], data -> [filename] """

        header: bytes = ((self.default_header
                         .replace("{data_type}", "text/html")
                         .replace("\r\n\r\n", "\r\nset-cookie: player=" + parameters['player'] + "\r\n\r\n"))
                         .encode("utf-8"))

        filename: str = data[0]
        with open("./html/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def get_override(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = ((self.default_header
                         .replace("{data_type}", "text/html")
                         .replace("\r\n\r\n", "\r\nset-cookie: player=DM\r\n\r\n"))
                         .encode("utf-8"))

        filename: str = data[0]
        with open("./html/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def get_html(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = self.default_header.replace("{data_type}", "text/html").encode("utf-8")

        filename: str = data[0]
        with open("./html/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def get_css(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = self.default_header.replace("{data_type}", "text/css").encode("utf-8")

        filename: str = data[0]
        with open("./css/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def get_js(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = self.default_header.replace("{data_type}", "text/js").encode("utf-8")

        filename: str = data[0]
        with open("./js/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def get_image(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [], cookies -> [], data -> [data_type, filename] """

        data_type = data[0]
        header: bytes = self.default_header.replace("{data_type}", data_type).encode("utf-8")

        filename = data[1]
        with open("./resources/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def api_player_statistics(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [player], cookies -> [],       data -> []
            parameters -> [],       cookies -> [player], data -> [] """

        if "player" not in parameters and "player" not in cookies:
            return self.request_error()
        if "player" in parameters:
            if parameters["player"] not in self.players:
                return self.request_error()
        if "player" in cookies:
            if cookies["player"] not in self.players:
                return self.request_error()

        header: bytes = self.default_header.replace("{data_type}", "text/data").encode("utf-8")

        player_id: str = parameters["player"] if "player" in parameters else cookies["player"]

        json_payload: dict = {
            "playerData": self.players[player_id].get_data(player_id)
        }

        return header, json.dumps(json_payload).encode()

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def api_state(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [], cookies -> [player], data -> [] """

        if "player" not in cookies:
            return self.request_error()
        if cookies["player"] not in self.players and cookies["player"] != "DM":
            return self.request_error()

        header: bytes = self.default_header.replace("{data_type}", "text/data").encode("utf-8")

        json_payload: dict = {
            "roomsWithPlayers": self.ship.get_rooms_with_players(),
            "abilities": self.ship.get_abilities(),
            "conditions": self.ship.get_conditions(),
            "resources": self.ship.get_resources()
        }

        if cookies["player"] != "DM":
            json_payload["currentRoom"] = self.ship.get_room_by_player(cookies["player"])
            json_payload["connections"] = self.ship.get_connections_by_player(cookies["player"])

        return header, json.dumps(json_payload).encode()

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def api_move_to_room(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [room], cookies -> [player], data -> [] """

        if "room" not in parameters or "player" not in cookies:
            return self.request_error()
        if parameters["room"] not in self.ship.rooms:
            return self.request_error()
        if cookies["player"] not in self.players:
            return self.request_error()

        header: bytes = self.default_header.replace("{data_type}", "text/data").encode("utf-8")

        self.ship.move_player_to_room(cookies["player"], parameters["room"])

        json_payload: dict = {
            "currentRoom": self.ship.get_room_by_player(cookies["player"]),
            "connections": self.ship.get_connections_by_player(cookies["player"])
        }

        return header, json.dumps(json_payload).encode()

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def api_use_ability(self, parameters: dict[str, str], cookies: dict[str, str], data: list[any]) -> tuple[bytes, bytes]:
        """ parameters -> [ability], cookies -> [player], data -> [] """

        if "ability" not in parameters or "player" not in cookies:
            return self.request_error()
        if parameters["ability"] not in self.ship.abilities:
            return self.request_error()
        if cookies["player"] not in self.players:
            return self.request_error()

        header: bytes = self.default_header.replace("{data_type}", "text/data").encode("utf-8")

        self.ship.use_ability(cookies["player"], parameters["ability"])

        json_payload: dict = {
            "connections": self.ship.get_connections_by_player(cookies["player"]),
            "abilities": self.ship.get_abilities(),
            "conditions": self.ship.get_conditions(),
            "resources": self.ship.get_resources()
        }

        return header, json.dumps(json_payload).encode()
