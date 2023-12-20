import datetime
import os
import random
from typing import Any, Callable

import json

import player
import ship


Params = dict[str, str]
Cookies = dict[str, str]
Data = list[str]
Response = tuple[bytes, bytes]


class Application:
    def __init__(self) -> None:
        self.GET: dict[str, tuple[Callable[[Params, Cookies, Data], Response], Data]] = {
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
            "/deckA.png": (self.get_image, ["image/png", "deckA.png"]),
            "/deckB.png": (self.get_image, ["image/png", "deckB.png"]),
            "/api/player_statistics": (self.api_player_statistics, []),
            "/api/state": (self.api_state, []),
            "/api/move_to_room": (self.api_move_to_room, []),
            "/api/roll": (self.api_roll, []),
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

        self.ship: ship.Ship = ship.Ship("ship.json")

        for person in self.players:
            self.ship.data["decks"]["deckA"]["rooms"]["cockpit"]["players"].append(person)

    # noinspection PyUnusedLocal
    @staticmethod
    def request_error() -> Response:
        header: bytes = "\r\n".join([
            "HTTP/1.1 404 NOT FOUND",
            "Content-Type: text/data; charset=utf-8",
            "\r\n"
        ]).encode()

        payload: bytes = "404 NOT FOUND - Get Fucked James ;)\nCan't Believe you Broke My Shit AGAIN".encode("utf-8")

        return header, payload

    # noinspection PyUnusedLocal
    def get_landing_page(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = self.default_header.replace("{data_type}", "text/html").encode("utf-8")

        filename: str = data[0]
        with open("./html/" + filename, "r") as file:
            decoded_payload: str = file.read()

        players: str = ""
        for k, v in self.players.items():
            players += "<a href='/main?player=" + k + "'>" + v.get_name() + "</a><br>"

        decoded_payload = decoded_payload.replace("{players}", players)

        return header, decoded_payload.encode()

    # noinspection PyUnusedLocal
    def get_main(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [player], cookies -> [], data -> [filename] """

        header: bytes = ((self.default_header
                         .replace("{data_type}", "text/html")
                         .replace("\r\n\r\n", "\r\nset-cookie: player=" + parameters['player'] + "\r\n\r\n"))
                         .encode())

        filename: str = data[0]
        with open("./html/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    def get_override(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = ((self.default_header
                         .replace("{data_type}", "text/html")
                         .replace("\r\n\r\n", "\r\nset-cookie: player=DM\r\n\r\n"))
                         .encode())

        filename: str = data[0]
        with open("./html/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    def get_html(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = self.default_header.replace("{data_type}", "text/html").encode("utf-8")

        filename: str = data[0]
        with open("./html/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    def get_css(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = self.default_header.replace("{data_type}", "text/css").encode("utf-8")

        filename: str = data[0]
        with open("./css/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    def get_js(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [], cookies -> [], data -> [filename] """

        header: bytes = self.default_header.replace("{data_type}", "text/js").encode("utf-8")

        filename: str = data[0]
        with open("./js/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    def get_image(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [], cookies -> [], data -> [data_type, filename] """

        data_type = data[0]
        header: bytes = self.default_header.replace("{data_type}", data_type).encode("utf-8")

        filename = data[1]
        with open("./resources/" + filename, "rb") as file:
            payload: bytes = file.read()

        return header, payload

    # noinspection PyUnusedLocal
    def api_player_statistics(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
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

        header: bytes = self.default_header.replace("{data_type}", "application/json").encode("utf-8")

        player_id: str = parameters["player"] if "player" in parameters else cookies["player"]

        json_payload: dict[str, Any] = {"playerData": self.players[player_id].get_data()}

        return header, json.dumps(json_payload).encode()

    # noinspection PyUnusedLocal
    def api_state(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [time], cookies -> [player], data -> [] """

        if "time" not in parameters:
            return self.request_error()
        if "player" not in cookies:
            return self.request_error()
        if cookies["player"] not in self.players and cookies["player"] != "DM":
            return self.request_error()

        time_format: str = "%Y.%m.%d-%H:%M:%S.%f"
        last_time: datetime.datetime = datetime.datetime.strptime(parameters["time"], time_format)

        header: bytes = self.default_header.replace("{data_type}", "application/json").encode("utf-8")

        updates = self.ship.data.get_updated(last_time)
        json_payload = {"time": datetime.datetime.now().strftime(time_format), "data": updates if updates is not None else {}}

        return header, json.dumps(json_payload).encode()

    # noinspection PyUnusedLocal
    def api_move_to_room(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [time, deck, room], cookies -> [player], data -> [] """

        if "deck" not in parameters or "room" not in parameters or "player" not in cookies:
            return self.request_error()
        if parameters["deck"] not in self.ship.data["decks"]:
            return self.request_error()
        if parameters["room"] not in self.ship.data["decks"][parameters["deck"]]["rooms"]:
            return self.request_error()
        if cookies["player"] not in self.players:
            return self.request_error()

        self.ship.move_player_to_room(cookies["player"], parameters["deck"], parameters["room"])

        return self.api_state(parameters, cookies, data)

    # noinspection PyUnusedLocal
    def api_roll(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [modifiers], cookies -> [player], data -> [] """
        if "modifiers" not in parameters:
            return self.request_error()
        if "player" not in cookies or cookies["player"] not in self.players:
            return self.request_error()

        header: bytes = self.default_header.replace("{data_type}", "application/json").encode("utf-8")

        modifiers: list[int] = [int(i) for i in json.loads(parameters["modifiers"])]

        rolls: list[int] = [random.randint(1, 20) for _ in modifiers]
        results: list[int] = [rolls[i] + modifiers[i] for i in range(len(rolls))]

        return header, json.dumps(results).encode()

    # noinspection PyUnusedLocal
    def api_use_ability(self, parameters: Params, cookies: Cookies, data: Data) -> Response:
        """ parameters -> [time, ability], cookies -> [player], data -> [] """

        if "time" not in parameters or "ability" not in parameters or "player" not in cookies:
            return self.request_error()
        if parameters["ability"] not in self.ship.data["abilities"]:
            return self.request_error()
        if cookies["player"] not in self.players:
            return self.request_error()

        rolls: list[int] = json.loads(parameters["rolls"]) if "rolls" in parameters else []
        self.ship.use_ability(cookies["player"], parameters["ability"], rolls)

        return self.api_state(parameters, cookies, data)
