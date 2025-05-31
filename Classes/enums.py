from __future__ import annotations
from enum import Enum

class Goal(str, Enum):
    lose = "lose"
    maintain = "maintain"
    gain = "gain"

    @property
    def description(self):
        return {
            Goal.lose: "Похудение",
            Goal.maintain: "Поддержание формы",
            Goal.gain: "Набор массы"
        }[self]
    
    @property
    def index(self) -> int:
        return {
            Goal.lose: 0,
            Goal.maintain: 1,
            Goal.gain: 2
        }[self]

    @classmethod
    def from_index(cls, idx: int) -> Goal:
        return [
            cls.lose,
            cls.maintain,
            cls.gain
        ][idx]
    