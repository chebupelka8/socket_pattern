import socket
import json

import threading

from typing import Tuple, Never
from notify import ServerNotifier

from dataclasses import dataclass

HOST, PORT = 'localhost', 5050


@dataclass
class User:
    id: int
    address: Tuple[str, int]
    sock: socket.socket
    name: str


class Server:
    def __init__(self, addr: Tuple[str, int]) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen()

        ServerNotifier.start_server()  # notify about the start

        # variables setup: --
        self.__is_working = True
        self.__clients: list[socket.socket] = []
        self.__users: list[User] = []

    def listen(self) -> Never:
        ServerNotifier.listening_server()

        while self.__is_working:
            client, address = self.server.accept()
            self.__clients.append(client)

            ServerNotifier.notify_connected(address)  # notify about the connect client

            threading.Thread(target=self.handle_client, args=(client, address)).start()  # start handle client

    def __disconnect_client(self, address: Tuple[str, int], client, user) -> None:
        ServerNotifier.notify_disconnected(address)
        self.__clients.remove(client)
        self.__users.remove(user)

    def __send(self, data: dict, client: socket.socket) -> None:
        client.send(bytes(json.dumps(data), "utf-8"))

    def __get_users_data(self) -> list[dict]:
        result = []

        for user in self.__users:
            result.append({
                "id": user.id,
                "address": user.address,
                "name": user.name
            })

        return result

    def handle_client(self, client: socket.socket, address: Tuple[str, int]) -> None:
        user = User(len(self.__clients), address, client, "hello"[:len(self.__clients)])
        self.__users.append(user)

        while True:
            try:
                recv = client.recv(1024)

                if not recv:  # if client disconnect
                    self.__disconnect_client(address, client, user)
                    break

                data = json.loads(client.recv(1024).decode('utf-8'))
                print("i")

                if data["request"] == "get_users":
                    self.__send({
                        "response": "get_users",
                        "users": self.__get_users_data()
                    }, client)

            except (ConnectionResetError, OSError):
                self.__disconnect_client(address, client, user)
                break


if __name__ == '__main__':
    server = Server((HOST, PORT))
    server.listen()