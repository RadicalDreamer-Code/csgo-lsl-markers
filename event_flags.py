from dataclasses import dataclass
from lsl_outlet import send_marker


@dataclass
class EventFlags:
    _alive: bool = False
    _smoked: bool = False
    _flashed: bool = False
    _burning: bool = False
    _kills: int = 0

    _round: int = 0

    @property
    def alive(self) -> bool:
        return self._alive

    @alive.setter
    def alive(self, v: bool) -> None:
        if self._alive is not v:
            print(f"player is alive: {v}")
            if not v:
                send_marker("player died")
            self._alive = v

    @property
    def smoked(self) -> bool:
        return self._smoked

    @smoked.setter
    def smoked(self, v: bool) -> None:
        if self._smoked is not v:
            print(f"player is smoked: {v}")

            if v:
                send_marker("smoke started")
            else:
                send_marker("smoke ended")

            self._smoked = v

    @property
    def flashed(self) -> bool:
        return self._flashed

    @flashed.setter
    def flashed(self, v: bool) -> None:
        if self._flashed is not v:
            print(f"player is flashed: {v}")

            if v:
                send_marker("flash started")
            else:
                send_marker("flash ended")

            self._flashed = v

    @property
    def burning(self) -> bool:
        return self._burning

    @burning.setter
    def burning(self, v: bool) -> None:
        if self._burning is not v:
            print(f"player is burning: {v}")

            if v:
                send_marker("burning started")
            else:
                send_marker("burning ended")

            self._burning = v

    @property
    def kills(self) -> int:
        return self._kills

    @kills.setter
    def kills(self, v: int) -> None:
        if self._kills is not v and v != 0:
            print(f"kills: {v}")
            send_marker("kill")
            self._kills = v

    @property
    def round(self) -> int:
        return self._round

    @round.setter
    def round(self, v: int) -> None:
        if self._round is not v:
            print(f"round: {v}")
            send_marker(f"round {v} ended")
            self._round = v
