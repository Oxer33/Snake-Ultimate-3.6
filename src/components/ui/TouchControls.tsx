/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Controlli Touch
 * ============================================
 * Componente per i controlli touch su dispositivi mobili.
 * Implementa un D-pad virtuale per controllare la direzione
 * del serpente.
 * 
 * Caratteristiche:
 * - D-pad virtuale responsivo
 * - Feedback aptico (vibrazione)
 * - Supporto gesture swipe
 * - Design ergonomico
 */

'use client';

import React, { useCallback, useRef } from 'react';
import { Direction } from '@/types/game';

/**
 * Props del componente TouchControls
 */
interface TouchControlsProps {
  onDirectionChange: (direction: Direction) => void;
  disabled?: boolean;
}

/**
 * Componente controlli touch per mobile
 */
const TouchControls: React.FC<TouchControlsProps> = ({
  onDirectionChange,
  disabled = false,
}) => {
  // Riferimento per prevenire doppio tap accidentale
  const lastTapRef = useRef<number>(0);
  
  /**
   * Gestisce il tocco su un pulsante direzionale
   */
  const handleDirectionPress = useCallback((direction: Direction) => {
    // Previeni doppio tap entro 100ms
    const now = Date.now();
    if (now - lastTapRef.current < 100) return;
    lastTapRef.current = now;
    
    // Feedback aptico (se supportato)
    if (navigator.vibrate) {
      navigator.vibrate(10);
    }
    
    // Cambia direzione
    onDirectionChange(direction);
  }, [onDirectionChange]);

  return (
    <div 
      className="touch-controls-container mt-4 md:hidden"
      role="group"
      aria-label="Controlli touch per il gioco"
    >
      {/* Griglia D-pad */}
      <div className="grid grid-cols-3 gap-2 w-40 mx-auto">
        {/* Riga vuota - Su */}
        <div />
        <button
          type="button"
          className="touch-btn"
          onTouchStart={(e) => {
            e.preventDefault();
            handleDirectionPress('UP');
          }}
          onClick={() => handleDirectionPress('UP')}
          disabled={disabled}
          aria-label="Muovi su"
        >
          <svg 
            width="24" 
            height="24" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="3"
            strokeLinecap="round" 
            strokeLinejoin="round"
          >
            <polyline points="18 15 12 9 6 15" />
          </svg>
        </button>
        <div />
        
        {/* Sinistra - Giù - Destra */}
        <button
          type="button"
          className="touch-btn"
          onTouchStart={(e) => {
            e.preventDefault();
            handleDirectionPress('LEFT');
          }}
          onClick={() => handleDirectionPress('LEFT')}
          disabled={disabled}
          aria-label="Muovi a sinistra"
        >
          <svg 
            width="24" 
            height="24" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="3"
            strokeLinecap="round" 
            strokeLinejoin="round"
          >
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>
        <button
          type="button"
          className="touch-btn"
          onTouchStart={(e) => {
            e.preventDefault();
            handleDirectionPress('DOWN');
          }}
          onClick={() => handleDirectionPress('DOWN')}
          disabled={disabled}
          aria-label="Muovi giù"
        >
          <svg 
            width="24" 
            height="24" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="3"
            strokeLinecap="round" 
            strokeLinejoin="round"
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </button>
        <button
          type="button"
          className="touch-btn"
          onTouchStart={(e) => {
            e.preventDefault();
            handleDirectionPress('RIGHT');
          }}
          onClick={() => handleDirectionPress('RIGHT')}
          disabled={disabled}
          aria-label="Muovi a destra"
        >
          <svg 
            width="24" 
            height="24" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="3"
            strokeLinecap="round" 
            strokeLinejoin="round"
          >
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>
        
        {/* Riga vuota */}
        <div />
        <div />
        <div />
      </div>
      
      {/* Istruzioni */}
      <p className="text-center text-xs text-gray-500 mt-2">
        Usa i pulsanti o swipe per muoverti
      </p>
    </div>
  );
};

export default TouchControls;
