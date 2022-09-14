from dotenv import dotenv_values
from event_flags import Event, EventFlags
from gsi.gamestate import GameState
from gsi.information import Map, Player, State
from gsi.server import GSIServer
from lsl_outlet import send_marker
from writer import Writer

event_flags = EventFlags()
csv_writer = Writer()

# add functions here which should react to events
@event_flags.subscribe
def send_to_lsl_stream(event: Event):
    send_marker(event.name)


@event_flags.subscribe
def write_to_csv(event: Event):
    csv_writer.write_to_csv(event)
    pass


# is called when gamestate is received from game
def callback(data: GameState):
    global event_flags

    # TODO: wait till game starts

    # should be in running game
    if not data.player.state:
        return

    # TODO: Filter spectator-target
    # print(data.player.__dict__)

    state = (
        data.player.state.__dict__
        if isinstance(data.player.state, State)
        else data.player.state
    )

    # remember which observer slot the active player has
    event_flags.observer_slot = (
        data.player.observer_slot
        if event_flags.observer_slot == -1 or data.player.observer_slot is None
        else event_flags.observer_slot
    )

    # map data
    event_flags.round = data.map.round

    # player data
    if data.player.observer_slot != event_flags.observer_slot:
        return

    event_flags.alive = (state.get("health") or 0) > 0
    event_flags.flashed = (state.get("flashed") or 0) > 0
    event_flags.smoked = (state.get("smoked") or 0) > 0
    event_flags.burning = (state.get("burning") or 0) > 0
    event_flags.kills = state.get("round_kills") or 0


if __name__ == "__main__":
    key_data = dotenv_values(".env")
    key = key_data.get("key")
    if key is None:
        print("key not found. .env created?")

    server = GSIServer(("0.0.0.0", 3000), key, callback)
    server.start_server()

    while True:
        pass
