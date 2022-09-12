from dotenv import dotenv_values
from gsi.gamestate import GameState
from gsi.information import Map, Player
from gsi.server import GSIServer


def callback(data: GameState):
    print(data.player.name)


if __name__ == "__main__":
    key_data = dotenv_values(".env")
    key = key_data.get("key")
    if key is None:
        print("key not found. .env created?")

    print(key)
    server = GSIServer(("0.0.0.0", 3000), key, callback)
    server.start_server()

    while True:
        pass
