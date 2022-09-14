from dataclasses import dataclass, field
from datetime import datetime
from itertools import count
from typing import Callable, List

EVENT_ROUND_START = "Round started"
EVENT_ROUND_END = "Round end"
EVENT_PLAYER_KILL = "Player kill"
EVENT_PLAYER_DIES = "Player dies"
EVENT_PLAYER_IN_SMOKE_START = "Player inside smoke"
EVENT_PLAYER_IN_SMOKE_END = "Player outside smoke again"
EVENT_PLAYER_BURNING_START = "Player is burning"
EVENT_PLAYER_BURNING_END = "Player is not burning anymore"
EVENT_PLAYER_FLASHED_START = "Player is flashed"
EVENT_PLAYER_FLASHED_END = "Player is not flashed anymore"

counter = count()


@dataclass
class Event:
    # index: int = field(default_factory=lambda: next(counter))
    name: str = ""
    value: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class EventFlags:
    _observers: List[Callable[[Event], None]] = field(default_factory=list)

    observer_slot: int = -1  # observer_slot indicates which player is currently watched
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
                self._on_change(EVENT_PLAYER_DIES)
            self._alive = v

    @property
    def smoked(self) -> bool:
        return self._smoked

    @smoked.setter
    def smoked(self, v: bool) -> None:
        if self._smoked is not v:
            print(f"player is smoked: {v}")

            if v:
                self._on_change(EVENT_PLAYER_IN_SMOKE_START)
            else:
                self._on_change(EVENT_PLAYER_IN_SMOKE_END)

            self._smoked = v

    @property
    def flashed(self) -> bool:
        return self._flashed

    @flashed.setter
    def flashed(self, v: bool) -> None:
        if self._flashed is not v:
            print(f"player is flashed: {v}")

            if v:
                self._on_change(EVENT_PLAYER_FLASHED_START)
            else:
                self._on_change(EVENT_PLAYER_FLASHED_END)

            self._flashed = v

    @property
    def burning(self) -> bool:
        return self._burning

    @burning.setter
    def burning(self, v: bool) -> None:
        if self._burning is not v:
            print(f"player is burning: {v}")

            if v:
                self._on_change(EVENT_PLAYER_BURNING_START)
            else:
                self._on_change(EVENT_PLAYER_BURNING_END)

            self._burning = v

    @property
    def kills(self) -> int:
        return self._kills

    @kills.setter
    def kills(self, v: int) -> None:
        if self._kills is not v and v != 0:
            print(f"kills: {v}")
            self._on_change(EVENT_PLAYER_KILL, v)
            self._kills = v

    @property
    def round(self) -> int:
        return self._round

    @round.setter
    def round(self, v: int) -> None:
        if self._round is not v:
            print(f"round: {v}")
            self._on_change(EVENT_ROUND_END)
            self._round = v

    def subscribe(self, func: Callable[[Event], None]) -> None:
        self._observers.append(func)

    """_summary_
    Notify all subscribers/observers by passing the state of the event.
    
    """

    def _on_change(self, event_name: str, value: int = 0):
        for observer in self._observers:
            if not callable(observer):
                continue

            print("new event")
            event = Event(event_name, value)
            observer(event)
