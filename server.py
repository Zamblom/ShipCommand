import socket
import threading
import typing

import typeguard

import application


class Server:
    @typeguard.typechecked
    def __init__(self, app: application.Application) -> None:
        self.running: bool = False

        self.application: application.Application = app

        self.ip: str = "0.0.0.0"
        self.port: int = 80
        self.socket: typing.Optional[socket.socket] = None

        self.main_thread: threading.Thread = threading.Thread(target=self.handle_requests, daemon=True)

    @typeguard.typechecked
    def start(self) -> None:
        self.running = True
        self.socket = socket.socket()
        self.socket.settimeout(1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(20)
        self.main_thread.start()

    @typeguard.typechecked
    def stop(self) -> None:
        self.running = False

    @typeguard.typechecked
    def replace_application(self, app: application.Application) -> None:
        self.application = app

    @typeguard.typechecked
    def handle_requests(self) -> None:
        while self.running:
            try:
                self.handle_request(*self.socket.accept())
            except TimeoutError:
                pass

    # noinspection PyUnusedLocal
    @typeguard.typechecked
    def handle_request(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        conn.settimeout(1)

        try:
            request: str = conn.recv(1024).decode("utf-8")
        except (ConnectionAbortedError, ConnectionResetError, UnicodeDecodeError, TimeoutError):
            conn.close()
            return

        if request.startswith("GET"):
            page: str = request.split()[1].split("?")[0]

            parameters: dict[str, str] = {}
            if "?" in request.split()[1].strip("/"):
                for param in request.split()[1].strip("/").split("?")[1].split("&"):
                    parameters[param.split("=")[0]] = param.split("=")[1]

            cookies: dict[str, str] = {}
            if "Cookie: " in request:
                cookie_list: list[str] = request.split("Cookie: ")[1].split("\r\n")[0].split("; ")
                for cookie in cookie_list:
                    key, value = cookie.split("=")
                    cookies[key] = value

            if page in self.application.GET:
                header, payload = self.application.GET[page][0](parameters, cookies, self.application.GET[page][1])
                conn.send(header + payload)
            else:
                print(page)
        elif request.startswith("POST"):
            print(request)
        else:
            print(request)

        conn.close()
