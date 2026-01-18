"""
Pathfinding algorithm for Pikachu Kawaii game.

Key DSA Concepts:
1. BFS (Breadth-First Search) - Find shortest path with turn constraints
2. Queue - For BFS traversal
3. Set - For visited cell tracking
4. 2D Grid traversal with direction vectors

The algorithm finds a path between two matching Pokemon with max 3 turns (4 line segments).
A "turn" is when the direction changes (horizontal to vertical or vice versa).
"""

from collections import deque
from typing import List, Optional, Tuple
from ..models.game import Cell, Position, MatchResult, CellType


class PathFinder:
    """
    Implements BFS-based pathfinding with turn constraints.

    Time Complexity: O(rows * cols * 4) for BFS traversal
    Space Complexity: O(rows * cols) for queue and visited set
    """

    # Direction vectors: right, down, left, up
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRECTION_NAMES = ['RIGHT', 'DOWN', 'LEFT', 'UP']

    def __init__(self, grid: List[List[Cell]], rows: int, cols: int):
        self.grid = grid
        self.rows = rows
        self.cols = cols

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board boundaries."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_cell_empty(self, row: int, col: int) -> bool:
        """
        Check if a cell is empty or can be passed through.
        Empty cells and the destination cell can be passed.
        """
        if not self.is_valid_position(row, col):
            return False

        cell = self.grid[row][col]
        return (cell.type == CellType.EMPTY or
                (cell.type == CellType.POKEMON and not cell.is_frozen))

    def find_path(self, pos1: Position, pos2: Position) -> MatchResult:
        """
        Find a valid path between two positions using BFS with turn constraints.

        Algorithm:
        1. Start from pos1
        2. Explore all 4 directions
        3. Track turns (direction changes)
        4. Stop if turns > 3
        5. Return path if pos2 is reached

        State: (row, col, direction, turns, path)
        """
        # Check if positions have matching Pokemon
        cell1 = self.grid[pos1.row][pos1.col]
        cell2 = self.grid[pos2.row][pos2.col]

        if cell1.type != CellType.POKEMON or cell2.type != CellType.POKEMON:
            return MatchResult(is_valid=False, turns=0)

        if cell1.pokemon_id != cell2.pokemon_id:
            return MatchResult(is_valid=False, turns=0)

        if cell1.is_frozen or cell2.is_frozen:
            return MatchResult(is_valid=False, turns=0)

        # Same position
        if pos1.row == pos2.row and pos1.col == pos2.col:
            return MatchResult(is_valid=False, turns=0)

        # BFS with state: (row, col, last_direction, turn_count, path)
        # last_direction: -1 means no direction yet (start), 0-3 for DIRECTIONS
        queue = deque()

        # Start exploring in all 4 directions
        for direction_idx in range(4):
            queue.append((pos1.row, pos1.col, direction_idx, 0, [Position(row=pos1.row, col=pos1.col)]))

        # Visited: (row, col, direction, turns) to avoid revisiting same state
        visited = set()
        visited.add((pos1.row, pos1.col, -1, 0))

        while queue:
            row, col, last_dir, turns, path = queue.popleft()

            # Explore current direction
            dr, dc = self.DIRECTIONS[last_dir]
            new_row, new_col = row + dr, col + dc

            # Check if we can move in this direction
            if not self.is_valid_position(new_row, new_col):
                continue

            # Check if reached destination
            if new_row == pos2.row and new_col == pos2.col:
                final_path = path + [Position(row=new_row, col=new_col)]
                return MatchResult(is_valid=True, path=final_path, turns=turns)

            # Check if cell is empty (can pass through)
            cell = self.grid[new_row][new_col]
            if cell.type != CellType.EMPTY:
                continue

            # Add current position to path
            new_path = path + [Position(row=new_row, col=new_col)]

            # Continue in same direction (no turn)
            state_same_dir = (new_row, new_col, last_dir, turns)
            if state_same_dir not in visited:
                visited.add(state_same_dir)
                queue.append((new_row, new_col, last_dir, turns, new_path))

            # Try changing direction (add a turn)
            if turns < 3:  # Max 3 turns allowed
                for new_dir in range(4):
                    if new_dir != last_dir:  # Different direction = turn
                        state_new_dir = (new_row, new_col, new_dir, turns + 1)
                        if state_new_dir not in visited:
                            visited.add(state_new_dir)
                            queue.append((new_row, new_col, new_dir, turns + 1, new_path))

        return MatchResult(is_valid=False, turns=0)

    def find_path_simple(self, pos1: Position, pos2: Position) -> MatchResult:
        """
        Simplified path finding: checks if two cells can be connected with at most 3 turns.

        This uses a more straightforward approach:
        1. Direct line (0 turns)
        2. One turn (L shape)
        3. Two turns (Z or U shape)
        4. Three turns
        """
        cell1 = self.grid[pos1.row][pos1.col]
        cell2 = self.grid[pos2.row][pos2.col]

        # Validation
        if cell1.type != CellType.POKEMON or cell2.type != CellType.POKEMON:
            return MatchResult(is_valid=False, turns=0)

        if cell1.pokemon_id != cell2.pokemon_id:
            return MatchResult(is_valid=False, turns=0)

        if cell1.is_frozen or cell2.is_frozen:
            return MatchResult(is_valid=False, turns=0)

        if pos1.row == pos2.row and pos1.col == pos2.col:
            return MatchResult(is_valid=False, turns=0)

        # Try direct paths (0 turns)
        result = self._try_direct_path(pos1, pos2)
        if result.is_valid:
            return result

        # Try 1 turn paths
        result = self._try_one_turn_path(pos1, pos2)
        if result.is_valid:
            return result

        # Try 2 turn paths
        result = self._try_two_turn_path(pos1, pos2)
        if result.is_valid:
            return result

        # Try border paths (paths that go around the edge)
        result = self._try_border_path(pos1, pos2)
        if result.is_valid:
            return result

        return MatchResult(is_valid=False, turns=0)

    def _try_direct_path(self, pos1: Position, pos2: Position) -> MatchResult:
        """Check if there's a direct horizontal or vertical path."""
        if pos1.row == pos2.row:
            # Same row, check horizontal path
            start_col = min(pos1.col, pos2.col)
            end_col = max(pos1.col, pos2.col)

            for col in range(start_col + 1, end_col):
                if self.grid[pos1.row][col].type != CellType.EMPTY:
                    return MatchResult(is_valid=False, turns=0)

            # For straight line, we only need start and end points
            path = [pos1, pos2]
            return MatchResult(is_valid=True, path=path, turns=0)

        elif pos1.col == pos2.col:
            # Same column, check vertical path
            start_row = min(pos1.row, pos2.row)
            end_row = max(pos1.row, pos2.row)

            for row in range(start_row + 1, end_row):
                if self.grid[row][pos1.col].type != CellType.EMPTY:
                    return MatchResult(is_valid=False, turns=0)

            # For straight line, we only need start and end points
            path = [pos1, pos2]
            return MatchResult(is_valid=True, path=path, turns=0)

        return MatchResult(is_valid=False, turns=0)

    def _try_one_turn_path(self, pos1: Position, pos2: Position) -> MatchResult:
        """Check for L-shaped path (1 turn)."""
        # Try corner at (pos1.row, pos2.col)
        corner1 = Position(row=pos1.row, col=pos2.col)
        if self._is_corner_valid(pos1, corner1, pos2):
            path = self._build_path(pos1, corner1, pos2)
            return MatchResult(is_valid=True, path=path, turns=1)

        # Try corner at (pos2.row, pos1.col)
        corner2 = Position(row=pos2.row, col=pos1.col)
        if self._is_corner_valid(pos1, corner2, pos2):
            path = self._build_path(pos1, corner2, pos2)
            return MatchResult(is_valid=True, path=path, turns=1)

        return MatchResult(is_valid=False, turns=0)

    def _try_two_turn_path(self, pos1: Position, pos2: Position) -> MatchResult:
        """Check for paths with 2 turns (Z or U shapes)."""
        # Try paths along each row
        for row in range(self.rows):
            mid1 = Position(row=row, col=pos1.col)
            mid2 = Position(row=row, col=pos2.col)

            # Check if mid1 and mid2 are empty (unless they are the start/end points)
            mid1_valid = (mid1.row == pos1.row and mid1.col == pos1.col) or \
                         (mid1.row == pos2.row and mid1.col == pos2.col) or \
                         self.grid[mid1.row][mid1.col].type == CellType.EMPTY

            mid2_valid = (mid2.row == pos1.row and mid2.col == pos1.col) or \
                         (mid2.row == pos2.row and mid2.col == pos2.col) or \
                         self.grid[mid2.row][mid2.col].type == CellType.EMPTY

            if (mid1_valid and mid2_valid and
                self._is_line_clear(pos1, mid1) and
                self._is_line_clear(mid1, mid2) and
                self._is_line_clear(mid2, pos2)):
                path = self._build_path_multi(pos1, mid1, mid2, pos2)
                return MatchResult(is_valid=True, path=path, turns=2)

        # Try paths along each column
        for col in range(self.cols):
            mid1 = Position(row=pos1.row, col=col)
            mid2 = Position(row=pos2.row, col=col)

            # Check if mid1 and mid2 are empty (unless they are the start/end points)
            mid1_valid = (mid1.row == pos1.row and mid1.col == pos1.col) or \
                         (mid1.row == pos2.row and mid1.col == pos2.col) or \
                         self.grid[mid1.row][mid1.col].type == CellType.EMPTY

            mid2_valid = (mid2.row == pos1.row and mid2.col == pos1.col) or \
                         (mid2.row == pos2.row and mid2.col == pos2.col) or \
                         self.grid[mid2.row][mid2.col].type == CellType.EMPTY

            if (mid1_valid and mid2_valid and
                self._is_line_clear(pos1, mid1) and
                self._is_line_clear(mid1, mid2) and
                self._is_line_clear(mid2, pos2)):
                path = self._build_path_multi(pos1, mid1, mid2, pos2)
                return MatchResult(is_valid=True, path=path, turns=2)

        return MatchResult(is_valid=False, turns=0)

    def _try_border_path(self, pos1: Position, pos2: Position) -> MatchResult:
        """
        Check for paths that go around the border of the board.
        This allows edge cells to connect via paths outside the grid.
        """
        # Try paths going around the top border (row = -1)
        if self._is_edge_clear(pos1, -1, True) and self._is_edge_clear(pos2, -1, True):
            # Both can reach top edge
            mid1 = Position(row=-1, col=pos1.col)
            mid2 = Position(row=-1, col=pos2.col)
            path = self._build_path_multi(pos1, mid1, mid2, pos2)
            return MatchResult(is_valid=True, path=path, turns=2)

        # Try paths going around the bottom border (row = rows)
        if self._is_edge_clear(pos1, self.rows, True) and self._is_edge_clear(pos2, self.rows, True):
            # Both can reach bottom edge
            mid1 = Position(row=self.rows, col=pos1.col)
            mid2 = Position(row=self.rows, col=pos2.col)
            path = self._build_path_multi(pos1, mid1, mid2, pos2)
            return MatchResult(is_valid=True, path=path, turns=2)

        # Try paths going around the left border (col = -1)
        if self._is_edge_clear(pos1, -1, False) and self._is_edge_clear(pos2, -1, False):
            # Both can reach left edge
            mid1 = Position(row=pos1.row, col=-1)
            mid2 = Position(row=pos2.row, col=-1)
            path = self._build_path_multi(pos1, mid1, mid2, pos2)
            return MatchResult(is_valid=True, path=path, turns=2)

        # Try paths going around the right border (col = cols)
        if self._is_edge_clear(pos1, self.cols, False) and self._is_edge_clear(pos2, self.cols, False):
            # Both can reach right edge
            mid1 = Position(row=pos1.row, col=self.cols)
            mid2 = Position(row=pos2.row, col=self.cols)
            path = self._build_path_multi(pos1, mid1, mid2, pos2)
            return MatchResult(is_valid=True, path=path, turns=2)

        return MatchResult(is_valid=False, turns=0)

    def _is_edge_clear(self, pos: Position, edge_value: int, is_row: bool) -> bool:
        """
        Check if a position can reach a virtual edge (outside the grid).

        Args:
            pos: The position to check from
            edge_value: The edge coordinate (-1 for top/left, rows/cols for bottom/right)
            is_row: True if checking row edge (top/bottom), False for col edge (left/right)
        """
        if is_row:
            # Checking vertical movement to top/bottom edge
            if edge_value == -1:
                # Top edge: check if all cells from row 0 to pos are clear
                for row in range(0, pos.row):
                    if self.grid[row][pos.col].type != CellType.EMPTY:
                        return False
                return True
            else:
                # Bottom edge: check if all cells from pos to last row are clear
                for row in range(pos.row + 1, self.rows):
                    if self.grid[row][pos.col].type != CellType.EMPTY:
                        return False
                return True
        else:
            # Checking horizontal movement to left/right edge
            if edge_value == -1:
                # Left edge: check if all cells from col 0 to pos are clear
                for col in range(0, pos.col):
                    if self.grid[pos.row][col].type != CellType.EMPTY:
                        return False
                return True
            else:
                # Right edge: check if all cells from pos to last col are clear
                for col in range(pos.col + 1, self.cols):
                    if self.grid[pos.row][col].type != CellType.EMPTY:
                        return False
                return True

    def _is_corner_valid(self, pos1: Position, corner: Position, pos2: Position) -> bool:
        """Check if path through corner is valid."""
        # Corner must be empty or be one of the endpoints
        if not (corner.row == pos1.row and corner.col == pos1.col) and \
           not (corner.row == pos2.row and corner.col == pos2.col):
            if self.grid[corner.row][corner.col].type != CellType.EMPTY:
                return False

        return self._is_line_clear(pos1, corner) and self._is_line_clear(corner, pos2)

    def _is_line_clear(self, start: Position, end: Position) -> bool:
        """Check if straight line between two points is clear."""
        if start.row == end.row and start.col == end.col:
            return True

        if start.row == end.row:
            # Horizontal line
            start_col = min(start.col, end.col)
            end_col = max(start.col, end.col)

            for col in range(start_col + 1, end_col):
                if self.grid[start.row][col].type != CellType.EMPTY:
                    return False
            return True

        elif start.col == end.col:
            # Vertical line
            start_row = min(start.row, end.row)
            end_row = max(start.row, end.row)

            for row in range(start_row + 1, end_row):
                if self.grid[row][start.col].type != CellType.EMPTY:
                    return False
            return True

        return False

    def _build_path(self, pos1: Position, corner: Position, pos2: Position) -> List[Position]:
        """Build path through corner - only return turning points for line drawing."""
        # For L-shaped path, we only need: start -> corner -> end
        # Check if corner is same as start or end (degenerate case)
        if (corner.row == pos1.row and corner.col == pos1.col):
            return [pos1, pos2]
        if (corner.row == pos2.row and corner.col == pos2.col):
            return [pos1, pos2]

        return [pos1, corner, pos2]

    def _build_path_multi(self, pos1: Position, mid1: Position,
                          mid2: Position, pos2: Position) -> List[Position]:
        """Build path through multiple points - only return turning points for line drawing."""
        # For Z/U-shaped path, we only need the corner points
        path = [pos1]

        # Add mid1 if it's a real turning point (not same as pos1)
        if not (mid1.row == pos1.row and mid1.col == pos1.col):
            path.append(mid1)

        # Add mid2 if it's a real turning point (not same as mid1 or pos1)
        if not (mid2.row == mid1.row and mid2.col == mid1.col) and \
           not (mid2.row == pos1.row and mid2.col == pos1.col):
            path.append(mid2)

        # Always add end point if it's different from the last point
        if not (pos2.row == path[-1].row and pos2.col == path[-1].col):
            path.append(pos2)

        return path
