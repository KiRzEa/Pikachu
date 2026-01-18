"""
Pokemon data configuration for the game.

Using PokeAPI sprite URLs for Pokemon images.
Source: https://github.com/PokeAPI/sprites
"""

# 20 popular Pokemon with their PokeAPI IDs
POKEMON_LIST = [
    {"id": 1, "name": "Pikachu", "pokedex_id": 25},
    {"id": 2, "name": "Bulbasaur", "pokedex_id": 1},
    {"id": 3, "name": "Charmander", "pokedex_id": 4},
    {"id": 4, "name": "Squirtle", "pokedex_id": 7},
    {"id": 5, "name": "Eevee", "pokedex_id": 133},
    {"id": 6, "name": "Jigglypuff", "pokedex_id": 39},
    {"id": 7, "name": "Meowth", "pokedex_id": 52},
    {"id": 8, "name": "Psyduck", "pokedex_id": 54},
    {"id": 9, "name": "Snorlax", "pokedex_id": 143},
    {"id": 10, "name": "Mew", "pokedex_id": 151},
    {"id": 11, "name": "Togepi", "pokedex_id": 175},
    {"id": 12, "name": "Chikorita", "pokedex_id": 152},
    {"id": 13, "name": "Totodile", "pokedex_id": 158},
    {"id": 14, "name": "Cyndaquil", "pokedex_id": 155},
    {"id": 15, "name": "Mudkip", "pokedex_id": 258},
    {"id": 16, "name": "Torchic", "pokedex_id": 255},
    {"id": 17, "name": "Treecko", "pokedex_id": 252},
    {"id": 18, "name": "Piplup", "pokedex_id": 393},
    {"id": 19, "name": "Turtwig", "pokedex_id": 387},
    {"id": 20, "name": "Chimchar", "pokedex_id": 390},
]


def get_pokemon_sprite_url(pokemon_id: int) -> str:
    """
    Get the sprite URL for a Pokemon from PokeAPI.

    Args:
        pokemon_id: Game Pokemon ID (1-20)

    Returns:
        URL to Pokemon sprite image
    """
    pokemon = next((p for p in POKEMON_LIST if p["id"] == pokemon_id), None)
    if not pokemon:
        return ""

    pokedex_id = pokemon["pokedex_id"]

    # PokeAPI sprites CDN
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokedex_id}.png"


def get_pokemon_name(pokemon_id: int) -> str:
    """Get the name of a Pokemon by game ID."""
    pokemon = next((p for p in POKEMON_LIST if p["id"] == pokemon_id), None)
    return pokemon["name"] if pokemon else f"Pokemon {pokemon_id}"


def get_all_pokemon_data():
    """Get all Pokemon data with sprite URLs."""
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "pokedex_id": p["pokedex_id"],
            "sprite_url": get_pokemon_sprite_url(p["id"])
        }
        for p in POKEMON_LIST
    ]
