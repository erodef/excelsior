from enum import Enum, auto


class State(Enum):
    """
    Controls game state
    """
    MENU = auto()
    ROOM_PHASE = auto()
    BATTLE_PHASE = auto()
    UPGD_PHASE = auto()
    ENDING = auto()
    GAMEOVER = auto()
