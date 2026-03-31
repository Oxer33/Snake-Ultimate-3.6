/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Componente Principale del Gioco
 * ============================================
 * Questo componente integra tutti i sottocomponenti
 * e gestisce la logica principale del gioco.
 * 
 * Funzionalità integrate:
 * - Game loop con motore di gioco
 * - Audio con effetti sonori
 * - Salvataggio punteggi e classifica
 * - Controlli tastiera e touch
 * - Menu, pausa, game over
 */

'use client';

import React, { useEffect, useCallback, useRef, useState } from 'react';
import GameCanvas from '@/components/game/GameCanvas';
import ScoreDisplay from '@/components/ui/ScoreDisplay';
import TouchControls from '@/components/ui/TouchControls';
import MainMenu from '@/components/ui/MainMenu';
import GameOver from '@/components/ui/GameOver';
import ScoreBoard from '@/components/ui/ScoreBoard';
import { gameEngine, GameEngineState } from '@/utils/gameEngine';
import { audioManager } from '@/utils/audioManager';
import { saveHighScore, loadHighScore, saveScore, incrementGamesPlayed } from '@/utils/scoreManager';
import { Direction, GameMode, GameState, GameScreen, Food } from '@/types/game';

/**
 * Componente principale del gioco
 */
const GameContainer: React.FC = () => {
  // Stato della schermata (menu, gioco, classifica, impostazioni)
  const [screen, setScreen] = useState<GameScreen>('menu');
  // Stato del gioco (playing, paused, gameover)
  const [gameState, setGameState] = useState<GameState>('menu');
  // Stato del motore di gioco
  const [engineState, setEngineState] = useState<GameEngineState>({
    snake: [],
    food: [],
    particles: [],
    score: 0,
    level: 1,
    foodEaten: 0,
    direction: 'RIGHT',
    isRunning: false,
  });
  
  // Punteggio più alto
  const [highScore, setHighScore] = useState<number>(0);
  // Modalità di gioco corrente
  const [currentMode, setCurrentMode] = useState<GameMode>('classic');
  // Configurazione griglia
  const [gridSize] = useState(20);
  const [cellSize] = useState(20);
  
  // Riferimento per i tasti premuti (evita ripetizioni)
  const keysPressedRef = useRef<Set<string>>(new Set());
  // Riferimento per inizializzazione audio
  const audioInitializedRef = useRef<boolean>(false);
  
  /**
   * Inizializza l'audio al primo click dell'utente
   */
  const initAudio = useCallback(() => {
    if (!audioInitializedRef.current) {
      audioManager.init();
      audioInitializedRef.current = true;
      console.log('[GameContainer] Audio inizializzato');
    }
  }, []);
  
  /**
   * Callback per quando il motore aggiorna lo stato
   */
  const handleEngineUpdate = useCallback((state: GameEngineState) => {
    setEngineState(state);
  }, []);
  
  /**
   * Callback per collisione (game over)
   */
  const handleCollision = useCallback(() => {
    console.log('[GameContainer] Collisione rilevata!');
    audioManager.playSound('die');
    
    // Salva il punteggio
    const finalScore = gameEngine.getScore();
    if (finalScore > highScore) {
      saveHighScore(finalScore);
      setHighScore(finalScore);
    }
    
    // Salva nella classifica
    saveScore({
      score: finalScore,
      mode: currentMode,
      difficulty: 'medium',
      date: new Date().toISOString(),
      name: 'Giocatore',
      level: gameEngine.getLevel(),
      foodEaten: gameEngine.getLevel() - 1,
    });
    
    incrementGamesPlayed();
    
    setGameState('gameover');
    gameEngine.stop();
  }, [highScore, currentMode]);
  
  /**
   * Callback per cibo mangiato
   */
  const handleFoodEaten = useCallback((food: Food) => {
    console.log('[GameContainer] Cibo mangiato!', food.type);
    if (food.type === 'bonus') {
      audioManager.playSound('bonus');
    } else {
      audioManager.playSound('eat');
    }
  }, []);
  
  /**
   * Avvia una nuova partita
   */
  const startGame = useCallback((mode: GameMode) => {
    console.log('[GameContainer] Avvio partita in modalità:', mode);
    initAudio();
    audioManager.playSound('click');
    
    setCurrentMode(mode);
    
    // Configura il motore di gioco
    gameEngine.initialize({
      gridSize,
      tickRate: mode === 'speed' ? 80 : mode === 'zen' ? 200 : 150,
      initialLength: 3,
      gameMode: mode,
    });
    
    // Registra i callback
    gameEngine.setOnGameStateUpdate(handleEngineUpdate);
    gameEngine.setOnCollision(handleCollision);
    gameEngine.setOnFoodEaten(handleFoodEaten);
    
    // Avvia il gioco
    gameEngine.start();
    setGameState('playing');
    setScreen('game');
  }, [gridSize, initAudio, handleEngineUpdate, handleCollision, handleFoodEaten]);
  
  /**
   * Cambia direzione
   */
  const changeDirection = useCallback((direction: Direction) => {
    gameEngine.changeDirection(direction);
  }, []);
  
  /**
   * Riavvia il gioco
   */
  const restartGame = useCallback(() => {
    console.log('[GameContainer] Riavvio partita');
    audioManager.playSound('click');
    gameEngine.stop();
    startGame(currentMode);
  }, [currentMode, startGame]);
  
  /**
   * Torna al menu
   */
  const goToMenu = useCallback(() => {
    console.log('[GameContainer] Torno al menu');
    audioManager.playSound('click');
    gameEngine.stop();
    setGameState('menu');
    setScreen('menu');
  }, []);
  
  /**
   * Mostra la classifica
   */
  const showScoreBoard = useCallback(() => {
    audioManager.playSound('click');
    setScreen('scoreboard');
  }, []);
  
  /**
   * Gestisce i tasti premuti
   */
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    // Previeni comportamento di default per i tasti di gioco
    const gameKeys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'w', 'a', 's', 'd', ' ', 'Escape', 'Enter'];
    
    if (gameKeys.includes(e.key)) {
      e.preventDefault();
    }
    
    // Ignora se il tasto è già premuto
    if (keysPressedRef.current.has(e.key)) return;
    keysPressedRef.current.add(e.key);
    
    // Mappa tasti -> direzioni
    const keyDirectionMap: Record<string, Direction> = {
      ArrowUp: 'UP',
      ArrowDown: 'DOWN',
      ArrowLeft: 'LEFT',
      ArrowRight: 'RIGHT',
      w: 'UP',
      s: 'DOWN',
      a: 'LEFT',
      d: 'RIGHT',
      W: 'UP',
      S: 'DOWN',
      A: 'LEFT',
      D: 'RIGHT',
    };
    
    if (gameState === 'playing' && keyDirectionMap[e.key]) {
      changeDirection(keyDirectionMap[e.key]);
    }
    
    // Pausa con spazio
    if (e.key === ' ' && gameState === 'playing') {
      gameEngine.stop();
      setGameState('paused');
    }
    
    // Riprendi con spazio
    if (e.key === ' ' && gameState === 'paused') {
      gameEngine.start();
      setGameState('playing');
    }
    
    // Riavvia con Enter dopo game over
    if (e.key === 'Enter' && gameState === 'gameover') {
      restartGame();
    }
    
    // Menu con ESC
    if (e.key === 'Escape' && (gameState === 'playing' || gameState === 'paused')) {
      goToMenu();
    }
  }, [gameState, changeDirection, restartGame, goToMenu]);
  
  /**
   * Gestisce il rilascio dei tasti
   */
  const handleKeyUp = useCallback((e: KeyboardEvent) => {
    keysPressedRef.current.delete(e.key);
  }, []);
  
  // Registra gli event listener per la tastiera
  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [handleKeyDown, handleKeyUp]);
  
  // Carica il punteggio più alto all'avvio
  useEffect(() => {
    setHighScore(loadHighScore());
  }, []);
  
  // Pulisci il motore quando il componente viene smontato
  useEffect(() => {
    return () => {
      gameEngine.stop();
    };
  }, []);
  
  /**
   * Renderizza la schermata di gioco
   */
  const renderGameScreen = () => {
    return (
      <div className="game-screen min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-b from-gray-900 via-gray-900 to-black">
        {/* Intestazione con punteggio */}
        <ScoreDisplay
          score={engineState.score}
          highScore={Math.max(engineState.score, highScore)}
          level={engineState.level}
          foodEaten={engineState.foodEaten}
        />
        
        {/* Area di gioco */}
        <div className="game-area relative">
          <GameCanvas
            snake={engineState.snake}
            food={engineState.food}
            particles={engineState.particles}
            config={{
              mode: currentMode,
              difficulty: 'medium',
              gridSize,
              cellSize,
              initialSpeed: 150,
              speedIncrement: 5,
              initialSnakeLength: 3,
              maxFoodOnGrid: 1,
              obstaclesEnabled: false,
              powerUpsEnabled: false,
            }}
            isRunning={engineState.isRunning}
            score={engineState.score}
            level={engineState.level}
          />
          
          {/* Overlay pausa */}
          {gameState === 'paused' && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/70 backdrop-blur-sm rounded-xl">
              <div className="text-center">
                <div className="text-6xl mb-4">⏸️</div>
                <h2 className="text-3xl font-bold text-white mb-4">PAUSA</h2>
                <p className="text-gray-400">Premi SPAZIO per continuare</p>
              </div>
            </div>
          )}
        </div>
        
        {/* Controlli touch (solo mobile) */}
        <TouchControls
          onDirectionChange={changeDirection}
          disabled={gameState !== 'playing'}
        />
        
        {/* Istruzioni */}
        <div className="mt-4 text-center text-gray-500 text-xs">
          <p>Frecce/WASD per muoversi • SPAZIO per pausa • ESC per il menu</p>
        </div>
        
        {/* Game Over Overlay */}
        {gameState === 'gameover' && (
          <GameOver
            score={engineState.score}
            highScore={highScore}
            level={engineState.level}
            foodEaten={engineState.foodEaten}
            onRestart={restartGame}
            onMenu={goToMenu}
          />
        )}
      </div>
    );
  };
  
  /**
   * Renderizza in base alla schermata corrente
   */
  const renderScreen = () => {
    switch (screen) {
      case 'menu':
        return (
          <MainMenu
            onStart={startGame}
            onSettings={() => console.log('Impostazioni')}
            onScores={showScoreBoard}
          />
        );
      case 'game':
        return renderGameScreen();
      case 'scoreboard':
        return <ScoreBoard onBack={goToMenu} />;
      default:
        return renderGameScreen();
    }
  };
  
  return (
    <div className="snake-ultimate-game">
      {renderScreen()}
    </div>
  );
};

export default GameContainer;
