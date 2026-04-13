"""
ui.py - Interfaccia Utente e HUD del gioco
===========================================
Gestisce tutto ciò che viene mostrato a schermo:
- Punteggio attuale
- Punteggio alto
- Power-up attivi e timer
- Barra della velocità
- Messaggi di notifica
- Griglia di sfondo
"""

import pygame
import math
from src.config import *


class HUD:
    """
    Heads-Up Display: mostra informazioni di gioco sovrapposte allo schermo.
    Come il cruscotto di un'auto, ma per il serpente!
    """
    
    def __init__(self):
        """Inizializza l'HUD."""
        self.font_piccolo = pygame.font.SysFont(FONT_NOME, FONT_PICCOLO)
        self.font_medio = pygame.font.SysFont(FONT_NOME, FONT_MEDIO)
        self.font_grande = pygame.font.SysFont(FONT_NOME, FONT_GRANDE)
        
        # Notifiche temporanee
        self.notifiche = []  # Lista di (testo, colore, timer)
        
        # Animazione punteggio
        self.punteggio_animazione = 0.0
        self.punteggio_precedente = 0
    
    def aggiungi_notifica(self, testo, colore=NEON_CIANO, durata=2.0):
        """
        Aggiunge una notifica temporanea a schermo.
        Es: "Power-up Scudo attivato!"
        
        Args:
            testo: Il messaggio da mostrare
            colore: Colore del testo
            durata: Quanto dura in secondi
        """
        self.notifiche.append([testo, colore, durata])
    
    def aggiorna(self, dt, punteggio):
        """
        Aggiorna l'HUD ogni frame.
        
        Args:
            dt: Tempo trascorso dall'ultimo frame
            punteggio: Punteggio attuale del giocatore
        """
        self.punteggio_animazione += dt * 3
        
        # Controlla se il punteggio è cambiato
        if punteggio != self.punteggio_precedente:
            self.punteggio_animazione = 0.0
            self.punteggio_precedente = punteggio
        
        # Aggiorna notifiche
        notifiche_rimaste = []
        for notifica in self.notifiche:
            notifica[2] -= dt  # Riduci timer
            if notifica[2] > 0:
                notifiche_rimaste.append(notifica)
        self.notifiche = notifiche_rimaste
    
    def disegna(self, superficie, punteggio, punteggio_alto, serpente, livello):
        """
        Disegna tutto l'HUD sullo schermo.
        
        Args:
            superficie: Dove disegnare
            punteggio: Punteggio attuale
            punteggio_alto: Punteggio record
            serpente: Oggetto serpente per info power-up
            livello: Livello attuale
        """
        # Pannello semi-trasparente in alto
        self._disegna_pannello_superiore(superficie)
        
        # Punteggio
        self._disegna_punteggio(superficie, punteggio)
        
        # Punteggio alto
        self._disegna_punteggio_alto(superficie, punteggio_alto)
        
        # Livello e velocità
        self._disegna_info_gioco(superficie, serpente, livello)
        
        # Power-up attivi
        self._disegna_powerup_attivi(superficie, serpente)
        
        # Notifiche
        self._disegna_notifiche(superficie)
    
    def _disegna_pannello_superiore(self, superficie):
        """Disegna il pannello semi-trasparente in alto."""
        pannello = pygame.Surface((SCHERMO_LARGHEZZA, 50), pygame.SRCALPHA)
        pannello.fill((10, 10, 30, 180))
        superficie.blit(pannello, (0, 0))
        
        # Linea neon sotto il pannello
        pygame.draw.line(superficie, NEON_CIANO, (0, 50), (SCHERMO_LARGHEZZA, 50), 1)
    
    def _disegna_punteggio(self, superficie, punteggio):
        """Disegna il punteggio attuale con effetto glow."""
        # Effetto scala quando il punteggio cambia
        scala = 1.0 + max(0, 0.2 - self.punteggio_animazione) * 2
        
        testo = f"PUNTEGGIO: {punteggio}"
        font_size = int(FONT_MEDIO * scala)
        font = pygame.font.SysFont(FONT_NOME, font_size)
        
        # Glow
        testo_glow = font.render(testo, True, NEON_VERDE)
        glow_surf = pygame.Surface(testo_glow.get_size(), pygame.SRCALPHA)
        glow_surf.fill((0, 0, 0, 0))
        glow_surf.blit(testo_glow, (0, 0))
        
        # Testo principale
        testo_render = font.render(testo, True, NEON_VERDE)
        rect = testo_render.get_rect(topleft=(20, 10))
        
        # Glow dietro
        glow_rect = rect.inflate(10, 6)
        glow_bg = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        colore_glow = (*NEON_VERDE, 30)
        pygame.draw.rect(glow_bg, colore_glow, glow_bg.get_rect(), border_radius=4)
        superficie.blit(glow_bg, glow_rect)
        
        superficie.blit(testo_render, rect)
    
    def _disegna_punteggio_alto(self, superficie, punteggio_alto):
        """Disegna il punteggio record."""
        testo = f"RECORD: {punteggio_alto}"
        testo_render = self.font_piccolo.render(testo, True, NEON_GIALLO)
        rect = testo_render.get_rect(topright=(SCHERMO_LARGHEZZA - 20, 15))
        superficie.blit(testo_render, rect)
    
    def _disegna_info_gioco(self, superficie, serpente, livello):
        """Disegna informazioni di gioco (livello, velocità, lunghezza)."""
        # Posizione in basso a sinistra
        y_base = SCHERMO_ALTEZZA - 30
        
        # Pannello semi-trasparente
        pannello = pygame.Surface((300, 30), pygame.SRCALPHA)
        pannello.fill((10, 10, 30, 150))
        superficie.blit(pannello, (0, y_base))
        
        # Livello
        testo_livello = f"LIV.{livello}"
        render_livello = self.font_piccolo.render(testo_livello, True, NEON_CIANO)
        superficie.blit(render_livello, (10, y_base + 5))
        
        # Lunghezza serpente
        testo_lunghezza = f"LEN:{len(serpente.corpo)}"
        render_lunghezza = self.font_piccolo.render(testo_lunghezza, True, NEON_VERDE)
        superficie.blit(render_lunghezza, (100, y_base + 5))
        
        # Barra velocità
        velocita_norm = min(1.0, (serpente.velocita - VELOCITA_INIZIALE) / 
                          (VELOCITA_MAX - VELOCITA_INIZIALE))
        barra_x = 200
        barra_lunghezza = 80
        barra_altezza = 12
        
        # Sfondo barra
        pygame.draw.rect(superficie, GRIGIO_MEDIO, 
                        (barra_x, y_base + 9, barra_lunghezza, barra_altezza), 
                        border_radius=3)
        
        # Barra riempita
        riempimento = int(barra_lunghezza * velocita_norm)
        colore_vel = NEON_CIANO if not serpente.velocita_boost_attivo else NEON_GIALLO
        if riempimento > 0:
            pygame.draw.rect(superficie, colore_vel,
                            (barra_x, y_base + 9, riempimento, barra_altezza),
                            border_radius=3)
        
        # Contorno
        pygame.draw.rect(superficie, NEON_CIANO,
                        (barra_x, y_base + 9, barra_lunghezza, barra_altezza),
                        width=1, border_radius=3)
        
        # Etichetta
        testo_vel = "SPD"
        render_vel = self.font_piccolo.render(testo_vel, True, NEON_CIANO)
        superficie.blit(render_vel, (barra_x - 30, y_base + 5))
    
    def _disegna_powerup_attivi(self, superficie, serpente):
        """Disegna indicatori dei power-up attivi."""
        x_base = SCHERMO_LARGHEZZA - 200
        y_base = 60
        
        powerups = []
        
        if serpente.scudo_attivo:
            powerups.append(("SCUDO", NEON_MAGENTA, serpente.scudo_timer, DURATA_SCUDO))
        
        if serpente.moltiplicatore_attivo:
            powerups.append(("x2", NEON_ARANCIO, serpente.moltiplicatore_timer, DURATA_MOLTIPLICATORE))
        
        if serpente.velocita_boost_attivo:
            powerups.append(("BOOST", NEON_CIANO, serpente.velocita_boost_timer, DURATA_VELOCITA))
        
        for i, (nome, colore, timer, durata) in enumerate(powerups):
            y = y_base + i * 30
            
            # Sfondo
            pannello = pygame.Surface((180, 25), pygame.SRCALPHA)
            pannello.fill((*colore, 30))
            superficie.blit(pannello, (x_base, y))
            
            # Nome power-up
            testo = self.font_piccolo.render(nome, True, colore)
            superficie.blit(testo, (x_base + 5, y + 3))
            
            # Barra timer
            rapporto = timer / durata
            barra_x = x_base + 60
            barra_lunghezza = 110
            barra_altezza = 10
            
            # Sfondo barra
            pygame.draw.rect(superficie, GRIGIO_SCURO,
                            (barra_x, y + 7, barra_lunghezza, barra_altezza),
                            border_radius=3)
            
            # Barra riempita
            riempimento = int(barra_lunghezza * rapporto)
            if riempimento > 0:
                pygame.draw.rect(superficie, colore,
                                (barra_x, y + 7, riempimento, barra_altezza),
                                border_radius=3)
            
            # Contorno
            pygame.draw.rect(superficie, colore,
                            (barra_x, y + 7, barra_lunghezza, barra_altezza),
                            width=1, border_radius=3)
    
    def _disegna_notifiche(self, superficie):
        """Disegna le notifiche temporanee al centro dello schermo."""
        for i, (testo, colore, timer) in enumerate(self.notifiche):
            # Fade in/out
            if timer > 1.5:
                alpha = int(255 * (2.0 - timer) / 0.5)
            elif timer < 0.5:
                alpha = int(255 * timer / 0.5)
            else:
                alpha = 255
            
            alpha = max(0, min(255, alpha))
            
            font = pygame.font.SysFont(FONT_NOME, FONT_MEDIO)
            testo_render = font.render(testo, True, colore)
            
            # Posizione centrata, leggermente spostata per ogni notifica
            y = SCHERMO_ALTEZZA // 2 - 50 + i * 40
            
            # Glow dietro
            glow_rect = testo_render.get_rect(center=(SCHERMO_LARGHEZZA // 2, y))
            glow_rect.inflate_ip(20, 10)
            glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            colore_glow = (*colore, alpha // 4)
            pygame.draw.rect(glow_surf, colore_glow, glow_surf.get_rect(), border_radius=8)
            superficie.blit(glow_surf, glow_rect)
            
            # Testo con alpha
            testo_surf = pygame.Surface(testo_render.get_size(), pygame.SRCALPHA)
            testo_surf.blit(testo_render, (0, 0))
            testo_surf.set_alpha(alpha)
            
            rect = testo_render.get_rect(center=(SCHERMO_LARGHEZZA // 2, y))
            superficie.blit(testo_surf, rect)


class GrigliaSfondo:
    """
    Disegna la griglia di sfondo futuristica.
    Crea l'effetto "Tron" con linee sottili neon.
    """
    
    def __init__(self):
        """Pre-renderizza la griglia per performance."""
        self.superficie_griglia = pygame.Surface(
            (SCHERMO_LARGHEZZA, SCHERMO_ALTEZZA), pygame.SRCALPHA
        )
        self._pre_renderizza()
        
        # Animazione "scanline" orizzontale
        self.scanline_y = 0
        self.scanline_velocita = 100  # pixel al secondo
    
    def _pre_renderizza(self):
        """Pre-disegna la griglia statica (non cambia ogni frame)."""
        self.superficie_griglia.fill((0, 0, 0, 0))
        
        colore_linea = (30, 30, 60, GRIGLIA_OPACITA)
        
        # Linee verticali
        for x in range(0, SCHERMO_LARGHEZZA, CELLA_DIMENSIONE):
            pygame.draw.line(self.superficie_griglia, colore_linea, 
                           (x, 0), (x, SCHERMO_ALTEZZA))
        
        # Linee orizzontali
        for y in range(0, SCHERMO_ALTEZZA, CELLA_DIMENSIONE):
            pygame.draw.line(self.superficie_griglia, colore_linea,
                           (0, y), (SCHERMO_LARGHEZZA, y))
        
        # Bordo griglia (più luminoso)
        colore_bordo = (*NEON_CIANO, 80)
        pygame.draw.rect(self.superficie_griglia, colore_bordo,
                        (0, 0, SCHERMO_LARGHEZZA, SCHERMO_ALTEZZA), 2)
    
    def aggiorna(self, dt):
        """Aggiorna l'animazione della scanline."""
        self.scanline_y += self.scanline_velocita * dt
        if self.scanline_y > SCHERMO_ALTEZZA:
            self.scanline_y = 0
    
    def disegna(self, superficie):
        """
        Disegna la griglia di sfondo con effetto scanline.
        """
        # Griglia statica
        superficie.blit(self.superficie_griglia, (0, 0))
        
        # Scanline animata (linea luminosa che scorre)
        scanline_surf = pygame.Surface((SCHERMO_LARGHEZZA, 2), pygame.SRCALPHA)
        scanline_surf.fill((*NEON_CIANO, 20))
        superficie.blit(scanline_surf, (0, int(self.scanline_y)))
