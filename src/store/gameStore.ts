/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Store di Stato Globale
 * ============================================
 * Utilizziamo Zustand per la gestione dello stato globale.
 * Questo store gestisce tutte le variabili di stato del gioco
 * in modo centralizzato e reattivo.
 */

import { create } from 'zustand';
import { 
  Direction, 
  SnakeSegment, 
  Food, 
  Obstacle, 
  Particle, 
  GameState, 
  GameMode, 
  Difficulty, 
  GameConfig, 
  GameStats, 
  GameSettings 
} from '@/types/game';

/**
 * Configurazioni predefinite per ogni modalità di gioco
 */
const MODE_CONFIGS: Record<GameMode, Partial<GameConfig>> = {
  classic: {
    initialSpeed: 150,
    speedIncrement: 5,
    initialSnakeLength: 3,
    maxFoodOnGrid: 1,
    obstaclesEnabled: false,
    powerUpsEnabled: false,
  },
  speed: {
    initialSpeed: 80,
    speedIncrement: 10,
    initialSnakeLength: 3,
    maxFoodOnGrid: 2,
    obstaclesEnabled: false,
    powerUpsEnabled: true,
  },
  obstacles: {
    initialSpeed: 120,
    speedIncrement: 8,
    initialSnakeLength: 3,
    maxFoodOnGrid: 1,
    obstaclesEnabled: true,
    powerUpsEnabled: true,
  },
  zen: {
    initialSpeed: 200,
    speedIncrement: 0,
    initialSnakeLength: 3,
    maxFoodOnGrid: 3,
    obstaclesEnabled: false,
    powerUpsEnabled: false,
  },
  challenge: {
    initialSpeed: 100,
    speedIncrement: 15,
    initialSnakeLength: 5,
    maxFoodOnGrid: 1,
    obstaclesEnabled: true,
    powerUpsEnabled: true,
  },
};

/**
 * Configurazioni predefinite per ogni difficoltà
 */
const DIFFICULTY_CONFIGS: Record<Difficulty, Partial<GameConfig>> = {
  easy: { gridSize: 15, cellSize: 24 },
  medium: { gridSize: 20, cellSize: 20 },
  hard: { gridSize: 25, cellSize: 16 },
  insane: { gridSize: 30, cellSize: 14 },
};

/**
 * Stato iniziale del serpente
 */
const createInitialSnake = (length: number, gridSize: number): SnakeSegment[] => {
  const centerX = Math.floor(gridSize / 2);
  const centerY = Math.floor(gridSize / 2);
  
  return Array.from({ length }, (_, i) => ({
    id: `snake-${i}`,
    x: centerX - i,
    y: centerY,
    isHead: i === 0,
    direction: 'RIGHT' as Direction,
  }));
};

/**
 * Interfaccia dello store
 */
interface GameStore {
  // Stato del gioco
  gameState: GameState;
  gameMode: GameMode;
  difficulty: Difficulty;
  
  // Entità di gioco
  snake: SnakeSegment[];
  food: Food[];
  obstacles: Obstacle[];
  particles: Particle[];
  
  // Direzione e movimento
  direction: Direction;
  nextDirection: Direction;
  speed: number;
  
  // Statistiche
  stats: GameStats;
  
  // Configurazione
  config: GameConfig;
  settings: GameSettings;
  
  // Azioni - Movimento
  setDirection: (direction: Direction) => void;
  moveSnake: () => void;
  
  // Azioni - Stato del gioco
  setGameState: (state: GameState) => void;
  startGame: (mode: GameMode, difficulty?: Difficulty) => void;
  pauseGame: () => void;
  resumeGame: () => void;
  restartGame: () => void;
  goToMenu: () => void;
  gameOver: () => void;
  
  // Azioni - Entità
  addFood: (food: Food) => void;
  removeFood: (id: string) => void;
  addObstacle: (obstacle: Obstacle) => void;
  addParticle: (particle: Particle) => void;
  clearParticles: () => void;
  
  // Azioni - Statistiche
  incrementScore: (points: number) => void;
  incrementLevel: () => void;
  updateHighScore: () => void;
  
  // Azioni - Configurazione
  setSettings: (settings: Partial<GameSettings>) => void;
}

/**
 * Carica i punteggi salvati dal localStorage
 */
const loadHighScore = (): number => {
  if (typeof window === 'undefined') return 0;
  try {
    const saved = localStorage.getItem('snake-ultimate-highscore');
    return saved ? parseInt(saved, 10) : 0;
  } catch {
    return 0;
  }
};

/**
 * Salva il punteggio nel localStorage
 */
const saveHighScore = (score: number): void => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem('snake-ultimate-highscore', score.toString());
  } catch (e) {
    console.warn('Impossibile salvare il punteggio:', e);
  }
};

/**
 * Creazione dello store Zustand
 */
export const useGameStore = create<GameStore>((set, get) => ({
  // ============================================
  // STATO INIZIALE
  // ============================================
  gameState: 'menu',
  gameMode: 'classic',
  difficulty: 'medium',
  
  snake: [],
  food: [],
  obstacles: [],
  particles: [],
  
  direction: 'RIGHT',
  nextDirection: 'RIGHT',
  speed: 150,
  
  stats: {
    score: 0,
    highScore: loadHighScore(),
    level: 1,
    foodEaten: 0,
    bonusFoodEaten: 0,
    timePlayed: 0,
    gamesPlayed: 0,
    gamesWon: 0,
  },
  
  config: {
    mode: 'classic',
    difficulty: 'medium',
    gridSize: 20,
    cellSize: 20,
    initialSpeed: 150,
    speedIncrement: 5,
    initialSnakeLength: 3,
    maxFoodOnGrid: 1,
    obstaclesEnabled: false,
    powerUpsEnabled: false,
  },
  
  settings: {
    soundEnabled: true,
    musicVolume: 0.5,
    sfxVolume: 0.7,
    vibrationEnabled: true,
    showGrid: true,
    snakeSkin: 'classic',
    theme: 'dark',
    controls: 'arrows',
  },
  
  // ============================================
  // AZIONI - MOVIMENTO
  // ============================================
  
  /**
   * Imposta la prossima direzione (con validazione)
   * Impedisce inversioni di direzione (es. da RIGHT a LEFT)
   */
  setDirection: (newDirection: Direction) => {
    const { direction } = get();
    
    // Mappa delle direzioni opposte (non permesse)
    const oppositeDirections: Record<Direction, Direction> = {
      UP: 'DOWN',
      DOWN: 'UP',
      LEFT: 'RIGHT',
      RIGHT: 'LEFT',
    };
    
    // Se la nuova direzione non è l'opposto di quella corrente, accettala
    if (oppositeDirections[newDirection] !== direction) {
      set({ nextDirection: newDirection });
    }
  },
  
  /**
   * Muove il serpente nella direzione corrente
   * Questa funzione verrà chiamata dal game loop
   */
  moveSnake: () => {
    const { snake, nextDirection, speed, stats, config } = get();
    
    if (snake.length === 0) return;
    
    // Aggiorna la direzione corrente
    const direction = nextDirection;
    
    // Calcola la nuova posizione della testa
    const head = snake[0];
    let newX = head.x;
    let newY = head.y;
    
    switch (direction) {
      case 'UP':
        newY = (head.y - 1 + config.gridSize) % config.gridSize;
        break;
      case 'DOWN':
        newY = (head.y + 1) % config.gridSize;
        break;
      case 'LEFT':
        newX = (head.x - 1 + config.gridSize) % config.gridSize;
        break;
      case 'RIGHT':
        newX = (head.x + 1) % config.gridSize;
        break;
    }
    
    // Crea la nuova testa
    const newHead: SnakeSegment = {
      id: `snake-head-${Date.now()}`,
      x: newX,
      y: newY,
      isHead: true,
      direction,
    };
    
    // Aggiorna i segmenti del serpente
    const newSnake = [newHead, ...snake.map((segment, index) => ({
      ...segment,
      isHead: false,
      direction: index === 0 ? direction : segment.direction,
    }))];
    
    // Rimuovi la coda (a meno che non abbia mangiato)
    // La gestione del cibo viene fatta nel game loop
    newSnake.pop();
    
    set({
      snake: newSnake,
      direction,
      speed: Math.max(50, speed - 0.01), // Leggero aumento di velocità
    });
  },
  
  // ============================================
  // AZIONI - STATO DEL GIOCO
  // ============================================
  
  setGameState: (state: GameState) => {
    set({ gameState: state });
  },
  
  /**
   * Avvia una nuova partita
   */
  startGame: (mode: GameMode, difficulty: Difficulty = 'medium') => {
    const modeConfig = MODE_CONFIGS[mode];
    const difficultyConfig = DIFFICULTY_CONFIGS[difficulty];
    
    const config: GameConfig = {
      mode,
      difficulty,
      gridSize: difficultyConfig.gridSize!,
      cellSize: difficultyConfig.cellSize!,
      initialSpeed: modeConfig.initialSpeed!,
      speedIncrement: modeConfig.speedIncrement!,
      initialSnakeLength: modeConfig.initialSnakeLength!,
      maxFoodOnGrid: modeConfig.maxFoodOnGrid!,
      obstaclesEnabled: modeConfig.obstaclesEnabled!,
      powerUpsEnabled: modeConfig.powerUpsEnabled!,
    };
    
    const snake = createInitialSnake(config.initialSnakeLength, config.gridSize);
    
    set({
      gameState: 'playing',
      gameMode: mode,
      difficulty,
      config,
      snake,
      food: [],
      obstacles: [],
      particles: [],
      direction: 'RIGHT',
      nextDirection: 'RIGHT',
      speed: config.initialSpeed,
      stats: {
        score: 0,
        highScore: get().stats.highScore,
        level: 1,
        foodEaten: 0,
        bonusFoodEaten: 0,
        timePlayed: 0,
        gamesPlayed: get().stats.gamesPlayed + 1,
        gamesWon: get().stats.gamesWon,
      },
    });
  },
  
  pauseGame: () => {
    set({ gameState: 'paused' });
  },
  
  resumeGame: () => {
    set({ gameState: 'playing' });
  },
  
  restartGame: () => {
    const { gameMode, difficulty } = get();
    get().startGame(gameMode, difficulty);
  },
  
  goToMenu: () => {
    set({ gameState: 'menu' });
  },
  
  /**
   * Gestisce il game over
   */
  gameOver: () => {
    const { stats } = get();
    
    // Aggiorna il punteggio più alto se necessario
    if (stats.score > stats.highScore) {
      saveHighScore(stats.score);
      set((state) => ({
        stats: { ...state.stats, highScore: state.stats.score },
      }));
    }
    
    set({ gameState: 'gameover' });
  },
  
  // ============================================
  // AZIONI - ENTITÀ
  // ============================================
  
  addFood: (food: Food) => {
    set((state) => ({
      food: [...state.food, food],
    }));
  },
  
  removeFood: (id: string) => {
    set((state) => ({
      food: state.food.filter((f) => f.id !== id),
    }));
  },
  
  addObstacle: (obstacle: Obstacle) => {
    set((state) => ({
      obstacles: [...state.obstacles, obstacle],
    }));
  },
  
  addParticle: (particle: Particle) => {
    set((state) => ({
      particles: [...state.particles, particle],
    }));
  },
  
  clearParticles: () => {
    set({ particles: [] });
  },
  
  // ============================================
  // AZIONI - STATISTICHE
  // ============================================
  
  incrementScore: (points: number) => {
    set((state) => ({
      stats: {
        ...state.stats,
        score: state.stats.score + points,
      },
    }));
  },
  
  incrementLevel: () => {
    set((state) => ({
      stats: {
        ...state.stats,
        level: state.stats.level + 1,
      },
      speed: Math.max(50, state.speed - state.config.speedIncrement),
    }));
  },
  
  updateHighScore: () => {
    const { stats } = get();
    if (stats.score > stats.highScore) {
      saveHighScore(stats.score);
      set((state) => ({
        stats: { ...state.stats, highScore: state.stats.score },
      }));
    }
  },
  
  // ============================================
  // AZIONI - CONFIGURAZIONE
  // ============================================
  
  setSettings: (newSettings: Partial<GameSettings>) => {
    set((state) => ({
      settings: { ...state.settings, ...newSettings },
    }));
  },
}));

// Esporta l'hook per l'utilizzo nei componenti
export default useGameStore;
