/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Schermata Game Over
 * ============================================
 * Schermata che appare quando il giocatore perde.
 * Mostra:
 * - Punteggio finale
 * - Nuovo record (se raggiunto)
 * - Statistiche della partita
 * - Pulsanti per rigiocare o tornare al menu
 */

'use client';

import React, { useEffect, useState } from 'react';

/**
 * Props del componente GameOver
 */
interface GameOverProps {
  score: number;
  highScore: number;
  level: number;
  foodEaten: number;
  onRestart: () => void;
  onMenu: () => void;
}

/**
 * Componente Game Over
 */
const GameOver: React.FC<GameOverProps> = ({
  score,
  highScore,
  level,
  foodEaten,
  onRestart,
  onMenu,
}) => {
  const [isNewRecord, setIsNewRecord] = useState(false);
  const [showContent, setShowContent] = useState(false);

  // Controlla se è un nuovo record
  useEffect(() => {
    if (score > highScore) {
      setIsNewRecord(true);
    }
    
    // Animazione di entrata
    const timer = setTimeout(() => setShowContent(true), 100);
    return () => clearTimeout(timer);
  }, [score, highScore]);

  return (
    <div 
      className="game-over-overlay fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{
        background: 'rgba(1, 4, 9, 0.95)',
        backdropFilter: 'blur(10px)',
      }}
      role="dialog"
      aria-modal="true"
      aria-label="Game Over"
    >
      <div 
        className={`
          game-over-content w-full max-w-md
          bg-gray-900 rounded-2xl p-8
          border border-gray-700
          shadow-2xl
          transition-all duration-500
          ${showContent ? 'opacity-100 scale-100' : 'opacity-0 scale-95'}
        `}
      >
        {/* Titolo */}
        <div className="text-center mb-6">
          <div className="text-6xl mb-4">💀</div>
          <h2 className="text-3xl font-bold text-white mb-2">
            GAME OVER
          </h2>
          {isNewRecord && (
            <div className="inline-block px-4 py-2 bg-snake-warning/20 border border-snake-warning rounded-full">
              <span className="text-snake-warning font-bold animate-pulse">
                🏆 NUOVO RECORD! 🏆
              </span>
            </div>
          )}
        </div>
        
        {/* Statistiche */}
        <div className="bg-gray-800/50 rounded-xl p-4 mb-6">
          <div className="grid grid-cols-2 gap-4">
            {/* Punteggio */}
            <div className="text-center">
              <p className="text-xs text-gray-400 uppercase">Punteggio</p>
              <p className="text-2xl font-bold text-snake-primary">
                {score.toLocaleString('it-IT')}
              </p>
            </div>
            
            {/* Livello */}
            <div className="text-center">
              <p className="text-xs text-gray-400 uppercase">Livello</p>
              <p className="text-2xl font-bold text-snake-accent">
                {level}
              </p>
            </div>
            
            {/* Mele mangiate */}
            <div className="text-center">
              <p className="text-xs text-gray-400 uppercase">Mele</p>
              <p className="text-2xl font-bold text-snake-danger">
                🍎 {foodEaten}
              </p>
            </div>
            
            {/* Record */}
            <div className="text-center">
              <p className="text-xs text-gray-400 uppercase">Record</p>
              <p className="text-2xl font-bold text-snake-warning">
                {Math.max(score, highScore).toLocaleString('it-IT')}
              </p>
            </div>
          </div>
        </div>
        
        {/* Pulsanti */}
        <div className="space-y-3">
          {/* Rigoca */}
          <button
            type="button"
            onClick={onRestart}
            className="
              w-full py-4 rounded-xl text-lg font-bold
              bg-gradient-to-r from-snake-primary to-snake-secondary
              text-gray-900
              transition-all duration-300
              hover:scale-105 hover:shadow-lg hover:shadow-snake-primary/30
              active:scale-95
            "
          >
            🔄 GIOCA ANCORA
          </button>
          
          {/* Torna al menu */}
          <button
            type="button"
            onClick={onMenu}
            className="
              w-full py-3 rounded-xl font-semibold
              bg-gray-800 text-gray-300
              border border-gray-700
              transition-all duration-300
              hover:bg-gray-700 hover:text-white
              active:scale-95
            "
          >
            🏠 Menu Principale
          </button>
        </div>
        
        {/* Suggerimento */}
        <p className="text-center text-gray-500 text-xs mt-6">
          Premi INVIO per rigiocare • ESC per il menu
        </p>
      </div>
    </div>
  );
};

export default GameOver;
