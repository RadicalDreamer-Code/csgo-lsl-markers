import csv
from dataclasses import asdict
from datetime import datetime
from event_flags import Event
from os.path import exists

CSV_DIC: str = "data/"


class Writer:
    def __init__(self, csv_path=None) -> None:
        created_at = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        self.filename = f"CSGO {created_at}.csv"

        if exists(CSV_DIC + self.filename):
            raise FileExistsError

        # write header
        with open(CSV_DIC + self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            dummy_event = asdict(Event())
            writer.writerow(dummy_event.keys())

    def write_to_csv(self, event: Event):
        event_dict = asdict(event)
        field_names = event_dict.keys()
        print(f"[Writer] create timestamp entry for {event.name}")
        with open(CSV_DIC + self.filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writerow(event_dict)
