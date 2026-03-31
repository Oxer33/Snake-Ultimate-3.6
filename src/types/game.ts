/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Definizioni dei Tipi
 * ============================================
 * Questo file contiene tutte le interfacce e i tipi
 * utilizzati in tutto il progetto per garantire
 * type-safety e migliore documentazione.
 */

/**
 * Direzione del serpente
 */
export type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT';

/**
 * Posizione sulla griglia (x, y)
 */
export interface Position {
  x: number;
  y: number;
}

/**
 * Segmento del serpente
 */
export interface SnakeSegment extends Position {
  id: string;
  isHead: boolean;
  direction: Direction;
}

/**
 * Tipo di cibo/oggetto sulla griglia
 */
export type FoodType = 'normal' | 'bonus' | 'speed' | 'slow' | 'shield';

/**
 * Oggetto cibo sulla griglia
 */
export interface Food extends Position {
  id: string;
  type: FoodType;
  value: number;
  spawnTime: number;
  lifetime?: number; // Tempo di vita in ms (per oggetti temporanei)
}

/**
 * Tipo di ostacolo
 */
export type ObstacleType = 'wall' | 'ice' | 'portal';

/**
 * Ostacolo sulla griglia
 */
export interface Obstacle extends Position {
  id: string;
  type: ObstacleType;
  targetPosition?: Position; // Per i portali
}

/**
 * Particella per effetti visivi
 */
export interface Particle {
  id: string;
  x: number;
  y: number;
  vx: number; // Velocità X
  vy: number; // Velocità Y
  life: number; // Vita rimanente (0-1)
  color: string;
  size: number;
  decay: number; // Velocità di decadimento
}

/**
 * Stato del gioco
 */
export type GameState = 'menu' | 'playing' | 'paused' | 'gameover' | 'settings';

/**
 * Schermata corrente dell'app
 */
export type GameScreen = 'menu' | 'game' | 'scoreboard' | 'settings';

/**
 * Modalità di gioco
 */
export type GameMode = 'classic' | 'speed' | 'obstacles' | 'zen' | 'challenge';

/**
 * Livello di difficoltà
 */
export type Difficulty = 'easy' | 'medium' | 'hard' | 'insane';

/**
 * Configurazione della partita
 */
export interface GameConfig {
  mode: GameMode;
  difficulty: Difficulty;
  gridSize: number; // Dimensione della griglia (es. 20x20)
  cellSize: number; // Dimensione di ogni cella in pixel
  initialSpeed: number; // Velocità iniziale in ms
  speedIncrement: number; // Incremento velocità per livello
  initialSnakeLength: number;
  maxFoodOnGrid: number;
  obstaclesEnabled: boolean;
  powerUpsEnabled: boolean;
}

/**
 * Statistiche di gioco
 */
export interface GameStats {
  score: number;
  highScore: number;
  level: number;
  foodEaten: number;
  bonusFoodEaten: number;
  timePlayed: number; // in secondi
  gamesPlayed: number;
  gamesWon: number;
}

/**
 * Record nella classifica
 */
export interface ScoreRecord {
  id: string;
  score: number;
  mode: GameMode;
  difficulty: Difficulty;
  date: string;
  name: string;
  level: number;
  foodEaten: number;
}

/**
 * Impostazioni del gioco
 */
export interface GameSettings {
  soundEnabled: boolean;
  musicVolume: number;
  sfxVolume: number;
  vibrationEnabled: boolean;
  showGrid: boolean;
  snakeSkin: string;
  theme: string;
  controls: 'arrows' | 'wasd' | 'swipe';
}

/**
 * Tipo di evento di gioco
 */
export type GameEventType = 
  | 'SNAKE_MOVE'
  | 'FOOD_EATEN'
  | 'BONUS_EATEN'
  | 'COLLISION'
  | 'LEVEL_UP'
  | 'GAME_OVER'
  | 'PAUSE'
  | 'RESUME'
  | 'RESTART';

/**
 * Evento di gioco
 */
export interface GameEvent {
  type: GameEventType;
  timestamp: number;
  data?: Record<string, unknown>;
}

/**
 * Props per il componente Canvas
 */
export interface GameCanvasProps {
  snake: SnakeSegment[];
  food: Food[];
  obstacles: Obstacle[];
  particles: Particle[];
  gameState: GameState;
  config: GameConfig;
}

/**
 * Props per il componente Score
 */
export interface ScoreDisplayProps {
  score: number;
  highScore: number;
  level: number;
}

/**
 * Props per il componente GameOver
 */
export interface GameOverProps {
  score: number;
  highScore: number;
  onRestart: () => void;
  onMenu: () => void;
}

/**
 * Props per il componente Menu
 */
export interface MainMenuProps {
  onStart: (mode: GameMode) => void;
  onSettings: () => void;
  onScores: () => void;
}

/**
 * Hook return type per useGame
 */
export interface UseGameReturn {
  snake: SnakeSegment[];
  food: Food[];
  obstacles: Obstacle[];
  particles: Particle[];
  gameState: GameState;
  stats: GameStats;
  config: GameConfig;
  direction: Direction;
  changeDirection: (newDirection: Direction) => void;
  startGame: (mode: GameMode) => void;
  pauseGame: () => void;
  resumeGame: () => void;
  restartGame: () => void;
  goToMenu: () => void;
}
