/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Pagina Principale
 * ============================================
 * Questa è la pagina principale dell'applicazione.
 * Importa e renderizza il componente GameContainer
 * che gestisce tutto il gioco.
 */

'use client';

import React from 'react';
import GameContainer from '@/components/game/GameContainer';

/**
 * Componente HomePage
 * Punto di ingresso principale dell'applicazione
 */
export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      <GameContainer />
    </main>
  );
}
