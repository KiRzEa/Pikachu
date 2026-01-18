/**
 * Pokemon sprite configuration
 *
 * Uses PokeAPI sprites from GitHub CDN
 * Source: https://github.com/PokeAPI/sprites
 */

export const POKEMON_SPRITES = {
  1: {
    name: 'Pikachu',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'
  },
  2: {
    name: 'Bulbasaur',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'
  },
  3: {
    name: 'Charmander',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png'
  },
  4: {
    name: 'Squirtle',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png'
  },
  5: {
    name: 'Eevee',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png'
  },
  6: {
    name: 'Jigglypuff',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/39.png'
  },
  7: {
    name: 'Meowth',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/52.png'
  },
  8: {
    name: 'Psyduck',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/54.png'
  },
  9: {
    name: 'Snorlax',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/143.png'
  },
  10: {
    name: 'Mew',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/151.png'
  },
  11: {
    name: 'Togepi',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/175.png'
  },
  12: {
    name: 'Chikorita',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/152.png'
  },
  13: {
    name: 'Totodile',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/158.png'
  },
  14: {
    name: 'Cyndaquil',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/155.png'
  },
  15: {
    name: 'Mudkip',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/258.png'
  },
  16: {
    name: 'Torchic',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/255.png'
  },
  17: {
    name: 'Treecko',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/252.png'
  },
  18: {
    name: 'Piplup',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/393.png'
  },
  19: {
    name: 'Turtwig',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/387.png'
  },
  20: {
    name: 'Chimchar',
    url: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/390.png'
  }
};

/**
 * Get sprite URL for a Pokemon ID
 */
export const getPokemonSprite = (pokemonId) => {
  return POKEMON_SPRITES[pokemonId]?.url || '';
};

/**
 * Get Pokemon name
 */
export const getPokemonName = (pokemonId) => {
  return POKEMON_SPRITES[pokemonId]?.name || `Pokemon ${pokemonId}`;
};

/**
 * Preload all Pokemon sprites for better performance
 */
export const preloadPokemonSprites = () => {
  return Promise.all(
    Object.values(POKEMON_SPRITES).map(pokemon => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(pokemon.name);
        img.onerror = reject;
        img.src = pokemon.url;
      });
    })
  );
};
