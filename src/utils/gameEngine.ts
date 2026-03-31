/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Motore di Gioco
 * ============================================
 * Questo è il cuore del gioco. Gestisce:
 * - Game loop principale
 * - Movimento del serpente
 * - Collisioni
 * - Generazione del cibo
 * - Sistema dei punteggi
 * - Effetti particellari
 */

import { 
  Direction, 
  SnakeSegment, 
  Food, 
  Position, 
  Particle,
  GameMode,
} from '@/types/game';

/**
 * Genera un ID univoco
 */
const generateId = (): string => {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * Motore di gioco Snake
 * Classe che gestisce tutta la logica del gioco
 */
export class SnakeGameEngine {
  // Stato del gioco
  private snake: SnakeSegment[] = [];
  private food: Food[] = [];
  private particles: Particle[] = [];
  private direction: Direction = 'RIGHT';
  private nextDirection: Direction = 'RIGHT';
  private isRunning: boolean = false;
  private gameLoopId: number | null = null;
  private lastUpdateTime: number = 0;
  private accumulator: number = 0;
  
  // Configurazione
  private gridSize: number = 20;
  private tickRate: number = 150; // ms tra ogni aggiornamento
  private gameMode: GameMode = 'classic';
  
  // Callbacks
  private onGameStateUpdate: ((state: GameEngineState) => void) | null = null;
  private onCollision: ((type: CollisionType) => void) | null = null;
  private onFoodEaten: ((food: Food) => void) | null = null;
  private onScoreUpdate: ((score: number) => void) | null = null;
  
  // Punteggio
  private score: number = 0;
  private level: number = 1;
  private foodEaten: number = 0;

  /**
   * Costruttore del motore di gioco
   */
  constructor() {
    console.log('[SnakeGameEngine] Motore inizializzato');
  }

  /**
   * Inizializza una nuova partita
   */
  public initialize(config: {
    gridSize?: number;
    tickRate?: number;
    initialLength?: number;
    gameMode?: GameMode;
  } = {}): void {
    console.log('[SnakeGameEngine] Inizializzazione partita', config);
    
    this.gridSize = config.gridSize || 20;
    this.tickRate = config.tickRate || 150;
    this.gameMode = config.gameMode || 'classic';
    
    // Reset stato
    this.score = 0;
    this.level = 1;
    this.foodEaten = 0;
    this.particles = [];
    this.food = [];
    
    // Crea serpente iniziale al centro della griglia
    const centerX = Math.floor(this.gridSize / 2);
    const centerY = Math.floor(this.gridSize / 2);
    const length = config.initialLength || 3;
    
    this.snake = Array.from({ length }, (_, i) => ({
      id: generateId(),
      x: centerX - i,
      y: centerY,
      isHead: i === 0,
      direction: 'RIGHT' as Direction,
    }));
    
    // Genera cibo iniziale
    this.spawnFood();
    
    // Notifica aggiornamento stato
    this.notifyStateUpdate();
  }

  /**
   * Avvia il game loop
   */
  public start(): void {
    if (this.isRunning) {
      console.warn('[SnakeGameEngine] Il gioco è già in corso');
      return;
    }
    
    console.log('[SnakeGameEngine] Avvio game loop');
    this.isRunning = true;
    this.lastUpdateTime = performance.now();
    this.accumulator = 0;
    
    // Avvia il game loop con requestAnimationFrame
    this.gameLoopId = requestAnimationFrame((time) => this.gameLoop(time));
  }

  /**
   * Ferma il game loop
   */
  public stop(): void {
    console.log('[SnakeGameEngine] Arresto game loop');
    this.isRunning = false;
    
    if (this.gameLoopId !== null) {
      cancelAnimationFrame(this.gameLoopId);
      this.gameLoopId = null;
    }
  }

  /**
   * Game loop principale
   * Utilizza un accumulatore per aggiornamenti fissi
   */
  private gameLoop = (currentTime: number): void => {
    if (!this.isRunning) return;
    
    // Calcola il delta time
    const deltaTime = currentTime - this.lastUpdateTime;
    this.lastUpdateTime = currentTime;
    this.accumulator += deltaTime;
    
    // Aggiorna la logica del gioco a intervalli fissi
    while (this.accumulator >= this.tickRate) {
      this.update();
      this.accumulator -= this.tickRate;
    }
    
    // Richiedi il prossimo frame
    this.gameLoopId = requestAnimationFrame(this.gameLoop);
  };

  /**
   * Aggiorna lo stato del gioco (chiamato ad ogni tick)
   */
  private update(): void {
    // Aggiorna la direzione corrente
    this.direction = this.nextDirection;
    
    // Muovi il serpente
    this.moveSnake();
    
    // Controlla collisioni
    this.checkCollisions();
    
    // Aggiorna particelle
    this.updateParticles();
    
    // Notifica aggiornamento stato
    this.notifyStateUpdate();
  }

  /**
   * Muove il serpente nella direzione corrente
   */
  private moveSnake(): void {
    if (this.snake.length === 0) return;
    
    const head = this.snake[0];
    let newX = head.x;
    let newY = head.y;
    
    // Calcola nuova posizione in base alla direzione
    switch (this.direction) {
      case 'UP':
        newY = head.y - 1;
        break;
      case 'DOWN':
        newY = head.y + 1;
        break;
      case 'LEFT':
        newX = head.x - 1;
        break;
      case 'RIGHT':
        newX = head.x + 1;
        break;
    }
    
    // Gestisci il wrapping (attraversamento bordi)
    if (this.gameMode === 'zen' || this.gameMode === 'classic') {
      newX = (newX + this.gridSize) % this.gridSize;
      newY = (newY + this.gridSize) % this.gridSize;
    }
    
    // Crea nuova testa
    const newHead: SnakeSegment = {
      id: generateId(),
      x: newX,
      y: newY,
      isHead: true,
      direction: this.direction,
    };
    
    // Aggiungi nuova testa e rimuovi coda
    this.snake = [newHead, ...this.snake.map((segment, index) => ({
      ...segment,
      isHead: false,
    }))];
    
    // Controlla se ha mangiato il cibo
    const foodIndex = this.food.findIndex(f => f.x === newX && f.y === newY);
    
    if (foodIndex !== -1) {
      // Ha mangiato!
      const eatenFood = this.food[foodIndex];
      this.food.splice(foodIndex, 1);
      
      // Non rimuovere la coda (il serpente cresce)
      this.snake.push({ ...this.snake[this.snake.length - 1] });
      
      // Aggiorna punteggio
      this.onFoodEaten?.(eatenFood);
      this.addScore(eatenFood.value);
      this.foodEaten++;
      
      // Genera effetti particellari
      this.spawnEatParticles(eatenFood);
      
      // Genera nuovo cibo
      this.spawnFood();
      
      // Controlla livello
      this.checkLevelUp();
    } else {
      // Rimuovi la coda (movimento normale)
      this.snake.pop();
    }
  }

  /**
   * Controlla le collisioni
   */
  private checkCollisions(): void {
    if (this.snake.length === 0) return;
    
    const head = this.snake[0];
    
    // Collisione con se stesso
    for (let i = 1; i < this.snake.length; i++) {
      if (head.x === this.snake[i].x && head.y === this.snake[i].y) {
        this.onCollision?.('self');
        this.stop();
        return;
      }
    }
    
    // Collisione con i bordi (solo per modalità che lo prevedono)
    if (this.gameMode === 'speed' || this.gameMode === 'obstacles' || this.gameMode === 'challenge') {
      if (head.x < 0 || head.x >= this.gridSize || head.y < 0 || head.y >= this.gridSize) {
        this.onCollision?.('wall');
        this.stop();
        return;
      }
    }
  }

  /**
   * Genera cibo in una posizione casuale
   */
  private spawnFood(): void {
    const occupiedPositions = new Set([
      ...this.snake.map(s => `${s.x},${s.y}`),
      ...this.food.map(f => `${f.x},${f.y}`),
    ]);
    
    let attempts = 0;
    const maxAttempts = this.gridSize * this.gridSize;
    
    while (attempts < maxAttempts) {
      const x = Math.floor(Math.random() * this.gridSize);
      const y = Math.floor(Math.random() * this.gridSize);
      
      if (!occupiedPositions.has(`${x},${y}`)) {
        const newFood: Food = {
          id: generateId(),
          x,
          y,
          type: Math.random() < 0.1 ? 'bonus' : 'normal',
          value: Math.random() < 0.1 ? 50 : 10,
          spawnTime: Date.now(),
        };
        
        this.food.push(newFood);
        return;
      }
      
      attempts++;
    }
  }

  /**
   * Genera particelle quando il serpente mangia
   */
  private spawnEatParticles(food: Food): void {
    const colors = ['#00ff88', '#7b61ff', '#ff4757', '#ffa502', '#2ed573'];
    
    for (let i = 0; i < 12; i++) {
      const angle = (Math.PI * 2 * i) / 12;
      const speed = 2 + Math.random() * 3;
      
      this.particles.push({
        id: generateId(),
        x: food.x,
        y: food.y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 1,
        color: colors[Math.floor(Math.random() * colors.length)],
        size: 3 + Math.random() * 4,
        decay: 0.02 + Math.random() * 0.02,
      });
    }
  }

  /**
   * Aggiorna le particelle
   */
  private updateParticles(): void {
    this.particles = this.particles
      .map(p => ({
        ...p,
        x: p.x + p.vx * 0.1,
        y: p.y + p.vy * 0.1,
        life: p.life - p.decay,
      }))
      .filter(p => p.life > 0);
  }

  /**
   * Controlla se è ora di salire di livello
   */
  private checkLevelUp(): void {
    const newLevel = Math.floor(this.foodEaten / 5) + 1;
    
    if (newLevel > this.level) {
      this.level = newLevel;
      // Aumenta la velocità
      this.tickRate = Math.max(50, 150 - (this.level - 1) * 10);
    }
  }

  /**
   * Aggiunge punti al punteggio
   */
  private addScore(points: number): void {
    this.score += points;
    this.onScoreUpdate?.(this.score);
  }

  /**
   * Cambia direzione del serpente
   */
  public changeDirection(newDirection: Direction): void {
    const opposites: Record<Direction, Direction> = {
      UP: 'DOWN',
      DOWN: 'UP',
      LEFT: 'RIGHT',
      RIGHT: 'LEFT',
    };
    
    // Impedisce inversioni di direzione
    if (opposites[newDirection] !== this.direction) {
      this.nextDirection = newDirection;
    }
  }

  /**
   * Notifica lo stato attuale ai listener
   */
  private notifyStateUpdate(): void {
    this.onGameStateUpdate?.({
      snake: [...this.snake],
      food: [...this.food],
      particles: [...this.particles],
      score: this.score,
      level: this.level,
      foodEaten: this.foodEaten,
      direction: this.direction,
      isRunning: this.isRunning,
    });
  }

  // ============================================
  // GETTER
  // ============================================

  public getSnake(): SnakeSegment[] {
    return [...this.snake];
  }

  public getFood(): Food[] {
    return [...this.food];
  }

  public getParticles(): Particle[] {
    return [...this.particles];
  }

  public getScore(): number {
    return this.score;
  }

  public getLevel(): number {
    return this.level;
  }

  public getDirection(): Direction {
    return this.direction;
  }

  public getIsRunning(): boolean {
    return this.isRunning;
  }

  // ============================================
  // CALLBACKS
  // ============================================

  public setOnGameStateUpdate(callback: (state: GameEngineState) => void): void {
    this.onGameStateUpdate = callback;
  }

  public setOnCollision(callback: (type: CollisionType) => void): void {
    this.onCollision = callback;
  }

  public setOnFoodEaten(callback: (food: Food) => void): void {
    this.onFoodEaten = callback;
  }

  public setOnScoreUpdate(callback: (score: number) => void): void {
    this.onScoreUpdate = callback;
  }
}

/**
 * Tipo di collisione
 */
export type CollisionType = 'self' | 'wall' | 'obstacle';

/**
 * Stato del motore di gioco
 */
export interface GameEngineState {
  snake: SnakeSegment[];
  food: Food[];
  particles: Particle[];
  score: number;
  level: number;
  foodEaten: number;
  direction: Direction;
  isRunning: boolean;
}

// Esporta l'istanza singleton
export const gameEngine = new SnakeGameEngine();
export default gameEngine;
