import React from 'react';
import './GameInfo.css';

function GameInfo({ score, lives, level, timeRemaining }) {
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="game-info">
      <div className="info-item">
        <span className="label">Level</span>
        <span className="value">{level}</span>
      </div>
      <div className="info-item">
        <span className="label">Score</span>
        <span className="value">{score}</span>
      </div>
      <div className="info-item">
        <span className="label">Lives</span>
        <span className="value">{'❤️'.repeat(lives)}</span>
      </div>
      <div className="info-item">
        <span className="label">Time</span>
        <span className="value">{formatTime(timeRemaining)}</span>
      </div>
    </div>
  );
}

export default GameInfo;
