from pydantic import BaseModel
from typing import List, Optional, Tuple
from enum import Enum


class CellType(str, Enum):
    EMPTY = "empty"
    POKEMON = "pokemon"
    ICE = "ice"


class Cell(BaseModel):
    type: CellType
    pokemon_id: Optional[int] = None  # ID of the pokemon (1-20 for different types)
    is_frozen: bool = False  # True if covered by ice


class Position(BaseModel):
    row: int
    col: int


class PathSegment(BaseModel):
    start: Position
    end: Position


class MatchResult(BaseModel):
    is_valid: bool
    path: Optional[List[Position]] = None
    turns: int = 0  # Number of turns in the path (max 3)


class GameBoard(BaseModel):
    grid: List[List[Cell]]
    rows: int
    cols: int
    time_remaining: int
    lives: int
    level: int
    score: int


class MoveRequest(BaseModel):
    pos1: Position
    pos2: Position


class GameState(BaseModel):
    board: GameBoard
    game_over: bool = False
    victory: bool = False
