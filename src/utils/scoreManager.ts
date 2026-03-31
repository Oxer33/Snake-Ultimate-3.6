/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Gestore Punteggi
 * ============================================
 * Gestisce il salvataggio e il recupero dei punteggi
 * utilizzando localStorage per la persistenza.
 * 
 * Funzionalità:
 * - Salvataggio punteggio corrente
 * - Recupero punteggio più alto
 * - Classifica locale (top 10)
 * - Statistiche complessive
 */

import { GameMode, Difficulty, ScoreRecord } from '@/types/game';

/**
 * Chiavi per localStorage
 */
const STORAGE_KEYS = {
  HIGH_SCORE: 'snake-ultimate-highscore',
  SCORES: 'snake-ultimate-scores',
  STATS: 'snake-ultimate-stats',
};

/**
 * Salva il punteggio più alto
 */
export const saveHighScore = (score: number): void => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEYS.HIGH_SCORE, score.toString());
    console.log('[ScoreManager] Nuovo record salvato:', score);
  } catch (e) {
    console.warn('[ScoreManager] Impossibile salvare il record:', e);
  }
};

/**
 * Carica il punteggio più alto
 */
export const loadHighScore = (): number => {
  if (typeof window === 'undefined') return 0;
  try {
    const saved = localStorage.getItem(STORAGE_KEYS.HIGH_SCORE);
    return saved ? parseInt(saved, 10) : 0;
  } catch {
    return 0;
  }
};

/**
 * Salva un record nella classifica
 */
export const saveScore = (record: Omit<ScoreRecord, 'id'>): void => {
  if (typeof window === 'undefined') return;
  try {
    const scores = loadScores();
    
    // Crea nuovo record con ID
    const newRecord: ScoreRecord = {
      ...record,
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    };
    
    // Aggiungi e ordina per punteggio
    scores.push(newRecord);
    scores.sort((a, b) => b.score - a.score);
    
    // Mantieni solo i top 10
    const topScores = scores.slice(0, 10);
    
    localStorage.setItem(STORAGE_KEYS.SCORES, JSON.stringify(topScores));
    console.log('[ScoreManager] Record salvato:', newRecord);
  } catch (e) {
    console.warn('[ScoreManager] Impossibile salvare il record:', e);
  }
};

/**
 * Carica la classifica (top 10)
 */
export const loadScores = (): ScoreRecord[] => {
  if (typeof window === 'undefined') return [];
  try {
    const saved = localStorage.getItem(STORAGE_KEYS.SCORES);
    return saved ? JSON.parse(saved) : [];
  } catch {
    return [];
  }
};

/**
 * Cancella la classifica
 */
export const clearScores = (): void => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.removeItem(STORAGE_KEYS.SCORES);
    console.log('[ScoreManager] Classifica cancellata');
  } catch (e) {
    console.warn('[ScoreManager] Impossibile cancellare la classifica:', e);
  }
};

/**
 * Salva le statistiche complessive
 */
export const saveStats = (stats: Record<string, unknown>): void => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEYS.STATS, JSON.stringify(stats));
  } catch (e) {
    console.warn('[ScoreManager] Impossibile salvare le statistiche:', e);
  }
};

/**
 * Carica le statistiche complessive
 */
export const loadStats = (): Record<string, unknown> => {
  if (typeof window === 'undefined') return {};
  try {
    const saved = localStorage.getItem(STORAGE_KEYS.STATS);
    return saved ? JSON.parse(saved) : {};
  } catch {
    return {};
  }
};

/**
 * Ottiene il numero di partite giocate
 */
export const getGamesPlayed = (): number => {
  const stats = loadStats();
  return (stats.gamesPlayed as number) || 0;
};

/**
 * Incrementa le partite giocate
 */
export const incrementGamesPlayed = (): void => {
  const stats = loadStats();
  stats.gamesPlayed = ((stats.gamesPlayed as number) || 0) + 1;
  saveStats(stats);
};
