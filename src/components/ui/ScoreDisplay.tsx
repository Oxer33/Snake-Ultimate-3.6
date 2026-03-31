/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Display Punteggio
 * ============================================
 * Componente che mostra il punteggio corrente,
 * il punteggio più alto e il livello attuale.
 */

'use client';

import React from 'react';

/**
 * Props del componente ScoreDisplay
 */
interface ScoreDisplayProps {
  score: number;
  highScore: number;
  level: number;
  foodEaten: number;
}

/**
 * Componente display punteggio
 */
const ScoreDisplay: React.FC<ScoreDisplayProps> = ({
  score,
  highScore,
  level,
  foodEaten,
}) => {
  return (
    <div className="score-container flex justify-between items-center gap-4 mb-4 p-4 rounded-xl bg-gray-900/50 backdrop-blur-sm border border-gray-800">
      {/* Punteggio corrente */}
      <div className="score-item text-center">
        <p className="text-xs text-gray-400 uppercase tracking-wider">Punteggio</p>
        <p className="score-display text-2xl font-bold text-snake-primary">
          {score.toLocaleString('it-IT')}
        </p>
      </div>
      
      {/* Separatore */}
      <div className="h-10 w-px bg-gray-700" />
      
      {/* Punteggio più alto */}
      <div className="score-item text-center">
        <p className="text-xs text-gray-400 uppercase tracking-wider">Record</p>
        <p className="text-2xl font-bold text-snake-accent">
          {highScore.toLocaleString('it-IT')}
        </p>
      </div>
      
      {/* Separatore */}
      <div className="h-10 w-px bg-gray-700" />
      
      {/* Livello */}
      <div className="score-item text-center">
        <p className="text-xs text-gray-400 uppercase tracking-wider">Livello</p>
        <p className="text-2xl font-bold text-snake-warning">
          {level}
        </p>
      </div>
      
      {/* Separatore */}
      <div className="h-10 w-px bg-gray-700" />
      
      {/* Cibo mangiato */}
      <div className="score-item text-center">
        <p className="text-xs text-gray-400 uppercase tracking-wider">Mele</p>
        <p className="text-2xl font-bold text-snake-danger">
          🍎 {foodEaten}
        </p>
      </div>
    </div>
  );
};

export default ScoreDisplay;
