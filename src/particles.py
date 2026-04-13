"""
particles.py - Sistema di particelle futuristico
==================================================
Gestisce tutti gli effetti visivi di particelle:
- Scia luminosa del serpente
- Esplosioni quando si mangia il cibo
- Particelle ambientali di sfondo
- Effetti power-up
"""

import pygame
import random
import math
from src.config import *


class Particella:
    """Una singola particella con posizione, velocità, colore e durata."""
    
    def __init__(self, x, y, colore, velocita_x=0, velocita_y=0, 
                 durata=1.0, dimensione=4, decelerazione=0.95):
        """
        Crea una nuova particella.
        
        Args:
            x, y: Posizione iniziale in pixel
            colore: Colore RGB della particella
            velocita_x, velocita_y: Velocità iniziale
            durata: Quanto dura in secondi prima di scomparire
            dimensione: Dimensione iniziale in pixel
            decelerazione: Quanto rallenta (0.95 = rallenta del 5% per frame)
        """
        self.x = x
        self.y = y
        self.colore = colore
        self.velocita_x = velocita_x
        self.velocita_y = velocita_y
        self.durata = durata
        self.durata_max = durata  # Durata iniziale per calcolare l'opacità
        self.dimensione = dimensione
        self.dimensione_max = dimensione
        self.decelerazione = decelerazione
        self.viva = True  # La particella è ancora visibile?
    
    def aggiorna(self, dt):
        """
        Aggiorna la particella ogni frame.
        dt = tempo trascorso dall'ultimo frame in secondi.
        """
        if not self.viva:
            return
        
        # Riduci la durata
        self.durata -= dt
        if self.durata <= 0:
            self.viva = False
            return
        
        # Muovi la particella
        self.x += self.velocita_x * dt * 60
        self.y += self.velocita_y * dt * 60
        
        # Decelera (rallenta gradualmente)
        self.velocita_x *= self.decelerazione
        self.velocita_y *= self.decelerazione
        
        # Riduci dimensione man mano che svanisce
        rapporto = self.durata / self.durata_max
        self.dimensione = self.dimensione_max * rapporto
    
    def disegna(self, superficie):
        """Disegna la particella con effetto glow sullo schermo."""
        if not self.viva or self.dimensione < 0.5:
            return
        
        # Calcola opacità basata sulla durata rimanente
        rapporto = max(0, self.durata / self.durata_max)
        alpha = int(255 * rapporto)
        
        # Crea superficie con trasparenza per il glow
        dim = int(self.dimensione * 3) + 2
        if dim < 2:
            return
        
        glow_surf = pygame.Surface((dim * 2, dim * 2), pygame.SRCALPHA)
        
        # Disegna cerchio glow (sfocato)
        colore_glow = (*self.colore[:3], alpha // 3)
        pygame.draw.circle(glow_surf, colore_glow, (dim, dim), dim)
        
        # Disegna cerchio centrale (più piccolo e luminoso)
        colore_centro = (*self.colore[:3], alpha)
        raggio_centro = max(1, int(self.dimensione))
        pygame.draw.circle(glow_surf, colore_centro, (dim, dim), raggio_centro)
        
        # Blit sulla superficie principale
        superficie.blit(glow_surf, (int(self.x) - dim, int(self.y) - dim))


class SistemaParticelle:
    """
    Gestisce tutte le particelle del gioco.
    È come un "motore" che crea, aggiorna e disegna tutte le particelle.
    """
    
    def __init__(self):
        self.particelle = []  # Lista di tutte le particelle attive
        self.particelle_ambientali = []  # Particelle di sfondo
        self._crea_particelle_ambientali()
    
    def _crea_particelle_ambientali(self):
        """Crea particelle ambientali che fluttuano nello sfondo."""
        for _ in range(50):
            x = random.randint(0, SCHERMO_LARGHEZZA)
            y = random.randint(0, SCHERMO_ALTEZZA)
            colore = random.choice([NEON_CIANO, NEON_BLU, NEON_VIOLA])
            velocita_x = random.uniform(-0.3, 0.3)
            velocita_y = random.uniform(-0.3, 0.3)
            durata = random.uniform(3.0, 8.0)
            dimensione = random.uniform(1, 3)
            
            p = Particella(x, y, colore, velocita_x, velocita_y, 
                          durata, dimensione, 0.99)
            p.durata_max = durata  # Per le ambientali, si riaggiorna
            self.particelle_ambientali.append(p)
    
    def _riaggiorna_ambientale(self, p):
        """Riporta in vita una particella ambientale quando svanisce."""
        p.x = random.randint(0, SCHERMO_LARGHEZZA)
        p.y = random.randint(0, SCHERMO_ALTEZZA)
        p.durata = random.uniform(3.0, 8.0)
        p.durata_max = p.durata
        p.dimensione = random.uniform(1, 3)
        p.dimensione_max = p.dimensione
        p.viva = True
    
    def crea_scia(self, x, y, colore, intensita=1.0):
        """
        Crea particelle di scia dietro il serpente.
        Chiamato ad ogni frame mentre il serpente si muove.
        """
        for _ in range(PARTICELLE_PER_CELLA):
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-5, 5)
            vel_x = random.uniform(-1, 1) * intensita
            vel_y = random.uniform(-1, 1) * intensita
            durata = random.uniform(0.3, 0.8)
            dim = random.uniform(2, 5)
            
            p = Particella(
                x + offset_x, y + offset_y, colore,
                vel_x, vel_y, durata, dim, 0.92
            )
            self.particelle.append(p)
    
    def crea_esplosione(self, x, y, colore, numero=PARTICELLE_ESPLOSIONE):
        """
        Crea un'esplosione di particelle (es. quando si mangia il cibo).
        Le particelle esplodono in tutte le direzioni!
        """
        for _ in range(numero):
            angolo = random.uniform(0, 2 * math.pi)  # Direzione casuale
            velocita = random.uniform(2, 8)  # Velocità casuale
            vel_x = math.cos(angolo) * velocita
            vel_y = math.sin(angolo) * velocita
            durata = random.uniform(0.5, 1.5)
            dim = random.uniform(3, 8)
            
            # Variazione leggera del colore
            r = min(255, colore[0] + random.randint(-30, 30))
            g = min(255, colore[1] + random.randint(-30, 30))
            b = min(255, colore[2] + random.randint(-30, 30))
            colore_variato = (max(0, r), max(0, g), max(0, b))
            
            p = Particella(
                x, y, colore_variato,
                vel_x, vel_y, durata, dim, 0.93
            )
            self.particelle.append(p)
    
    def crea_esplosione_powerup(self, x, y, colore):
        """
        Esplosione speciale per i power-up - più grande e spettacolare!
        """
        # Anello esterno
        for i in range(40):
            angolo = (2 * math.pi / 40) * i
            velocita = random.uniform(3, 10)
            vel_x = math.cos(angolo) * velocita
            vel_y = math.sin(angolo) * velocita
            durata = random.uniform(0.8, 2.0)
            dim = random.uniform(4, 10)
            
            p = Particella(
                x, y, colore,
                vel_x, vel_y, durata, dim, 0.95
            )
            self.particelle.append(p)
        
        # Scintille centrali
        for _ in range(20):
            angolo = random.uniform(0, 2 * math.pi)
            velocita = random.uniform(1, 4)
            vel_x = math.cos(angolo) * velocita
            vel_y = math.sin(angolo) * velocita
            durata = random.uniform(0.3, 1.0)
            dim = random.uniform(2, 5)
            
            p = Particella(
                x, y, BIANCO,
                vel_x, vel_y, durata, dim, 0.90
            )
            self.particelle.append(p)
    
    def crea_effetto_scudo(self, x, y, raggio):
        """
        Crea particelle che formano un cerchio di scudo attorno al serpente.
        """
        for i in range(12):
            angolo = (2 * math.pi / 12) * i + random.uniform(-0.2, 0.2)
            px = x + math.cos(angolo) * raggio
            py = y + math.sin(angolo) * raggio
            vel_x = math.cos(angolo) * 0.5
            vel_y = math.sin(angolo) * 0.5
            
            p = Particella(
                px, py, NEON_MAGENTA,
                vel_x, vel_y, 0.5, 3, 0.90
            )
            self.particelle.append(p)
    
    def aggiorna(self, dt):
        """
        Aggiorna tutte le particelle ogni frame.
        Rimuove quelle morte per non occupare memoria.
        """
        # Aggiorna particelle normali
        for p in self.particelle:
            p.aggiorna(dt)
        
        # Rimuovi particelle morte
        self.particelle = [p for p in self.particelle if p.viva]
        
        # Aggiorna particelle ambientali
        for p in self.particelle_ambientali:
            p.aggiorna(dt)
            if not p.viva:
                self._riaggiorna_ambientale(p)
    
    def disegna(self, superficie):
        """Disegna tutte le particelle sullo schermo."""
        # Prima le ambientali (dietro tutto)
        for p in self.particelle_ambientali:
            p.disegna(superficie)
        
        # Poi le particelle attive (davanti)
        for p in self.particelle:
            p.disegna(superficie)
    
    def pulisci(self):
        """Rimuove tutte le particelle attive (non ambientali)."""
        self.particelle.clear()
