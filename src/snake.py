"""
snake.py - Il serpente del gioco
================================
Gestisce tutto ciò che riguarda il serpente:
- Movimento e direzione
- Crescita quando mangia
- Collisioni con muri e se stesso
- Effetti visivi (glow, scia)
- Power-up attivi
"""

import pygame
import math
import random
from src.config import *


class Serpente:
    """
    Rappresenta il serpente del gioco.
    Il serpente è una lista di segmenti (celle della griglia).
    Il primo segmento è la testa, gli altri sono il corpo.
    """
    
    def __init__(self):
        """Inizializza il serpente nella posizione centrale."""
        self.reset()
    
    def reset(self):
        """
        Riporta il serpente allo stato iniziale.
        Chiamato all'inizio di ogni partita.
        """
        # Posizione iniziale: centro dello schermo
        centro_x = GRIGLIA_LARGHEZZA // 2
        centro_y = GRIGLIA_ALTEZZA // 2
        
        # Il serpente parte con 3 segmenti
        self.corpo = [
            (centro_x, centro_y),      # Testa
            (centro_x - 1, centro_y),  # Corpo 1
            (centro_x - 2, centro_y),  # Corpo 2
        ]
        
        # Direzione iniziale: verso destra
        self.direzione = DESTRA
        self.prossima_direzione = DESTRA  # Buffer per evitare inversioni
        
        # Velocità del serpente
        self.velocita = VELOCITA_INIZIALE
        self.timer_movimento = 0.0  # Timer per controllare la velocità
        
        # Flag per la crescita
        self.deve_crescere = False
        self.crescita_rimanente = 0
        
        # Power-up attivi
        self.scudo_attivo = False
        self.scudo_timer = 0.0
        self.moltiplicatore_attivo = False
        self.moltiplicatore_timer = 0.0
        self.velocita_boost_attivo = False
        self.velocita_boost_timer = 0.0
        
        # Animazione
        self.animazione_testa = 0.0  # Per effetto pulsazione
        self.storico_posizioni = []  # Per la scia luminosa
        
        # Stato
        self.vivo = True
    
    def imposta_direzione(self, nuova_direzione):
        """
        Cambia la direzione del serpente.
        Impedisce di fare un 180° (andare nella direzione opposta).
        
        Args:
            nuova_direzione: Tupla (dx, dy) con la nuova direzione
        """
        # Non permettere inversione di marcia
        if nuova_direzione == DIREZIONI_OPPOST.get(self.direzione):
            return
        
        self.prossima_direzione = nuova_direzione
    
    def aggiorna(self, dt):
        """
        Aggiorna il serpente ogni frame.
        
        Args:
            dt: Tempo trascorso dall'ultimo frame in secondi
        """
        if not self.vivo:
            return
        
        # Aggiorna animazione
        self.animazione_testa += dt * 5
        
        # Aggiorna timer power-up
        self._aggiorna_powerup(dt)
        
        # Calcola velocità effettiva
        velocita_effettiva = self.velocita
        if self.velocita_boost_attivo:
            velocita_effettiva *= 1.5
        
        # Timer per il movimento basato sulla velocità
        self.timer_movimento += dt
        intervallo = 1.0 / velocita_effettiva
        
        # Muovi solo quando il timer scatta
        if self.timer_movimento >= intervallo:
            self.timer_movimento -= intervallo
            self._muovi()
    
    def _aggiorna_powerup(self, dt):
        """Aggiorna i timer dei power-up attivi."""
        # Scudo
        if self.scudo_attivo:
            self.scudo_timer -= dt
            if self.scudo_timer <= 0:
                self.scudo_attivo = False
        
        # Moltiplicatore
        if self.moltiplicatore_attivo:
            self.moltiplicatore_timer -= dt
            if self.moltiplicatore_timer <= 0:
                self.moltiplicatore_attivo = False
        
        # Boost velocità
        if self.velocita_boost_attivo:
            self.velocita_boost_timer -= dt
            if self.velocita_boost_timer <= 0:
                self.velocita_boost_attivo = False
    
    def _muovi(self):
        """
        Muove il serpente di una cella nella direzione corrente.
        Se deve crescere, aggiunge un segmento invece di muovere la coda.
        """
        # Applica la direzione programmata
        self.direzione = self.prossima_direzione
        
        # Calcola nuova posizione della testa
        testa_x, testa_y = self.corpo[0]
        dx, dy = self.direzione
        nuova_testa = (testa_x + dx, testa_y + dy)
        
        # Salva posizione nello storico per la scia
        self.storico_posizioni.append(
            (testa_x * CELLA_DIMENSIONE + CELLA_DIMENSIONE // 2,
             testa_y * CELLA_DIMENSIONE + CELLA_DIMENSIONE // 2)
        )
        if len(self.storico_posizioni) > SCIA_LUNGHEZZA * 3:
            self.storico_posizioni.pop(0)
        
        # Inserisci la nuova testa
        self.corpo.insert(0, nuova_testa)
        
        # Se non deve crescere, rimuovi la coda
        if self.crescita_rimanente > 0:
            self.crescita_rimanente -= 1
        else:
            self.corpo.pop()
    
    def cresci(self, quantita=1):
        """
        Fa crescere il serpente di un certo numero di segmenti.
        
        Args:
            quantita: Quanti segmenti aggiungere
        """
        self.crescita_rimanente += quantita
    
    def riduci(self, quantita=3):
        """
        Riduce il serpente (power-up riduzione).
        Non può andare sotto 3 segmenti.
        """
        rimuovi = min(quantita, len(self.corpo) - 3)
        for _ in range(rimuovi):
            if len(self.corpo) > 3:
                self.corpo.pop()
    
    def attiva_scudo(self):
        """Attiva il power-up scudo."""
        self.scudo_attivo = True
        self.scudo_timer = DURATA_SCUDO
    
    def attiva_moltiplicatore(self):
        """Attiva il power-up moltiplicatore punteggio."""
        self.moltiplicatore_attivo = True
        self.moltiplicatore_timer = DURATA_MOLTIPLICATORE
    
    def attiva_velocita(self):
        """Attiva il power-up boost velocità."""
        self.velocita_boost_attivo = True
        self.velocita_boost_timer = DURATA_VELOCITA
    
    def controlla_collisione_muro(self):
        """
        Controlla se il serpente ha sbattuto contro un muro.
        Returns: True se c'è stata una collisione
        """
        testa_x, testa_y = self.corpo[0]
        return (testa_x < 0 or testa_x >= GRIGLIA_LARGHEZZA or
                testa_y < 0 or testa_y >= GRIGLIA_ALTEZZA)
    
    def controlla_collisione_se_stesso(self):
        """
        Controlla se il serpente ha sbattuto contro se stesso.
        Returns: True se c'è stata una collisione
        """
        testa = self.corpo[0]
        return testa in self.corpo[1:]
    
    def ottieni_testa_pixel(self):
        """Ritorna la posizione della testa in pixel (centro della cella)."""
        x, y = self.corpo[0]
        return (x * CELLA_DIMENSIONE + CELLA_DIMENSIONE // 2,
                y * CELLA_DIMENSIONE + CELLA_DIMENSIONE // 2)
    
    def disegna(self, superficie, sistema_particelle):
        """
        Disegna il serpente con effetti glow futuristici.
        
        Args:
            superficie: La superficie su cui disegnare
            sistema_particelle: Per creare le particelle di scia
        """
        if not self.vivo:
            return
        
        # Disegna scia luminosa
        self._disegna_scia(superficie)
        
        # Disegna corpo (dalla coda alla testa)
        for i in range(len(self.corpo) - 1, -1, -1):
            x, y = self.corpo[i]
            px = x * CELLA_DIMENSIONE
            py = y * CELLA_DIMENSIONE
            
            if i == 0:
                # TESTA - più grande e luminosa
                self._disegna_testa(superficie, px, py, sistema_particelle)
            else:
                # CORPO - con gradiente di colore
                self._disegna_segmento_corpo(superficie, px, py, i)
        
        # Disegna effetto scudo se attivo
        if self.scudo_attivo:
            self._disegna_scudo(superficie, sistema_particelle)
    
    def _disegna_scia(self, superficie):
        """Disegna la scia luminosa dietro il serpente."""
        for i, (sx, sy) in enumerate(self.storico_posizioni):
            # Più vecchia = più trasparente e piccola
            rapporto = (i + 1) / len(self.storico_posizioni) if self.storico_posizioni else 1
            alpha = int(80 * rapporto)
            dim = int(CELLA_DIMENSIONE * 0.3 * rapporto)
            
            if dim < 1:
                continue
            
            # Crea superficie glow
            glow_size = dim * 4
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            colore_glow = (*SERPENTE_CORPO_COLORE, alpha)
            pygame.draw.circle(glow_surf, colore_glow, (glow_size, glow_size), glow_size)
            superficie.blit(glow_surf, (sx - glow_size, sy - glow_size))
    
    def _disegna_testa(self, superficie, px, py, sistema_particelle):
        """
        Disegna la testa del serpente con effetto glow pulsante.
        """
        centro_x = px + CELLA_DIMENSIONE // 2
        centro_y = py + CELLA_DIMENSIONE // 2
        
        # Effetto pulsazione
        pulsazione = math.sin(self.animazione_testa) * 2
        dim = CELLA_DIMENSIONE - 2 + int(pulsazione)
        
        # Glow esterno
        glow_dim = dim + 8
        glow_surf = pygame.Surface((glow_dim * 2, glow_dim * 2), pygame.SRCALPHA)
        colore_glow = (*SERPENTE_TESTA_COLORE, 60)
        pygame.draw.circle(glow_surf, colore_glow, (glow_dim, glow_dim), glow_dim)
        superficie.blit(glow_surf, (centro_x - glow_dim, centro_y - glow_dim))
        
        # Corpo testa
        rect = pygame.Rect(centro_x - dim // 2, centro_y - dim // 2, dim, dim)
        pygame.draw.rect(superficie, SERPENTE_TESTA_COLORE, rect, border_radius=8)
        
        # Contorno neon
        pygame.draw.rect(superficie, SERPENTE_CONTORNO, rect, width=2, border_radius=8)
        
        # Occhi
        self._disegna_occhi(superficie, centro_x, centro_y)
        
        # Particelle scia dalla testa
        if random.random() < 0.5:
            sistema_particelle.crea_scia(centro_x, centro_y, SERPENTE_TESTA_COLORE, 0.5)
    
    def _disegna_occhi(self, superficie, cx, cy):
        """Disegna gli occhi del serpente nella direzione del movimento."""
        dx, dy = self.direzione
        offset_x = dx * 4
        offset_y = dy * 4
        
        # Occhio sinistro e destro (perpendicolari alla direzione)
        if dx != 0:  # Movimento orizzontale
            occhio1 = (cx + offset_x, cy - 4)
            occhio2 = (cx + offset_x, cy + 4)
        else:  # Movimento verticale
            occhio1 = (cx - 4, cy + offset_y)
            occhio2 = (cx + 4, cy + offset_y)
        
        # Disegna occhi (bianco con pupilla nera)
        for ex, ey in [occhio1, occhio2]:
            pygame.draw.circle(superficie, BIANCO, (int(ex), int(ey)), 3)
            pygame.draw.circle(superficie, NERO, (int(ex + dx), int(ey + dy)), 1)
    
    def _disegna_segmento_corpo(self, superficie, px, py, indice):
        """
        Disegna un segmento del corpo con gradiente di colore.
        Più vicino alla coda = più scuro.
        """
        # Calcola gradiente (più vicino alla coda = più scuro)
        rapporto = 1.0 - (indice / max(len(self.corpo), 1)) * 0.5
        
        r = int(SERPENTE_CORPO_COLORE[0] * rapporto)
        g = int(SERPENTE_CORPO_COLORE[1] * rapporto)
        b = int(SERPENTE_CORPO_COLORE[2] * rapporto)
        colore = (r, g, b)
        
        centro_x = px + CELLA_DIMENSIONE // 2
        centro_y = py + CELLA_DIMENSIONE // 2
        dim = CELLA_DIMENSIONE - 4
        
        # Glow
        glow_dim = dim + 4
        glow_surf = pygame.Surface((glow_dim * 2, glow_dim * 2), pygame.SRCALPHA)
        colore_glow = (*colore, 30)
        pygame.draw.circle(glow_surf, colore_glow, (glow_dim, glow_dim), glow_dim)
        superficie.blit(glow_surf, (centro_x - glow_dim, centro_y - glow_dim))
        
        # Corpo segmento
        rect = pygame.Rect(px + 2, py + 2, dim, dim)
        pygame.draw.rect(superficie, colore, rect, border_radius=6)
        
        # Contorno sottile
        colore_contorno = (*SERPENTE_CONTORNO[:3],)
        pygame.draw.rect(superficie, colore_contorno, rect, width=1, border_radius=6)
    
    def _disegna_scudo(self, superficie, sistema_particelle):
        """Disegna l'effetto visivo dello scudo attorno al serpente."""
        testa_x, testa_y = self.ottieni_testa_pixel()
        raggio = CELLA_DIMENSIONE * 2
        
        # Cerchio scudo con trasparenza
        scudo_surf = pygame.Surface((raggio * 4, raggio * 4), pygame.SRCALPHA)
        
        # Lampeggiamento basato sul tempo rimanente
        lampeggio = abs(math.sin(self.scudo_timer * 3))
        alpha = int(40 + 30 * lampeggio)
        
        # Cerchio esterno
        colore_scudo = (*NEON_MAGENTA, alpha)
        pygame.draw.circle(scudo_surf, colore_scudo, (raggio * 2, raggio * 2), raggio, 3)
        
        # Cerchio interno
        colore_interno = (*NEON_MAGENTA, alpha // 2)
        pygame.draw.circle(scudo_surf, colore_interno, (raggio * 2, raggio * 2), raggio - 5, 1)
        
        superficie.blit(scudo_surf, (testa_x - raggio * 2, testa_y - raggio * 2))
        
        # Particelle scudo
        if random.random() < 0.3:
            sistema_particelle.crea_effetto_scudo(testa_x, testa_y, raggio)
