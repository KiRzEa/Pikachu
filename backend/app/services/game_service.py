"""
Game service managing board state and operations.

Key DSA Concepts:
1. Fisher-Yates Shuffle - O(n) randomization algorithm
2. Hash Map - Quick lookup of pokemon positions
3. Backtracking - Find all valid moves
4. 2D Matrix operations
"""

import random
from typing import List, Optional, Tuple, Dict
from ..models.game import (
    Cell, CellType, Position, GameBoard,
    GameState, MatchResult
)
from ..core.pathfinder import PathFinder


class GameService:
    """Manages game state and operations."""

    # Pokemon IDs for different characters (20 different types)
    POKEMON_TYPES = list(range(1, 21))

    def __init__(self, rows: int = 8, cols: int = 12, pokemon_types: int = 20):
        self.rows = rows
        self.cols = cols
        self.pokemon_types = pokemon_types

    def create_new_game(self, level: int = 1) -> GameState:
        """
        Create a new game board with randomly distributed Pokemon.

        Algorithm:
        1. Calculate how many pairs we need (rows * cols must be even)
        2. Create list of pokemon pairs
        3. Shuffle using Fisher-Yates
        4. Populate grid

        Time Complexity: O(rows * cols)
        """
        total_cells = self.rows * self.cols

        # Ensure even number of cells
        if total_cells % 2 != 0:
            raise ValueError("Grid must have even number of cells")

        # Create pairs of pokemon
        num_pairs = total_cells // 2

        # Distribute pokemon types evenly
        pokemon_list = []
        pokemon_per_type = num_pairs // self.pokemon_types

        for pokemon_id in self.POKEMON_TYPES:
            pokemon_list.extend([pokemon_id] * 2)  # Each appears twice (one pair)

        # If we need more pairs, add random pokemon
        while len(pokemon_list) < total_cells:
            pokemon_list.append(random.choice(self.POKEMON_TYPES))
            pokemon_list.append(pokemon_list[-1])  # Add matching pair

        # Fisher-Yates shuffle - O(n)
        self._shuffle_list(pokemon_list)

        # Create grid without padding
        grid = []
        idx = 0

        for row in range(self.rows):
            grid_row = []
            for col in range(self.cols):
                cell = Cell(
                    type=CellType.POKEMON,
                    pokemon_id=pokemon_list[idx],
                    is_frozen=False
                )
                idx += 1
                grid_row.append(cell)
            grid.append(grid_row)

        # Add ice for higher levels
        if level > 3:
            self._add_ice_blocks(grid, level, self.rows, self.cols)

        board = GameBoard(
            grid=grid,
            rows=self.rows,
            cols=self.cols,
            time_remaining=300,  # 5 minutes
            lives=5,
            level=level,
            score=0
        )

        return GameState(board=board, game_over=False, victory=False)

    def _shuffle_list(self, items: List[int]) -> None:
        """
        Fisher-Yates shuffle algorithm - in-place randomization.

        Time Complexity: O(n)
        Space Complexity: O(1)

        Algorithm:
        - Iterate from last to first
        - For each position i, pick random index j from [0, i]
        - Swap items[i] and items[j]
        """
        for i in range(len(items) - 1, 0, -1):
            j = random.randint(0, i)
            items[i], items[j] = items[j], items[i]

    def _add_ice_blocks(self, grid: List[List[Cell]], level: int, rows: int, cols: int) -> None:
        """Add ice blocks to increase difficulty."""
        num_ice = min(level - 3, rows * cols // 4)

        ice_positions = set()
        while len(ice_positions) < num_ice:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            ice_positions.add((row, col))

        for row, col in ice_positions:
            grid[row][col].is_frozen = True

    def make_move(self, game_state: GameState, pos1: Position, pos2: Position) -> Tuple[bool, Optional[MatchResult]]:
        """
        Process a player move.

        Returns: (success, match_result)
        """
        board = game_state.board
        pathfinder = PathFinder(board.grid, board.rows, board.cols)

        # Find path between positions
        result = pathfinder.find_path_simple(pos1, pos2)

        if result.is_valid:
            # Remove matched pokemon
            board.grid[pos1.row][pos1.col] = Cell(type=CellType.EMPTY)
            board.grid[pos2.row][pos2.col] = Cell(type=CellType.EMPTY)

            # Remove adjacent ice
            self._remove_adjacent_ice(board.grid, pos1)
            self._remove_adjacent_ice(board.grid, pos2)

            # Update score
            board.score += 10 * (4 - result.turns)  # Fewer turns = more points

            # Check if board is clear
            if self._is_board_clear(board.grid):
                game_state.victory = True

            return True, result

        return False, None

    def _remove_adjacent_ice(self, grid: List[List[Cell]], pos: Position) -> None:
        """Remove ice from adjacent cells."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        rows = len(grid)
        cols = len(grid[0]) if grid else 0

        for dr, dc in directions:
            new_row, new_col = pos.row + dr, pos.col + dc

            if (0 <= new_row < rows and
                0 <= new_col < cols):
                grid[new_row][new_col].is_frozen = False

    def _is_board_clear(self, grid: List[List[Cell]]) -> bool:
        """Check if all pokemon are removed."""
        for row in grid:
            for cell in row:
                if cell.type == CellType.POKEMON:
                    return False
        return True

    def shuffle_board(self, game_state: GameState) -> bool:
        """
        Shuffle remaining pokemon on board when no valid moves exist.

        Algorithm:
        1. Collect all remaining pokemon
        2. Shuffle using Fisher-Yates
        3. Redistribute to same positions

        Time Complexity: O(rows * cols)
        """
        board = game_state.board

        # Collect all pokemon and their positions
        pokemon_list = []
        positions = []

        for row in range(board.rows):
            for col in range(board.cols):
                cell = board.grid[row][col]
                if cell.type == CellType.POKEMON:
                    pokemon_list.append(cell.pokemon_id)
                    positions.append((row, col))

        if not pokemon_list:
            return False

        # Shuffle pokemon
        self._shuffle_list(pokemon_list)

        # Redistribute
        for i, (row, col) in enumerate(positions):
            board.grid[row][col].pokemon_id = pokemon_list[i]

        # Reduce lives
        board.lives -= 1

        if board.lives <= 0:
            game_state.game_over = True

        return True

    def find_hint(self, game_state: GameState) -> Optional[Tuple[Position, Position]]:
        """
        Find a valid move as a hint.

        Algorithm:
        1. Group pokemon by type using hash map - O(rows * cols)
        2. For each pair of same type, check if path exists - O(n^2) worst case
        3. Return first valid pair found

        Time Complexity: O(n^2) where n = number of pokemon on board
        """
        board = game_state.board

        # Hash map: pokemon_id -> list of positions
        pokemon_positions: Dict[int, List[Position]] = {}

        for row in range(board.rows):
            for col in range(board.cols):
                cell = board.grid[row][col]
                if cell.type == CellType.POKEMON and not cell.is_frozen:
                    pos = Position(row=row, col=col)
                    if cell.pokemon_id not in pokemon_positions:
                        pokemon_positions[cell.pokemon_id] = []
                    pokemon_positions[cell.pokemon_id].append(pos)

        # Try to find valid pair
        pathfinder = PathFinder(board.grid, board.rows, board.cols)

        for pokemon_id, positions in pokemon_positions.items():
            # Check all pairs of same pokemon type
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    result = pathfinder.find_path_simple(positions[i], positions[j])
                    if result.is_valid:
                        return positions[i], positions[j]

        return None

    def has_valid_moves(self, game_state: GameState) -> bool:
        """Check if any valid moves exist."""
        return self.find_hint(game_state) is not None

    def update_time(self, game_state: GameState, seconds: int) -> None:
        """Update remaining time."""
        board = game_state.board
        board.time_remaining -= seconds

        if board.time_remaining <= 0:
            board.time_remaining = 0
            game_state.game_over = True
