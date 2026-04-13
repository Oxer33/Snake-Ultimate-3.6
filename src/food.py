"""
food.py - Cibo e Power-ups del gioco
=====================================
Gestisce tutto ciò che il serpente può mangiare:
- Cibo normale (rosso) = +10 punti
- Cibo bonus (oro) = +50 punti
- Power-up velocità (ciano) = serpente più veloce
- Power-up scudo (magenta) = immunità alle collisioni
- Power-up moltiplicatore (arancio) = punti x2
- Power-up riduzione (viola) = accorcia il serpente
"""

import pygame
import random
import math
from src.config import *


class Cibo:
    """
    Rappresenta un singolo elemento di cibo o power-up sulla griglia.
    Ogni cibo ha una posizione, un tipo e un'animazione.
    """
    
    # Tipi di cibo disponibili
    NORMALE = "normale"
    BONUS = "bonus"
    VELOCITA = "velocita"
    SCUDO = "scudo"
    MOLTIPLICATORE = "moltiplicatore"
    RIDUZIONE = "riduzione"
    
    # Mappa tipo -> colore
    COLORI = {
        NORMALE: CIBO_NORMALE_COLORE,
        BONUS: CIBO_BONUS_COLORE,
        VELOCITA: POWERUP_VELOCITA_COLORE,
        SCUDO: POWERUP_SCUDO_COLORE,
        MOLTIPLICATORE: POWERUP_MOLTIPLICATORE_COLORE,
        RIDUZIONE: POWERUP_RIDUZIONE_COLORE,
    }
    
    # Mappa tipo -> punteggio
    PUNTEGGI = {
        NORMALE: PUNTEGGIO_CIBO,
        BONUS: PUNTEGGIO_BONUS,
        VELOCITA: 0,
        SCUDO: 0,
        MOLTIPLICATORE: 0,
        RIDUZIONE: 0,
    }
    
    # Mappa tipo -> è un power-up?
    POWERUP = {
        NORMALE: False,
        BONUS: False,
        VELOCITA: True,
        SCUDO: True,
        MOLTIPLICATORE: True,
        RIDUZIONE: True,
    }
    
    def __init__(self, x, y, tipo=NORMALE):
        """
        Crea un nuovo cibo.
        
        Args:
            x, y: Posizione sulla griglia (non in pixel!)
            tipo: Tipo di cibo (NORMALE, BONUS, ecc.)
        """
        self.x = x
        self.y = y
        self.tipo = tipo
        self.colore = self.COLORI[tipo]
        self.punteggio = self.PUNTEGGI[tipo]
        self.e_powerup = self.POWERUP[tipo]
        
        # Animazione
        self.animazione = 0.0  # Contatore per animazione
        self.pulsazione = 0.0  # Effetto pulsazione
        self.rotazione = 0.0   # Rotazione per power-up
        
        # Timer di vita (i power-up scompaiono dopo un po')
        self.tempo_vita = 0.0
        self.durata_max = 15.0 if self.e_powerup else 999.0  # Power-up durano 15 secondi
        self.vivo = True
    
    def ottieni_posizione_pixel(self):
        """Ritorna la posizione in pixel (centro della cella)."""
        return (
            self.x * CELLA_DIMENSIONE + CELLA_DIMENSIONE // 2,
            self.y * CELLA_DIMENSIONE + CELLA_DIMENSIONE // 2
        )
    
    def aggiorna(self, dt):
        """
        Aggiorna l'animazione del cibo ogni frame.
        
        Args:
            dt: Tempo trascorso dall'ultimo frame
        """
        self.animazione += dt * 3
        self.pulsazione = math.sin(self.animazione) * 0.3 + 1.0
        self.rotazione += dt * 2
        
        # Timer di vita per power-up
        self.tempo_vita += dt
        if self.tempo_vita >= self.durata_max:
            self.vivo = False
    
    def disegna(self, superficie):
        """
        Disegna il cibo con effetti glow futuristici.
        """
        if not self.vivo:
            return
        
        cx, cy = self.ottieni_posizione_pixel()
        
        if self.e_powerup:
            self._disegna_powerup(superficie, cx, cy)
        else:
            self._disegna_cibo_normale(superficie, cx, cy)
    
    def _disegna_cibo_normale(self, superficie, cx, cy):
        """Disegna cibo normale o bonus con effetto glow."""
        # Dimensione con pulsazione
        dim_base = CELLA_DIMENSIONE - 6
        dim = int(dim_base * self.pulsazione)
        
        # Glow esterno
        glow_dim = dim + 12
        glow_surf = pygame.Surface((glow_dim * 2, glow_dim * 2), pygame.SRCALPHA)
        colore_glow = (*self.colore, 40)
        pygame.draw.circle(glow_surf, colore_glow, (glow_dim, glow_dim), glow_dim)
        superficie.blit(glow_surf, (cx - glow_dim, cy - glow_dim))
        
        # Corpo del cibo
        if self.tipo == self.BONUS:
            # Cibo bonus: forma a stella/diamante
            self._disegna_diamante(superficie, cx, cy, dim)
        else:
            # Cibo normale: cerchio
            pygame.draw.circle(superficie, self.colore, (cx, cy), dim // 2)
            # Highlight
            highlight = (min(255, self.colore[0] + 80),
                        min(255, self.colore[1] + 80),
                        min(255, self.colore[2] + 80))
            pygame.draw.circle(superficie, highlight, (cx - 2, cy - 2), dim // 4)
    
    def _disegna_diamante(self, superficie, cx, cy, dim):
        """Disegna una forma a diamante per il cibo bonus."""
        meta = dim // 2
        punti = [
            (cx, cy - meta),      # Alto
            (cx + meta, cy),      # Destra
            (cx, cy + meta),      # Basso
            (cx - meta, cy),      # Sinistra
        ]
        pygame.draw.polygon(superficie, self.colore, punti)
        
        # Contorno luminoso
        pygame.draw.polygon(superficie, BIANCO, punti, 2)
        
        # Highlight
        highlight = (min(255, self.colore[0] + 100),
                    min(255, self.colore[1] + 100),
                    min(255, self.colore[2] + 100))
        punti_piccoli = [
            (cx, cy - meta // 2),
            (cx + meta // 2, cy),
            (cx, cy + meta // 2),
            (cx - meta // 2, cy),
        ]
        pygame.draw.polygon(superficie, highlight, punti_piccoli)
    
    def _disegna_powerup(self, superficie, cx, cy):
        """Disegna un power-up con effetto rotazione e glow intenso."""
        # Dimensione con pulsazione
        dim_base = CELLA_DIMENSIONE - 4
        dim = int(dim_base * self.pulsazione)
        
        # Lampeggiamento quando sta per scomparire (ultimi 3 secondi)
        tempo_rimanente = self.durata_max - self.tempo_vita
        if tempo_rimanente < 3.0:
            lampeggio = abs(math.sin(self.animazione * 3))
            if lampeggio < 0.3:
                return  # Nascondi momentaneamente per effetto lampeggio
        
        # Glow esterno grande
        glow_dim = dim + 16
        glow_surf = pygame.Surface((glow_dim * 2, glow_dim * 2), pygame.SRCALPHA)
        colore_glow = (*self.colore, 50)
        pygame.draw.circle(glow_surf, colore_glow, (glow_dim, glow_dim), glow_dim)
        superficie.blit(glow_surf, (cx - glow_dim, cy - glow_dim))
        
        # Glow medio
        glow_medio = dim + 8
        glow_surf2 = pygame.Surface((glow_medio * 2, glow_medio * 2), pygame.SRCALPHA)
        colore_glow2 = (*self.colore, 80)
        pygame.draw.circle(glow_surf2, colore_glow2, (glow_medio, glow_medio), glow_medio)
        superficie.blit(glow_surf2, (cx - glow_medio, cy - glow_medio))
        
        # Forma base (cerchio)
        pygame.draw.circle(superficie, self.colore, (cx, cy), dim // 2)
        
        # Disegna simbolo del power-up
        self._disegna_simbolo_powerup(superficie, cx, cy, dim)
        
        # Anello rotante
        raggio_anello = dim // 2 + 4
        for i in range(4):
            angolo = self.rotazione + (math.pi / 2) * i
            px = cx + math.cos(angolo) * raggio_anello
            py = cy + math.sin(angolo) * raggio_anello
            pygame.draw.circle(superficie, self.colore, (int(px), int(py)), 2)
    
    def _disegna_simbolo_powerup(self, superficie, cx, cy, dim):
        """Disegna il simbolo specifico del tipo di power-up."""
        meta = dim // 3
        
        if self.tipo == self.VELOCITA:
            # Simbolo freccia (velocità)
            punti = [
                (cx + meta, cy),
                (cx - meta // 2, cy - meta),
                (cx - meta // 4, cy),
                (cx - meta // 2, cy + meta),
            ]
            pygame.draw.polygon(superficie, BIANCO, punti)
        
        elif self.tipo == self.SCUDO:
            # Simbolo scudo
            punti = [
                (cx, cy - meta),
                (cx + meta, cy - meta // 2),
                (cx + meta, cy + meta // 2),
                (cx, cy + meta),
                (cx - meta, cy + meta // 2),
                (cx - meta, cy - meta // 2),
            ]
            pygame.draw.polygon(superficie, BIANCO, punti, 2)
        
        elif self.tipo == self.MOLTIPLICATORE:
            # Simbolo "x2"
            font = pygame.font.SysFont(FONT_NOME, FONT_PICCOLO - 4)
            testo = font.render("x2", True, BIANCO)
            rect = testo.get_rect(center=(cx, cy))
            superficie.blit(testo, rect)
        
        elif self.tipo == self.RIDUZIONE:
            # Simbolo freccia giù (riduzione)
            punti = [
                (cx, cy + meta),
                (cx - meta, cy - meta // 3),
                (cx - meta // 3, cy - meta // 3),
                (cx - meta // 3, cy - meta),
                (cx + meta // 3, cy - meta),
                (cx + meta // 3, cy - meta // 3),
                (cx + meta, cy - meta // 3),
            ]
            pygame.draw.polygon(superficie, BIANCO, punti)


class GestoreCibo:
    """
    Gestisce tutti i cibi e power-up presenti nel gioco.
    Si occupa di spawnare nuovi cibi e rimuovere quelli mangiati.
    """
    
    def __init__(self):
        """Inizializza il gestore del cibo."""
        self.cibi = []  # Lista di tutti i cibi attivi
        self.cibo_normale_presente = False  # C'è già un cibo normale?
    
    def reset(self):
        """Ripulisce tutto all'inizio di una nuova partita."""
        self.cibi.clear()
        self.cibo_normale_presente = False
    
    def spawna_cibo_iniziale(self):
        """Spawna il primo cibo all'inizio della partita."""
        self._spawna_cibo_normale()
    
    def _spawna_cibo_normale(self):
        """Spawna un cibo normale in una posizione casuale."""
        pos = self._posizione_casuale()
        if pos:
            cibo = Cibo(pos[0], pos[1], Cibo.NORMALE)
            self.cibi.append(cibo)
            self.cibo_normale_presente = True
    
    def _spawna_cibo_bonus(self):
        """Spawna un cibo bonus in una posizione casuale."""
        pos = self._posizione_casuale()
        if pos:
            cibo = Cibo(pos[0], pos[1], Cibo.BONUS)
            self.cibi.append(cibo)
    
    def _spawna_powerup(self):
        """Spawna un power-up casuale in una posizione casuale."""
        pos = self._posizione_casuale()
        if not pos:
            return
        
        # Scegli tipo casuale
        tipo = random.choice([
            Cibo.VELOCITA, Cibo.SCUDO, 
            Cibo.MOLTIPLICATORE, Cibo.RIDUZIONE
        ])
        cibo = Cibo(pos[0], pos[1], tipo)
        self.cibi.append(cibo)
    
    def _posizione_casuale(self, posizioni_occupate=None):
        """
        Trova una posizione casuale libera sulla griglia.
        Evita le posizioni già occupate dal serpente e da altri cibi.
        
        Returns:
            Tupla (x, y) o None se non trova posizione
        """
        posizioni_occupate_set = set()
        
        # Aggiungi posizioni dei cibi esistenti
        for cibo in self.cibi:
            posizioni_occupate_set.add((cibo.x, cibo.y))
        
        # Se ci vengono passate posizioni occupate (es. corpo del serpente)
        if posizioni_occupate:
            posizioni_occupate_set.update(posizioni_occupate)
        
        # Prova a trovare una posizione libera
        tentativi = 100
        for _ in range(tentativi):
            x = random.randint(1, GRIGLIA_LARGHEZZA - 2)
            y = random.randint(1, GRIGLIA_ALTEZZA - 2)
            if (x, y) not in posizioni_occupate_set:
                return (x, y)
        
        return None
    
    def controlla_collisione(self, testa_serpente):
        """
        Controlla se la testa del serpente ha mangiato un cibo.
        
        Args:
            testa_serpente: Tupla (x, y) della testa del serpente sulla griglia
        
        Returns:
            Il cibo mangiato o None
        """
        for cibo in self.cibi:
            if cibo.x == testa_serpente[0] and cibo.y == testa_serpente[1]:
                return cibo
        return None
    
    def gestisci_mangiato(self, cibo_mangiato, corpo_serpente):
        """
        Gestisce cosa fare dopo che il serpente ha mangiato un cibo.
        Rimuove il cibo e ne spawna uno nuovo se necessario.
        
        Args:
            cibo_mangiato: Il cibo che è stato mangiato
            corpo_serpente: Lista delle posizioni del corpo del serpente
        """
        # Rimuovi il cibo mangiato
        if cibo_mangiato in self.cibi:
            self.cibi.remove(cibo_mangiato)
        
        # Se era cibo normale, spawnane uno nuovo
        if cibo_mangiato.tipo == Cibo.NORMALE:
            self.cibo_normale_presente = False
            self._spawna_cibo_normale()
            
            # Probabilità di spawnare un bonus
            if random.random() < PROB_CIBO_BONUS:
                self._spawna_cibo_bonus()
            
            # Probabilità di spawnare un power-up
            if random.random() < PROB_POWERUP:
                self._spawna_powerup()
    
    def aggiorna(self, dt):
        """
        Aggiorna tutti i cibi ogni frame.
        Rimuove quelli scaduti.
        """
        for cibo in self.cibi:
            cibo.aggiorna(dt)
        
        # Rimuovi cibi scaduti
        cibi_scaduti = [c for c in self.cibi if not c.vivo]
        for cibo in cibi_scaduti:
            if cibo.tipo == Cibo.NORMALE:
                self.cibo_normale_presente = False
            self.cibi.remove(cibo)
        
        # Assicurati che ci sia sempre un cibo normale
        if not self.cibo_normale_presente:
            self._spawna_cibo_normale()
    
    def disegna(self, superficie):
        """Disegna tutti i cibi sullo schermo."""
        for cibo in self.cibi:
            cibo.disegna(superficie)
