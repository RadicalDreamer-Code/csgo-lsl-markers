from dotenv import dotenv_values
from event_flags import EventFlags
from gsi.gamestate import GameState
from gsi.information import Map, Player
from gsi.server import GSIServer


event_flags = EventFlags()

# is called when gamestate is received from game
def callback(data: GameState):
    global event_flags

    # should be in running game
    if not data.player.state:
        return

    event_flags.alive = True if data.player.state.get("health", 0) > 0 else False
    event_flags.flashed = True if data.player.state.get("flashed", 0) > 0 else False
    event_flags.smoked = True if data.player.state.get("smoked", 0) > 0 else False
    event_flags.burning = True if data.player.state.get("burning", 0) > 0 else False
    event_flags.kills = data.player.state.get("round_kills")

    event_flags.round = data.map.round


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
