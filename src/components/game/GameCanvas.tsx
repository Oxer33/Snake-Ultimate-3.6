/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Componente Canvas di Gioco
 * ============================================
 * Questo componente gestisce il rendering grafico
 * del gioco utilizzando l'elemento HTML5 Canvas.
 * 
 * Caratteristiche:
 * - Rendering ottimizzato con double buffering
 * - Effetti glow e gradienti
 * - Animazioni fluide a 60fps
 * - Supporto per temi personalizzati
 */

'use client';

import React, { useRef, useEffect, useCallback } from 'react';
import { SnakeSegment, Food, Particle, GameConfig } from '@/types/game';

/**
 * Props del componente GameCanvas
 */
interface GameCanvasProps {
  snake: SnakeSegment[];
  food: Food[];
  particles: Particle[];
  config: GameConfig;
  isRunning: boolean;
  score: number;
  level: number;
}

/**
 * Componente Canvas per il rendering del gioco
 */
const GameCanvas: React.FC<GameCanvasProps> = ({
  snake,
  food,
  particles,
  config,
  isRunning,
  score,
  level,
}) => {
  // Riferimento al canvas
  const canvasRef = useRef<HTMLCanvasElement>(null);
  // Riferimento per l'animation frame
  const animationRef = useRef<number | null>(null);
  // Riferimento per lo stato del gioco (evita re-render)
  const gameStateRef = useRef({
    snake,
    food,
    particles,
    config,
    isRunning,
    score,
    level,
  });

  // Aggiorna il ref quando le props cambiano
  useEffect(() => {
    gameStateRef.current = {
      snake,
      food,
      particles,
      config,
      isRunning,
      score,
      level,
    };
  }, [snake, food, particles, config, isRunning, score, level]);

  /**
   * Disegna lo sfondo della griglia
   */
  const drawBackground = useCallback((ctx: CanvasRenderingContext2D, width: number, height: number) => {
    const { config } = gameStateRef.current;
    const { gridSize, cellSize } = config;
    
    // Sfondo principale
    ctx.fillStyle = '#0d1117';
    ctx.fillRect(0, 0, width, height);
    
    // Griglia sottile
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
    ctx.lineWidth = 1;
    
    for (let i = 0; i <= gridSize; i++) {
      // Linee verticali
      ctx.beginPath();
      ctx.moveTo(i * cellSize, 0);
      ctx.lineTo(i * cellSize, height);
      ctx.stroke();
      
      // Linee orizzontali
      ctx.beginPath();
      ctx.moveTo(0, i * cellSize);
      ctx.lineTo(width, i * cellSize);
      ctx.stroke();
    }
    
    // Bordo luminoso
    const gradient = ctx.createLinearGradient(0, 0, width, height);
    gradient.addColorStop(0, 'rgba(0, 255, 136, 0.3)');
    gradient.addColorStop(0.5, 'rgba(123, 97, 255, 0.3)');
    gradient.addColorStop(1, 'rgba(0, 255, 136, 0.3)');
    
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 3;
    ctx.strokeRect(1, 1, width - 2, height - 2);
  }, []);

  /**
   * Disegna un segmento del serpente
   */
  const drawSnakeSegment = useCallback(
    (ctx: CanvasRenderingContext2D, segment: SnakeSegment, cellSize: number) => {
      const x = segment.x * cellSize;
      const y = segment.y * cellSize;
      const padding = 1;
      
      if (segment.isHead) {
        // Testa del serpente con effetto glow
        ctx.shadowColor = '#00ff88';
        ctx.shadowBlur = 15;
        
        // Gradiente per la testa
        const gradient = ctx.createRadialGradient(
          x + cellSize / 2,
          y + cellSize / 2,
          0,
          x + cellSize / 2,
          y + cellSize / 2,
          cellSize / 2
        );
        gradient.addColorStop(0, '#00ffaa');
        gradient.addColorStop(1, '#00cc6a');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.roundRect(x + padding, y + padding, cellSize - padding * 2, cellSize - padding * 2, 6);
        ctx.fill();
        
        // Reset shadow
        ctx.shadowBlur = 0;
        
        // Occhi del serpente
        const eyeSize = cellSize / 6;
        const eyeOffset = cellSize / 4;
        
        ctx.fillStyle = '#0d1117';
        
        // Posizione occhi basata sulla direzione
        let eye1X = x + cellSize / 2;
        let eye1Y = y + eyeOffset;
        let eye2X = x + cellSize / 2;
        let eye2Y = y + eyeOffset;
        
        switch (segment.direction) {
          case 'UP':
            eye1X = x + eyeOffset;
            eye2X = x + cellSize - eyeOffset;
            break;
          case 'DOWN':
            eye1X = x + eyeOffset;
            eye2X = x + cellSize - eyeOffset;
            eye1Y = y + cellSize - eyeOffset;
            eye2Y = y + cellSize - eyeOffset;
            break;
          case 'LEFT':
            eye1X = x + eyeOffset;
            eye2X = x + eyeOffset;
            eye1Y = y + eyeOffset;
            eye2Y = y + cellSize - eyeOffset;
            break;
          case 'RIGHT':
            eye1X = x + cellSize - eyeOffset;
            eye2X = x + cellSize - eyeOffset;
            eye1Y = y + eyeOffset;
            eye2Y = y + cellSize - eyeOffset;
            break;
        }
        
        ctx.beginPath();
        ctx.arc(eye1X, eye1Y, eyeSize, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(eye2X, eye2Y, eyeSize, 0, Math.PI * 2);
        ctx.fill();
        
        // Pupille
        ctx.fillStyle = '#00ff88';
        ctx.beginPath();
        ctx.arc(eye1X, eye1Y, eyeSize / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(eye2X, eye2Y, eyeSize / 2, 0, Math.PI * 2);
        ctx.fill();
        
      } else {
        // Corpo del serpente
        const alpha = 0.7 + (0.3 * (1 - snake.indexOf(segment) / snake.length));
        
        ctx.fillStyle = `rgba(0, 255, 136, ${alpha})`;
        ctx.beginPath();
        ctx.roundRect(x + padding, y + padding, cellSize - padding * 2, cellSize - padding * 2, 4);
        ctx.fill();
        
        // Pattern sul corpo
        ctx.fillStyle = 'rgba(0, 204, 106, 0.5)';
        ctx.beginPath();
        ctx.roundRect(
          x + padding + 2,
          y + padding + 2,
          cellSize - padding * 2 - 4,
          cellSize - padding * 2 - 4,
          3
        );
        ctx.fill();
      }
    },
    [snake]
  );

  /**
   * Disegna il cibo
   */
  const drawFood = useCallback((ctx: CanvasRenderingContext2D, foodItem: Food, cellSize: number) => {
    const x = foodItem.x * cellSize;
    const y = foodItem.y * cellSize;
    const centerX = x + cellSize / 2;
    const centerY = y + cellSize / 2;
    const radius = cellSize / 2 - 2;
    
    // Effetto pulsazione
    const pulse = Math.sin(Date.now() / 200) * 0.1 + 1;
    
    switch (foodItem.type) {
      case 'normal':
        // Cibo normale - mela rossa
        ctx.shadowColor = '#ff4757';
        ctx.shadowBlur = 10;
        
        const normalGradient = ctx.createRadialGradient(
          centerX - 2,
          centerY - 2,
          0,
          centerX,
          centerY,
          radius * pulse
        );
        normalGradient.addColorStop(0, '#ff6b7a');
        normalGradient.addColorStop(1, '#ff4757');
        
        ctx.fillStyle = normalGradient;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * pulse, 0, Math.PI * 2);
        ctx.fill();
        
        // Foglia
        ctx.shadowBlur = 0;
        ctx.fillStyle = '#2ed573';
        ctx.beginPath();
        ctx.ellipse(centerX, centerY - radius * pulse + 2, 3, 5, Math.PI / 4, 0, Math.PI * 2);
        ctx.fill();
        break;
        
      case 'bonus':
        // Cibo bonus - stella dorata
        ctx.shadowColor = '#ffa502';
        ctx.shadowBlur = 15;
        
        ctx.fillStyle = '#ffa502';
        ctx.beginPath();
        
        // Disegna stella
        const spikes = 5;
        const outerRadius = radius * pulse;
        const innerRadius = outerRadius / 2;
        
        for (let i = 0; i < spikes * 2; i++) {
          const r = i % 2 === 0 ? outerRadius : innerRadius;
          const angle = (Math.PI * i) / spikes - Math.PI / 2;
          const px = centerX + Math.cos(angle) * r;
          const py = centerY + Math.sin(angle) * r;
          
          if (i === 0) {
            ctx.moveTo(px, py);
          } else {
            ctx.lineTo(px, py);
          }
        }
        ctx.closePath();
        ctx.fill();
        break;
        
      case 'speed':
        // Power-up velocità
        ctx.shadowColor = '#00ff88';
        ctx.shadowBlur = 12;
        ctx.fillStyle = '#00ff88';
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * pulse, 0, Math.PI * 2);
        ctx.fill();
        
        // Icona fulmine
        ctx.shadowBlur = 0;
        ctx.fillStyle = '#0d1117';
        ctx.font = `${cellSize / 2}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('⚡', centerX, centerY);
        break;
        
      case 'slow':
        // Power-up rallentamento
        ctx.shadowColor = '#7b61ff';
        ctx.shadowBlur = 12;
        ctx.fillStyle = '#7b61ff';
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * pulse, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowBlur = 0;
        ctx.fillStyle = '#0d1117';
        ctx.font = `${cellSize / 2}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('🐌', centerX, centerY);
        break;
        
      case 'shield':
        // Power-up scudo
        ctx.shadowColor = '#3498db';
        ctx.shadowBlur = 12;
        ctx.fillStyle = '#3498db';
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * pulse, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowBlur = 0;
        ctx.fillStyle = '#0d1117';
        ctx.font = `${cellSize / 2}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('🛡️', centerX, centerY);
        break;
    }
    
    ctx.shadowBlur = 0;
  }, []);

  /**
   * Disegna le particelle
   */
  const drawParticles = useCallback((ctx: CanvasRenderingContext2D, particles: Particle[], cellSize: number) => {
    particles.forEach((particle) => {
      const x = particle.x * cellSize + cellSize / 2;
      const y = particle.y * cellSize + cellSize / 2;
      
      ctx.globalAlpha = particle.life;
      ctx.fillStyle = particle.color;
      ctx.shadowColor = particle.color;
      ctx.shadowBlur = 5;
      
      ctx.beginPath();
      ctx.arc(x, y, particle.size * particle.life, 0, Math.PI * 2);
      ctx.fill();
    });
    
    ctx.globalAlpha = 1;
    ctx.shadowBlur = 0;
  }, []);

  /**
   * Funzione di rendering principale
   */
  const render = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const { snake, food, particles, config } = gameStateRef.current;
    const { gridSize, cellSize } = config;
    
    const width = gridSize * cellSize;
    const height = gridSize * cellSize;
    
    // Imposta dimensioni canvas
    canvas.width = width;
    canvas.height = height;
    
    // Pulisci e disegna sfondo
    ctx.clearRect(0, 0, width, height);
    drawBackground(ctx, width, height);
    
    // Disegna cibo
    food.forEach((f) => drawFood(ctx, f, cellSize));
    
    // Disegna serpente
    snake.forEach((segment) => drawSnakeSegment(ctx, segment, cellSize));
    
    // Disegna particelle
    drawParticles(ctx, particles, cellSize);
    
    // Richiedi prossimo frame
    animationRef.current = requestAnimationFrame(render);
  }, [drawBackground, drawFood, drawSnakeSegment, drawParticles]);

  /**
   * Avvia il rendering quando il componente è montato
   */
  useEffect(() => {
    animationRef.current = requestAnimationFrame(render);
    
    return () => {
      if (animationRef.current !== null) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [render]);

  return (
    <canvas
      ref={canvasRef}
      className="game-canvas rounded-xl shadow-2xl"
      style={{
        imageRendering: 'pixelated',
        maxWidth: '100%',
        height: 'auto',
      }}
      aria-label="Area di gioco Snake Ultimate"
      role="img"
    />
  );
};

export default GameCanvas;
