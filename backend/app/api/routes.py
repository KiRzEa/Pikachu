"""
FastAPI routes for Pikachu Kawaii game.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from ..models.game import GameState, MoveRequest, Position
from ..services.game_service import GameService
from ..services.pokemon_data import get_all_pokemon_data


router = APIRouter()

# In-memory game storage (for demo - use database in production)
games: Dict[str, GameState] = {}
game_service = GameService(rows=8, cols=12)


@router.post("/game/new")
async def create_game(level: int = 1):
    """
    Create a new game.

    DSA Operations:
    - Fisher-Yates shuffle for board generation
    - 2D matrix initialization
    """
    game_state = game_service.create_new_game(level=level)
    game_id = f"game_{len(games)}"
    games[game_id] = game_state

    return {
        "game_id": game_id,
        "game_state": game_state
    }


@router.get("/game/{game_id}", response_model=GameState)
async def get_game(game_id: str):
    """Get current game state."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    return games[game_id]


@router.post("/game/{game_id}/move")
async def make_move(game_id: str, move: MoveRequest):
    """
    Make a move by connecting two Pokemon.

    DSA Operations:
    - Pathfinding with BFS
    - Turn constraint validation
    - Grid updates

    Returns:
    - success: bool
    - path: List of positions if valid
    - turns: Number of turns in path
    - game_state: Updated game state
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game_state = games[game_id]

    if game_state.game_over or game_state.victory:
        raise HTTPException(status_code=400, detail="Game is already finished")

    success, result = game_service.make_move(game_state, move.pos1, move.pos2)

    if not success:
        return {
            "success": False,
            "message": "Invalid move - no valid path exists",
            "game_state": game_state
        }

    # Check if shuffle is needed
    if not game_service.has_valid_moves(game_state) and not game_state.victory:
        game_service.shuffle_board(game_state)

    return {
        "success": True,
        "path": result.path,
        "turns": result.turns,
        "game_state": game_state
    }


@router.post("/game/{game_id}/hint")
async def get_hint(game_id: str):
    """
    Get a hint for a valid move.

    DSA Operations:
    - Hash map for grouping pokemon by type
    - Pathfinding for each potential pair
    - Early termination on first valid path
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game_state = games[game_id]

    if game_state.game_over or game_state.victory:
        raise HTTPException(status_code=400, detail="Game is already finished")

    hint = game_service.find_hint(game_state)

    if hint is None:
        return {
            "hint_available": False,
            "message": "No valid moves available - shuffling board"
        }

    pos1, pos2 = hint
    return {
        "hint_available": True,
        "pos1": pos1,
        "pos2": pos2
    }


@router.post("/game/{game_id}/shuffle")
async def shuffle_board(game_id: str):
    """
    Manually shuffle the board (costs 1 life).

    DSA Operations:
    - Fisher-Yates shuffle algorithm
    - In-place array manipulation
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game_state = games[game_id]

    if game_state.game_over or game_state.victory:
        raise HTTPException(status_code=400, detail="Game is already finished")

    success = game_service.shuffle_board(game_state)

    if not success:
        raise HTTPException(status_code=400, detail="No pokemon to shuffle")

    return {
        "success": True,
        "lives_remaining": game_state.board.lives,
        "game_state": game_state
    }


@router.post("/game/{game_id}/time")
async def update_time(game_id: str, seconds_elapsed: int):
    """Update game time."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game_state = games[game_id]
    game_service.update_time(game_state, seconds_elapsed)

    return {
        "time_remaining": game_state.board.time_remaining,
        "game_over": game_state.game_over
    }


@router.delete("/game/{game_id}")
async def delete_game(game_id: str):
    """Delete a game."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    del games[game_id]
    return {"message": "Game deleted successfully"}


@router.get("/pokemon")
async def get_pokemon_data():
    """
    Get all Pokemon data with sprite URLs.

    Returns Pokemon information including:
    - Game ID (1-20)
    - Pokemon name
    - Pokedex ID
    - Sprite URL from PokeAPI
    """
    return {"pokemon": get_all_pokemon_data()}
