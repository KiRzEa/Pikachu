import React, { useState, useEffect } from 'react';
import GameBoard from './components/GameBoard';
import GameInfo from './components/GameInfo';
import { gameAPI } from './services/api';
import { preloadPokemonSprites } from './services/pokemonSprites';
import './App.css';

function App() {
  const [gameState, setGameState] = useState(null);
  const [gameId, setGameId] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [hintCells, setHintCells] = useState(null);
  const [spritesLoaded, setSpritesLoaded] = useState(false);
  const [matchPath, setMatchPath] = useState(null);

  useEffect(() => {
    // Preload Pokemon sprites for better performance
    setMessage('Loading Pokemon sprites...');
    preloadPokemonSprites()
      .then(() => {
        setSpritesLoaded(true);
        startNewGame();
      })
      .catch((error) => {
        console.error('Failed to preload sprites:', error);
        setSpritesLoaded(true);
        startNewGame();
      });
  }, []);

  const startNewGame = async (level = 1) => {
    setLoading(true);
    try {
      const response = await gameAPI.createGame(level);
      setGameState(response.game_state);
      setGameId(response.game_id);
      setSelectedCell(null);
      setHintCells(null);
      setMessage('Game started! Match the Pokemon!');
    } catch (error) {
      setMessage('Error starting game: ' + error.message);
      console.error('Error:', error);
    }
    setLoading(false);
  };

  const handleCellClick = async (row, col) => {
    if (!gameState || gameState.game_over || gameState.victory) return;

    const cell = gameState.board.grid[row][col];
    if (cell.type === 'empty' || cell.is_frozen) return;

    const newPos = { row, col };

    if (!selectedCell) {
      // First selection
      setSelectedCell(newPos);
      setMessage('Selected! Now select the matching Pokemon.');
    } else {
      // Second selection - try to make a move
      if (selectedCell.row === row && selectedCell.col === col) {
        // Clicked same cell - deselect
        setSelectedCell(null);
        setMessage('Selection cleared.');
        return;
      }

      setLoading(true);
      try {
        const result = await gameAPI.makeMove(gameId, selectedCell, newPos);

        if (result.success) {
          // Show the match path animation
          setMatchPath(result.path);
          setMessage(`Great! Matched in ${result.turns} turn(s)!`);

          // Update game state after a short delay to let the animation show
          setTimeout(() => {
            setGameState(result.game_state);
            if (result.game_state.victory) {
              setMessage('Congratulations! You won!');
            }
          }, 300);
        } else {
          setMessage('No valid path between these Pokemon. Try again!');
        }
      } catch (error) {
        setMessage('Error making move: ' + error.message);
      }

      setSelectedCell(null);
      setHintCells(null);
      setLoading(false);
    }
  };

  const handleHint = async () => {
    if (!gameState || loading) return;

    setLoading(true);
    try {
      const result = await gameAPI.getHint(gameId);

      if (result.hint_available) {
        setHintCells({ pos1: result.pos1, pos2: result.pos2 });
        setMessage('Hint shown! Look for the highlighted cells.');

        // Clear hint after 3 seconds
        setTimeout(() => {
          setHintCells(null);
        }, 3000);
      } else {
        setMessage('No hints available - board is being shuffled!');
        // Refresh game state
        const game = await gameAPI.getGame(gameId);
        setGameState(game);
      }
    } catch (error) {
      setMessage('Error getting hint: ' + error.message);
    }
    setLoading(false);
  };

  const handleShuffle = async () => {
    if (!gameState || loading) return;

    setLoading(true);
    try {
      const result = await gameAPI.shuffleBoard(gameId);
      setGameState(result.game_state);
      setMessage(`Board shuffled! Lives remaining: ${result.lives_remaining}`);
      setSelectedCell(null);
    } catch (error) {
      setMessage('Error shuffling: ' + error.message);
    }
    setLoading(false);
  };

  if (!gameState || !spritesLoaded) {
    return <div className="loading">
      <div>Loading Pokemon...</div>
      <div style={{ fontSize: '4rem', marginTop: '20px' }}>⚡</div>
    </div>;
  }

  return (
    <div className="app">
      <h1>Pikachu Kawaii Classic</h1>

      <GameInfo
        score={gameState.board.score}
        lives={gameState.board.lives}
        level={gameState.board.level}
        timeRemaining={gameState.board.time_remaining}
      />

      <div className="message">{message}</div>

      <GameBoard
        grid={gameState.board.grid}
        rows={gameState.board.rows}
        cols={gameState.board.cols}
        selectedCell={selectedCell}
        hintCells={hintCells}
        onCellClick={handleCellClick}
        disabled={loading || gameState.game_over || gameState.victory}
        matchPath={matchPath}
        onMatchLineComplete={() => setMatchPath(null)}
      />

      <div className="controls">
        <button onClick={() => startNewGame()} disabled={loading}>
          New Game
        </button>
        <button onClick={handleHint} disabled={loading || gameState.game_over}>
          Hint
        </button>
        <button onClick={handleShuffle} disabled={loading || gameState.game_over}>
          Shuffle (-1 Life)
        </button>
      </div>

      {gameState.game_over && (
        <div className="game-over">
          <h2>Game Over!</h2>
          <p>Final Score: {gameState.board.score}</p>
          <button onClick={() => startNewGame()}>Play Again</button>
        </div>
      )}

      {gameState.victory && (
        <div className="victory">
          <h2>Victory!</h2>
          <p>Score: {gameState.board.score}</p>
          <button onClick={() => startNewGame(gameState.board.level + 1)}>
            Next Level
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
