/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Sistema Audio
 * ============================================
 * Gestisce tutti gli effetti sonori e la musica del gioco.
 * Utilizza Web Audio API per generare suoni sintetizzati
 * senza bisogno di file audio esterni.
 */

/**
 * Tipo di effetto sonoro
 */
export type SoundEffect = 'eat' | 'bonus' | 'die' | 'levelup' | 'click' | 'move';

/**
 * Classe per la gestione dell'audio
 */
export class AudioManager {
  private audioContext: AudioContext | null = null;
  private enabled: boolean = true;
  private volume: number = 0.5;

  /**
   * Inizializza l'audio context
   * Deve essere chiamato dopo un'interazione utente (policy browser)
   */
  public init(): void {
    if (this.audioContext) return;
    
    try {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      console.log('[AudioManager] Audio context inizializzato');
    } catch (e) {
      console.warn('[AudioManager] Web Audio API non supportata:', e);
    }
  }

  /**
   * Abilita o disabilita l'audio
   */
  public setEnabled(enabled: boolean): void {
    this.enabled = enabled;
  }

  /**
   * Imposta il volume (0-1)
   */
  public setVolume(volume: number): void {
    this.volume = Math.max(0, Math.min(1, volume));
  }

  /**
   * Riproduce un effetto sonoro
   */
  public playSound(effect: SoundEffect): void {
    if (!this.enabled || !this.audioContext) return;

    // Assicurati che il context sia attivo
    if (this.audioContext.state === 'suspended') {
      this.audioContext.resume();
    }

    const now = this.audioContext.currentTime;
    const oscillator = this.audioContext.createOscillator();
    const gainNode = this.audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(this.audioContext.destination);

    // Configura il suono in base al tipo di effetto
    switch (effect) {
      case 'eat':
        // Suono breve e acuto per il cibo normale
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(523.25, now); // C5
        oscillator.frequency.exponentialRampToValueAtTime(783.99, now + 0.1); // G5
        gainNode.gain.setValueAtTime(this.volume * 0.3, now);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        oscillator.start(now);
        oscillator.stop(now + 0.15);
        break;

      case 'bonus':
        // Suono brillante per il cibo bonus
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(659.25, now); // E5
        oscillator.frequency.setValueAtTime(783.99, now + 0.1); // G5
        oscillator.frequency.setValueAtTime(1046.50, now + 0.2); // C6
        gainNode.gain.setValueAtTime(this.volume * 0.3, now);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        oscillator.start(now);
        oscillator.stop(now + 0.3);
        break;

      case 'die':
        // Suono grave e discendente per la morte
        oscillator.type = 'sawtooth';
        oscillator.frequency.setValueAtTime(300, now);
        oscillator.frequency.exponentialRampToValueAtTime(50, now + 0.5);
        gainNode.gain.setValueAtTime(this.volume * 0.4, now);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        oscillator.start(now);
        oscillator.stop(now + 0.5);
        break;

      case 'levelup':
        // Arpeggio ascendente per il livello
        this.playArpeggio(now, [523.25, 659.25, 783.99, 1046.50]);
        break;

      case 'click':
        // Click breve per i pulsanti
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(800, now);
        gainNode.gain.setValueAtTime(this.volume * 0.2, now);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.05);
        oscillator.start(now);
        oscillator.stop(now + 0.05);
        break;

      case 'move':
        // Suono molto sottile per il movimento
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(200, now);
        gainNode.gain.setValueAtTime(this.volume * 0.05, now);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.03);
        oscillator.start(now);
        oscillator.stop(now + 0.03);
        break;
    }
  }

  /**
   * Riproduce un arpeggio (per level up)
   */
  private playArpeggio(startTime: number, frequencies: number[]): void {
    const noteDuration = 0.1;
    const gap = 0.02;

    frequencies.forEach((freq, index) => {
      const oscillator = this.audioContext!.createOscillator();
      const gainNode = this.audioContext!.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(this.audioContext!.destination);

      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(freq, startTime + index * (noteDuration + gap));

      gainNode.gain.setValueAtTime(this.volume * 0.3, startTime + index * (noteDuration + gap));
      gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + index * (noteDuration + gap) + noteDuration);

      oscillator.start(startTime + index * (noteDuration + gap));
      oscillator.stop(startTime + index * (noteDuration + gap) + noteDuration);
    });
  }
}

// Esporta l'istanza singleton
export const audioManager = new AudioManager();
export default audioManager;
