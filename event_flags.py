from dataclasses import dataclass


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
            self._alive = v

    @property
    def smoked(self) -> bool:
        return self._smoked

    @smoked.setter
    def smoked(self, v: bool) -> None:
        if self._smoked is not v:
            print(f"player is smoked: {v}")
            self._smoked = v

    @property
    def flashed(self) -> bool:
        return self._flashed

    @flashed.setter
    def flashed(self, v: bool) -> None:
        if self._flashed is not v:
            print(f"player is flashed: {v}")
            self._flashed = v

    @property
    def burning(self) -> bool:
        return self._burning

    @burning.setter
    def burning(self, v: bool) -> None:
        if self._burning is not v:
            print(f"player is burning: {v}")
            self._burning = v

    @property
    def kills(self) -> int:
        return self._kills

    @kills.setter
    def kills(self, v: int) -> None:
        if self._kills is not v and v is not 0:
            print(f"kills: {v}")
            self._kills = v

    @property
    def round(self) -> int:
        return self._round

    @round.setter
    def round(self, v: int) -> None:
        if self._round is not v:
            print(f"round: {v}")
            self._round = v
