from time import sleep
from pylsl import StreamOutlet, StreamInfo

info = StreamInfo(
    name="DataSyncMarker",
    type="Tags",
    channel_count=1,
    channel_format="string",
    source_id="12345",
)

outlet = StreamOutlet(info)


def send_marker(name):
    print(f"Send: {name}")
    outlet.push_sample([name])
