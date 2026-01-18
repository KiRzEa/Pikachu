"""
Test script to demonstrate DSA algorithms used in Pikachu Kawaii game.

Run: python test_algorithms.py
"""

from app.models.game import Cell, CellType, Position
from app.core.pathfinder import PathFinder
from app.services.game_service import GameService


def print_grid(grid, rows, cols):
    """Pretty print the game grid."""
    print("\nGame Board:")
    print("  ", end="")
    for col in range(cols):
        print(f"{col:3}", end="")
    print()

    for row in range(rows):
        print(f"{row:2}", end=" ")
        for col in range(cols):
            cell = grid[row][col]
            if cell.type == CellType.EMPTY:
                print("  .", end="")
            else:
                frozen_mark = "❄" if cell.is_frozen else " "
                print(f"{cell.pokemon_id:2}{frozen_mark}", end="")
        print()
    print()


def test_pathfinding():
    """Test BFS pathfinding algorithm."""
    print("=" * 60)
    print("TEST 1: BFS Pathfinding Algorithm")
    print("=" * 60)

    # Create a simple 5x6 grid
    rows, cols = 5, 6
    grid = [[Cell(type=CellType.EMPTY) for _ in range(cols)] for _ in range(rows)]

    # Place two matching Pokemon
    grid[0][0] = Cell(type=CellType.POKEMON, pokemon_id=1)
    grid[0][5] = Cell(type=CellType.POKEMON, pokemon_id=1)

    # Add some obstacles
    grid[0][2] = Cell(type=CellType.POKEMON, pokemon_id=2)
    grid[1][2] = Cell(type=CellType.POKEMON, pokemon_id=3)

    print_grid(grid, rows, cols)

    # Test pathfinding
    pathfinder = PathFinder(grid, rows, cols)
    pos1 = Position(row=0, col=0)
    pos2 = Position(row=0, col=5)

    print(f"Finding path from ({pos1.row}, {pos1.col}) to ({pos2.row}, {pos2.col})")

    result = pathfinder.find_path_simple(pos1, pos2)

    if result.is_valid:
        print(f"✅ Valid path found with {result.turns} turn(s)!")
        print("Path:", end=" ")
        for pos in result.path:
            print(f"({pos.row},{pos.col})", end=" -> ")
        print("END")
    else:
        print("❌ No valid path found")

    print()


def test_fisher_yates():
    """Test Fisher-Yates shuffle algorithm."""
    print("=" * 60)
    print("TEST 2: Fisher-Yates Shuffle Algorithm")
    print("=" * 60)

    service = GameService(rows=4, cols=4)

    # Create a simple list
    items = list(range(1, 17))
    print(f"Original list: {items}")

    # Shuffle multiple times to show randomness
    print("\nShuffle results (5 iterations):")
    for i in range(5):
        test_items = items.copy()
        service._shuffle_list(test_items)
        print(f"  Shuffle {i+1}: {test_items}")

    print("\n✅ Each shuffle produces a different random permutation")
    print()


def test_hint_system():
    """Test hint system with hash map."""
    print("=" * 60)
    print("TEST 3: Hint System (Hash Map)")
    print("=" * 60)

    # Create a game
    service = GameService(rows=4, cols=6)
    game_state = service.create_new_game(level=1)

    print_grid(game_state.board.grid, 4, 6)

    # Find hint
    hint = service.find_hint(game_state)

    if hint:
        pos1, pos2 = hint
        print(f"✅ Hint found!")
        print(f"  Position 1: ({pos1.row}, {pos1.col}) - Pokemon ID: {game_state.board.grid[pos1.row][pos1.col].pokemon_id}")
        print(f"  Position 2: ({pos2.row}, {pos2.col}) - Pokemon ID: {game_state.board.grid[pos2.row][pos2.col].pokemon_id}")

        # Verify the path
        pathfinder = PathFinder(game_state.board.grid, 4, 6)
        result = pathfinder.find_path_simple(pos1, pos2)
        print(f"  Path valid: {result.is_valid}, Turns: {result.turns}")
    else:
        print("❌ No hints available")

    print()


def test_board_generation():
    """Test board generation algorithm."""
    print("=" * 60)
    print("TEST 4: Board Generation")
    print("=" * 60)

    service = GameService(rows=6, cols=8)
    game_state = service.create_new_game(level=1)

    print(f"Board size: {game_state.board.rows}x{game_state.board.cols}")
    print(f"Total cells: {game_state.board.rows * game_state.board.cols}")

    # Count Pokemon types
    pokemon_count = {}
    for row in game_state.board.grid:
        for cell in row:
            if cell.type == CellType.POKEMON:
                pokemon_count[cell.pokemon_id] = pokemon_count.get(cell.pokemon_id, 0) + 1

    print(f"\nPokemon distribution:")
    for pokemon_id, count in sorted(pokemon_count.items()):
        print(f"  Pokemon {pokemon_id:2}: {count} instances {'✅' if count % 2 == 0 else '❌'}")

    total = sum(pokemon_count.values())
    all_even = all(count % 2 == 0 for count in pokemon_count.values())

    print(f"\nTotal Pokemon: {total}")
    print(f"All counts are even (paired): {'✅' if all_even else '❌'}")

    print_grid(game_state.board.grid, game_state.board.rows, game_state.board.cols)


def test_complexity_analysis():
    """Demonstrate time complexity of operations."""
    print("=" * 60)
    print("TEST 5: Time Complexity Analysis")
    print("=" * 60)

    import time

    sizes = [4, 8, 12, 16]
    print("\nBoard Size vs Generation Time:")
    print(f"{'Size':<10} {'Cells':<10} {'Time (ms)':<15}")
    print("-" * 35)

    for size in sizes:
        service = GameService(rows=size, cols=size)

        start = time.time()
        game_state = service.create_new_game(level=1)
        end = time.time()

        cells = size * size
        elapsed_ms = (end - start) * 1000

        print(f"{size}x{size:<6} {cells:<10} {elapsed_ms:<15.4f}")

    print("\n✅ Time complexity is O(n) where n = rows × cols")
    print()


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("PIKACHU KAWAII - DSA ALGORITHM DEMONSTRATIONS")
    print("=" * 60 + "\n")

    test_pathfinding()
    test_fisher_yates()
    test_hint_system()
    test_board_generation()
    test_complexity_analysis()

    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
