from dotenv import dotenv_values
from event_flags import Event, EventFlags
from gsi.gamestate import GameState
from gsi.information import Map, Player, State
from gsi.server import GSIServer

event_flags = EventFlags()

# add functions here which should react to events
@event_flags.subscribe
def test(event: Event):
    print(event.__dict__)


# is called when gamestate is received from game
def callback(data: GameState):
    global event_flags

    # should be in running game
    if not data.player.state:
        return

    state = (
        data.player.state.__dict__
        if isinstance(data.player.state, State)
        else data.player.state
    )

    event_flags.alive = (state.get("health") or 0) > 0
    event_flags.flashed = (state.get("flashed") or 0) > 0
    event_flags.smoked = (state.get("smoked") or 0) > 0
    event_flags.burning = (state.get("burning") or 0) > 0
    event_flags.kills = state.get("round_kills") or 0

    event_flags.round = data.map.round


if __name__ == "__main__":
    key_data = dotenv_values(".env")
    key = key_data.get("key")
    if key is None:
        print("key not found. .env created?")

    server = GSIServer(("0.0.0.0", 3000), key, callback)
    server.start_server()

    while True:
        pass
