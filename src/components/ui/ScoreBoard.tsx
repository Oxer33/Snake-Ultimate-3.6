/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Componente Classifica
 * ============================================
 * Mostra i migliori punteggi salvati localmente.
 */

'use client';

import React, { useEffect, useState } from 'react';
import { ScoreRecord } from '@/types/game';
import { loadScores } from '@/utils/scoreManager';

/**
 * Props del componente ScoreBoard
 */
interface ScoreBoardProps {
  onBack: () => void;
}

/**
 * Componente Classifica
 */
const ScoreBoard: React.FC<ScoreBoardProps> = ({ onBack }) => {
  const [scores, setScores] = useState<ScoreRecord[]>([]);

  // Carica i punteggi al mount
  useEffect(() => {
    setScores(loadScores());
  }, []);

  return (
    <div className="scoreboard min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      <div className="w-full max-w-2xl">
        {/* Titolo */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🏆</div>
          <h1 className="text-4xl font-bold text-white mb-2">
            Classifica
          </h1>
          <p className="text-gray-400">I migliori punteggi</p>
        </div>

        {/* Lista punteggi */}
        <div className="bg-gray-800/50 rounded-xl p-6 mb-6 border border-gray-700">
          {scores.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p className="text-lg">Nessun punteggio salvato</p>
              <p className="text-sm mt-2">Gioca una partita per entrare in classifica!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {scores.map((score, index) => (
                <div
                  key={score.id}
                  className={`
                    flex items-center justify-between p-4 rounded-lg
                    ${index === 0 ? 'bg-yellow-500/20 border border-yellow-500/50' : 
                      index === 1 ? 'bg-gray-400/20 border border-gray-400/50' :
                      index === 2 ? 'bg-orange-600/20 border border-orange-600/50' :
                      'bg-gray-900/50 border border-gray-700'}
                  `}
                >
                  {/* Posizione */}
                  <div className="flex items-center gap-4">
                    <span className={`
                      text-2xl font-bold w-8 text-center
                      ${index === 0 ? 'text-yellow-400' : 
                        index === 1 ? 'text-gray-300' :
                        index === 2 ? 'text-orange-500' :
                        'text-gray-500'}
                    `}>
                      {index + 1}
                    </span>
                    
                    {/* Info */}
                    <div>
                      <p className="font-semibold text-white">{score.name || 'Giocatore'}</p>
                      <p className="text-xs text-gray-400">
                        {score.mode} • {score.difficulty} • Liv. {score.level}
                      </p>
                    </div>
                  </div>
                  
                  {/* Punteggio */}
                  <div className="text-right">
                    <p className="text-xl font-bold text-snake-primary">
                      {score.score.toLocaleString('it-IT')}
                    </p>
                    <p className="text-xs text-gray-500">
                      {new Date(score.date).toLocaleDateString('it-IT')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Pulsante torna indietro */}
        <button
          type="button"
          onClick={onBack}
          className="
            w-full py-4 rounded-xl text-lg font-bold
            bg-gradient-to-r from-snake-primary to-snake-secondary
            text-gray-900
            transition-all duration-300
            hover:scale-105 hover:shadow-lg hover:shadow-snake-primary/30
            active:scale-95
          "
        >
          ← Torna al Menu
        </button>
      </div>
    </div>
  );
};

export default ScoreBoard;
