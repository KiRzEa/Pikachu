import React from 'react';
import './Cell.css';
import { getPokemonSprite, getPokemonName } from '../services/pokemonSprites';

function Cell({ cell, row, col, isSelected, isHinted, onClick, disabled }) {
  const isEmpty = cell.type === 'empty';
  const isFrozen = cell.is_frozen;

  const getClassName = () => {
    const classes = ['cell'];

    if (isEmpty) classes.push('empty');
    if (isSelected) classes.push('selected');
    if (isHinted) classes.push('hinted');
    if (isFrozen) classes.push('frozen');
    if (disabled && !isEmpty) classes.push('disabled');

    return classes.join(' ');
  };

  return (
    <div className={getClassName()} onClick={onClick}>
      {!isEmpty && (
        <>
          <img
            src={getPokemonSprite(cell.pokemon_id)}
            alt={getPokemonName(cell.pokemon_id)}
            className="pokemon-sprite"
            draggable="false"
          />
          {isFrozen && <div className="ice-overlay">❄️</div>}
        </>
      )}
    </div>
  );
}

export default Cell;
