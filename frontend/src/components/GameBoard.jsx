import React, { useState } from 'react';
import Cell from './Cell';
import MatchLine from './MatchLine';
import './GameBoard.css';

function GameBoard({
  grid,
  rows,
  cols,
  selectedCell,
  hintCells,
  onCellClick,
  disabled,
  matchPath,
  onMatchLineComplete,
}) {
  const isCellSelected = (row, col) => {
    return selectedCell && selectedCell.row === row && selectedCell.col === col;
  };

  const isCellHinted = (row, col) => {
    if (!hintCells) return false;
    return (
      (hintCells.pos1.row === row && hintCells.pos1.col === col) ||
      (hintCells.pos2.row === row && hintCells.pos2.col === col)
    );
  };

  return (
    <div className="game-board-container">
      <div className="game-board" style={{ gridTemplateColumns: `repeat(${cols}, 1fr)` }}>
        {grid.map((row, rowIndex) =>
          row.map((cell, colIndex) => (
            <Cell
              key={`${rowIndex}-${colIndex}`}
              cell={cell}
              row={rowIndex}
              col={colIndex}
              isSelected={isCellSelected(rowIndex, colIndex)}
              isHinted={isCellHinted(rowIndex, colIndex)}
              onClick={() => !disabled && onCellClick(rowIndex, colIndex)}
              disabled={disabled}
            />
          ))
        )}
      </div>
      {matchPath && (
        <MatchLine
          start={matchPath[0]}
          end={matchPath[matchPath.length - 1]}
          path={matchPath}
          onComplete={onMatchLineComplete}
          rows={rows}
          cols={cols}
        />
      )}
    </div>
  );
}

export default GameBoard;
