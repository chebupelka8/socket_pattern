import socket
import json

import threading

from typing import Tuple, Never
from notify import ClientNotifier

HOST, PORT = 'localhost', 5050


class Client:
    def __init__(self, address: Tuple[str, int]) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(address)

        ClientNotifier.connection_notify(address)  # notify about the connection

        # variable setup: --
        self.__address = address
        self.__users = []

        # start receive in the new thread: --
        threading.Thread(target=self.receive).start()

    def get_response(self) -> dict:
        return json.loads(self.client.recv(1024).decode('UTF-8'))

    def __send(self, data: dict) -> None:
        self.client.send(bytes(json.dumps(data), "utf-8"))

    # def change_name(self, __name: str) -> None:

    def receive(self) -> Never:
        while True:
            try:
                self.__send({
                    "request": "get_users"
                })

                received = self.get_response()
                print(received)

                if received["response"] == "get_users":
                    self.__users = received["users"]

            except (ConnectionResetError, OSError):
                ClientNotifier.disconnection_notify(self.__address, "Server has broken the connection")
                self.client.close()
                break

    def __repr__(self) -> str:
        return f'Client(address={self.__address})'


if __name__ == '__main__':
    client = Client((HOST, PORT))
