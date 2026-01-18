import React, { useEffect, useState, useRef } from 'react';
import './MatchLine.css';

function MatchLine({ start, end, path, onComplete, rows = 10, cols = 14 }) {
  const [isVisible, setIsVisible] = useState(true);
  const svgRef = useRef(null);

  useEffect(() => {
    // Start fade out animation after a short delay
    const fadeTimer = setTimeout(() => {
      setIsVisible(false);
    }, 600);

    // Remove the line completely after animation
    const removeTimer = setTimeout(() => {
      onComplete();
    }, 1400); // 600ms delay + 800ms fade animation

    return () => {
      clearTimeout(fadeTimer);
      clearTimeout(removeTimer);
    };
  }, [onComplete]);

  if (!start || !end || !path || path.length < 2) return null;

  // Use a coordinate system based on grid cells, not pixels
  // We'll use a normalized grid where each cell is 1 unit wide/tall
  // Gap and padding are calculated as fractions of cell size
  const gapRatio = 4 / 100; // gap / cellSize from CSS (4px gap)
  const paddingRatio = 12 / 100; // boardPadding / cellSize from CSS (12px padding)

  // Calculate the actual position of each cell center in grid units
  const getCellCenter = (row, col) => {
    // Handle virtual border cells (negative or beyond grid)
    // These represent paths that go around the edge of the board
    let actualRow = row;
    let actualCol = col;

    // Clamp to just outside the visible grid for border paths
    if (row < 0) actualRow = -0.5; // Just above top edge
    if (row >= rows) actualRow = rows - 0.5; // Just below bottom edge
    if (col < 0) actualCol = -0.5; // Just left of left edge
    if (col >= cols) actualCol = cols - 0.5; // Just right of right edge

    // Each cell plus gap is 1 + gapRatio units
    // Start position includes padding
    const x = paddingRatio + actualCol * (1 + gapRatio) + 0.5; // 0.5 = center of 1-unit cell
    const y = paddingRatio + actualRow * (1 + gapRatio) + 0.5;
    return { x, y };
  };

  // Generate SVG path from the path array
  const generatePath = () => {
    if (path.length < 2) return '';

    const firstPoint = getCellCenter(path[0].row, path[0].col);
    let pathString = `M ${firstPoint.x} ${firstPoint.y}`;

    for (let i = 1; i < path.length; i++) {
      const point = getCellCenter(path[i].row, path[i].col);
      pathString += ` L ${point.x} ${point.y}`;
    }

    return pathString;
  };

  const pathData = generatePath();

  // Calculate viewBox to cover the entire grid including padding
  // In our normalized coordinate system where each cell is 1 unit
  const viewBoxWidth = cols * (1 + gapRatio) + paddingRatio * 2;
  const viewBoxHeight = rows * (1 + gapRatio) + paddingRatio * 2;

  return (
    <div className={`match-line-container ${!isVisible ? 'fade-out' : ''}`}>
      <svg
        ref={svgRef}
        className="match-line-svg"
        viewBox={`0 0 ${viewBoxWidth} ${viewBoxHeight}`}
        preserveAspectRatio="none"
      >
        {/* Simple thin line to show the connection path */}
        <path
          d={pathData}
          fill="none"
          stroke="#00FF00"
          strokeWidth="0.08"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Small circles at each turn point */}
        {path.map((point, index) => {
          const center = getCellCenter(point.row, point.col);
          return (
            <circle
              key={index}
              cx={center.x}
              cy={center.y}
              r="0.08"
              fill="#00FF00"
            />
          );
        })}
      </svg>
    </div>
  );
}

export default MatchLine;
