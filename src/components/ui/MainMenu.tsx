/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Menu Principale
 * ============================================
 * Schermata iniziale del gioco con:
 * - Logo animato
 * - Selezione modalità di gioco
 * - Pulsanti impostazioni e classifica
 * - Effetti visivi accattivanti
 */

'use client';

import React, { useState } from 'react';
import { GameMode } from '@/types/game';

/**
 * Props del componente MainMenu
 */
interface MainMenuProps {
  onStart: (mode: GameMode) => void;
  onSettings: () => void;
  onScores: () => void;
}

/**
 * Descrizioni delle modalità di gioco
 */
const GAME_MODES: { id: GameMode; name: string; description: string; icon: string }[] = [
  {
    id: 'classic',
    name: 'Classico',
    description: 'Il tradizionale gioco Snake. Mangia, cresci, non morire!',
    icon: '🐍',
  },
  {
    id: 'speed',
    name: 'Velocità',
    description: 'Sempre più veloce! Riuscirai a tenere il passo?',
    icon: '⚡',
  },
  {
    id: 'obstacles',
    name: 'Ostacoli',
    description: 'Attenzione ai muri! Naviga attraverso il percorso.',
    icon: '🧱',
  },
  {
    id: 'zen',
    name: 'Zen',
    description: 'Nessuna fretta, nessun game over. Rilassati e gioca.',
    icon: '🧘',
  },
  {
    id: 'challenge',
    name: 'Sfida',
    description: 'Per i più coraggiosi. Difficoltà estrema!',
    icon: '🏆',
  },
];

/**
 * Componente Menu Principale
 */
const MainMenu: React.FC<MainMenuProps> = ({
  onStart,
  onSettings,
  onScores,
}) => {
  const [selectedMode, setSelectedMode] = useState<GameMode>('classic');

  return (
    <div className="main-menu min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      {/* Contenitore principale */}
      <div className="w-full max-w-2xl">
        
        {/* Logo e Titolo */}
        <div className="text-center mb-12 animate-fade-in">
          {/* Icona serpente animata */}
          <div className="text-8xl mb-4 animate-float">
            🐍
          </div>
          
          {/* Titolo */}
          <h1 className="text-5xl md:text-6xl font-bold mb-2">
            <span className="bg-gradient-to-r from-snake-primary via-snake-accent to-snake-primary bg-clip-text text-transparent">
              SNAKE
            </span>
          </h1>
          <h2 className="text-2xl md:text-3xl font-light text-gray-400">
            ULTIMATE <span className="text-snake-accent">3.6</span>
          </h2>
          
          {/* Sottotitolo */}
          <p className="text-gray-500 mt-4 text-sm">
            Il gioco Snake più bello mai creato
          </p>
        </div>
        
        {/* Selezione Modalità */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-300 mb-4 text-center">
            Scegli la modalità di gioco
          </h3>
          
          {/* Griglia modalità - Bento Grid Style */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {GAME_MODES.map((mode) => (
              <button
                key={mode.id}
                type="button"
                onClick={() => setSelectedMode(mode.id)}
                className={`
                  relative p-4 rounded-xl border-2 transition-all duration-300
                  flex flex-col items-center gap-2
                  ${selectedMode === mode.id
                    ? 'border-snake-primary bg-snake-primary/10 shadow-lg shadow-snake-primary/20'
                    : 'border-gray-700 bg-gray-800/50 hover:border-gray-600 hover:bg-gray-800'
                  }
                `}
              >
                {/* Icona */}
                <span className="text-3xl">{mode.icon}</span>
                
                {/* Nome */}
                <span className="font-semibold text-white">{mode.name}</span>
                
                {/* Descrizione (visibile solo su desktop) */}
                <span className="text-xs text-gray-400 text-center hidden md:block">
                  {mode.description}
                </span>
                
                {/* Indicatore selezione */}
                {selectedMode === mode.id && (
                  <div className="absolute top-2 right-2 w-3 h-3 bg-snake-primary rounded-full animate-pulse" />
                )}
              </button>
            ))}
          </div>
        </div>
        
        {/* Pulsante Gioca */}
        <button
          type="button"
          onClick={() => onStart(selectedMode)}
          className="
            w-full py-4 rounded-xl text-xl font-bold
            bg-gradient-to-r from-snake-primary to-snake-secondary
            text-gray-900
            transform transition-all duration-300
            hover:scale-105 hover:shadow-lg hover:shadow-snake-primary/30
            active:scale-95
            focus:outline-none focus:ring-2 focus:ring-snake-primary focus:ring-offset-2 focus:ring-offset-gray-900
          "
        >
          🎮 GIOCA ORA
        </button>
        
        {/* Pulsanti secondari */}
        <div className="flex gap-4 mt-6">
          <button
            type="button"
            onClick={onScores}
            className="
              flex-1 py-3 rounded-xl font-semibold
              bg-gray-800 text-gray-300
              border border-gray-700
              transition-all duration-300
              hover:bg-gray-700 hover:text-white
              active:scale-95
            "
          >
            🏆 Classifica
          </button>
          <button
            type="button"
            onClick={onSettings}
            className="
              flex-1 py-3 rounded-xl font-semibold
              bg-gray-800 text-gray-300
              border border-gray-700
              transition-all duration-300
              hover:bg-gray-700 hover:text-white
              active:scale-95
            "
          >
            ⚙️ Impostazioni
          </button>
        </div>
        
        {/* Footer */}
        <div className="text-center mt-8 text-gray-600 text-xs">
          <p>Usa le frecce direzionali o WASD per muoverti</p>
          <p className="mt-1">Premi SPAZIO per mettere in pausa</p>
        </div>
      </div>
    </div>
  );
};

export default MainMenu;
