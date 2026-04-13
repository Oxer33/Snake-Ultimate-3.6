"""
audio.py - Sistema audio del gioco
==================================
Gestisce tutti gli effetti sonori e la musica.
Usa pygame.mixer per generare suoni sintetizzati (nessun file esterno necessario!)
Questo approccio è fantastico perché non servono file audio esterni.
"""

import pygame
import math
import struct
import io
from src.config import *


class SistemaAudio:
    """
    Gestisce tutto l'audio del gioco.
    Genera suoni proceduralmente (senza file esterni) per un effetto futuristico!
    """
    
    def __init__(self):
        """Inizializza il sistema audio."""
        self.inizializzato = False
        self.muto = False
        self.volume = 0.5  # Volume da 0.0 a 1.0
        
        # Suoni generati
        self.suoni = {}
        
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.inizializzato = True
            self._genera_suoni()
            print("[DEBUG] Sistema audio inizializzato con successo")
        except pygame.error as e:
            print(f"[DEBUG] Errore inizializzazione audio: {e}")
            self.inizializzato = False
    
    def _genera_suoni(self):
        """Genera tutti i suoni del gioco proceduralmente."""
        if not self.inizializzato:
            return
        
        # Suono mangia cibo - beep corto ascendente
        self.suoni['mangia'] = self._genera_suono(
            frequenza_inizio=440, frequenza_fine=880,
            durata=0.1, tipo='sinusoidale', volume=0.3
        )
        
        # Suono mangia bonus - arpeggio felice
        self.suoni['bonus'] = self._genera_suono(
            frequenza_inizio=523, frequenza_fine=1047,
            durata=0.2, tipo='sinusoidale', volume=0.4
        )
        
        # Suono power-up - sweep ascendente
        self.suoni['powerup'] = self._genera_suono(
            frequenza_inizio=330, frequenza_fine=1320,
            durata=0.3, tipo='sinusoidale', volume=0.35
        )
        
        # Suono game over - discendente drammatico
        self.suoni['gameover'] = self._genera_suono(
            frequenza_inizio=440, frequenza_fine=110,
            durata=0.8, tipo='sinusoidale', volume=0.4
        )
        
        # Suono scudo attivato - blip
        self.suoni['scudo'] = self._genera_suono(
            frequenza_inizio=660, frequenza_fine=660,
            durata=0.15, tipo='quadrata', volume=0.25
        )
        
        # Suono muro colpito - rumore
        self.suoni['collisione'] = self._genera_suono(
            frequenza_inizio=200, frequenza_fine=50,
            durata=0.3, tipo='dente_sega', volume=0.35
        )
        
        # Suono menu - click soft
        self.suoni['menu_selezione'] = self._genera_suono(
            frequenza_inizio=550, frequenza_fine=550,
            durata=0.08, tipo='sinusoidale', volume=0.2
        )
        
        # Suono menu conferma - doppio blip
        self.suoni['menu_conferma'] = self._genera_suono(
            frequenza_inizio=440, frequenza_fine=880,
            durata=0.15, tipo='sinusoidale', volume=0.3
        )
        
        print(f"[DEBUG] Generati {len(self.suoni)} suoni procedurali")
    
    def _genera_suono(self, frequenza_inizio, frequenza_fine, durata, 
                      tipo='sinusoidale', volume=0.5):
        """
        Genera un suono proceduralmente usando forme d'onda.
        
        Args:
            frequenza_inizio: Frequenza iniziale in Hz
            frequenza_fine: Frequenza finale in Hz (per effetti sweep)
            durata: Durata in secondi
            tipo: Tipo di onda ('sinusoidale', 'quadrata', 'dente_sega', 'rumore')
            volume: Volume da 0.0 a 1.0
        
        Returns:
            pygame.mixer.Sound object
        """
        sample_rate = 44100
        num_campioni = int(sample_rate * durata)
        
        # Buffer per i campioni audio (stereo: 2 canali)
        campioni = []
        
        for i in range(num_campioni):
            t = i / sample_rate  # Tempo in secondi
            progresso = i / num_campioni  # Progresso 0-1
            
            # Interpola frequenza (sweep)
            frequenza = frequenza_inizio + (frequenza_fine - frequenza_inizio) * progresso
            
            # Genera forma d'onda
            if tipo == 'sinusoidale':
                valore = math.sin(2 * math.pi * frequenza * t)
            elif tipo == 'quadrata':
                valore = 1.0 if math.sin(2 * math.pi * frequenza * t) >= 0 else -1.0
            elif tipo == 'dente_sega':
                valore = 2.0 * (frequenza * t % 1.0) - 1.0
            elif tipo == 'rumore':
                import random
                valore = random.uniform(-1.0, 1.0)
            else:
                valore = math.sin(2 * math.pi * frequenza * t)
            
            # Envelope ADSR (Attack-Decay-Sustain-Release)
            envelope = 1.0
            attack = 0.01  # 10ms attack
            release = 0.05  # 50ms release
            
            if t < attack:
                envelope = t / attack
            elif t > durata - release:
                envelope = (durata - t) / release
            
            valore *= envelope
            
            # Applica volume
            valore *= volume * self.volume
            
            # Clamp
            valore = max(-1.0, min(1.0, valore))
            
            # Converti a 16-bit signed integer (stereo)
            campione = int(valore * 32767)
            campioni.append(campione)   # Canale sinistro
            campioni.append(campione)   # Canale destro
        
        # Crea buffer bytes
        buffer = struct.pack(f'{len(campioni)}h', *campioni)
        
        # Crea oggetto Sound di pygame
        suono = pygame.mixer.Sound(buffer=buffer)
        return suono
    
    def riproduci(self, nome_suono):
        """
        Riproduce un suono per nome.
        
        Args:
            nome_suono: Nome del suono ('mangia', 'bonus', ecc.)
        """
        if not self.inizializzato or self.muto:
            return
        
        if nome_suono in self.suoni:
            try:
                self.suoni[nome_suono].play()
            except pygame.error as e:
                print(f"[DEBUG] Errore riproduzione suono {nome_suono}: {e}")
    
    def imposta_volume(self, volume):
        """
        Imposta il volume generale.
        
        Args:
            volume: Volume da 0.0 a 1.0
        """
        self.volume = max(0.0, min(1.0, volume))
        # Rigenera suoni con il nuovo volume
        if self.inizializzato:
            self._genera_suoni()
    
    def toggle_muto(self):
        """Attiva/disattiva il muto. Ritorna il nuovo stato."""
        self.muto = not self.muto
        return self.muto
    
    def stop_tutto(self):
        """Ferma tutti i suoni in riproduzione."""
        if self.inizializzato:
            pygame.mixer.stop()