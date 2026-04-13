"""
screens.py - Schermate del gioco
=================================
Gestisce tutte le schermate del gioco:
- Menu principale
- Schermata Game Over
- Classifica punteggi
- Schermata di pausa
Ogni schermata ha animazioni e effetti neon futuristici!
"""

import pygame
import math
from src.config import *


class SchermataMenu:
    """
    Il menu principale del gioco.
    Mostra il titolo animato e le opzioni di gioco.
    """
    
    def __init__(self):
        """Inizializza il menu."""
        self.opzioni = ["GIOCA", "CLASSIFICA", "ESCI"]
        self.opzione_selezionata = 0
        self.animazione = 0.0
        self.titolo_offset = 0.0
        
        # Font
        self.font_titolo = pygame.font.SysFont(FONT_NOME, FONT_TITOLARE, bold=True)
        self.font_grande = pygame.font.SysFont(FONT_NOME, FONT_GRANDE, bold=True)
        self.font_opzione = pygame.font.SysFont(FONT_NOME, FONT_MEDIO)
        self.font_piccolo = pygame.font.SysFont(FONT_NOME, FONT_PICCOLO)
    
    def aggiorna(self, dt):
        """Aggiorna le animazioni del menu."""
        self.animazione += dt
        self.titolo_offset = math.sin(self.animazione * 2) * 5
    
    def gestisci_input(self, evento):
        """
        Gestisce gli input del giocatore nel menu.
        
        Args:
            evento: Evento pygame
        
        Returns:
            Nome dell'azione selezionata o None
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                self.opzione_selezionata = (self.opzione_selezionata - 1) % len(self.opzioni)
                return "selezione"
            
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                self.opzione_selezionata = (self.opzione_selezionata + 1) % len(self.opzioni)
                return "selezione"
            
            elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                return self.opzioni[self.opzione_selezionata].lower()
        
        return None
    
    def disegna(self, superficie):
        """Disegna il menu principale."""
        # Sfondo
        superficie.fill(NERO)
        
        # Titolo animato
        self._disegna_titolo(superficie)
        
        # Opzioni menu
        self._disegna_opzioni(superficie)
        
        # Istruzioni
        self._disegna_istruzioni(superficie)
    
    def _disegna_titolo(self, superficie):
        """Disegna il titolo del gioco con effetto glow."""
        # Testo titolo
        testo_titolo = "SNAKE"
        render_titolo = self.font_titolo.render(testo_titolo, True, NEON_VERDE)
        rect_titolo = render_titolo.get_rect(
            centerx=SCHERMO_LARGHEZZA // 2,
            centery=180 + self.titolo_offset
        )
        
        # Glow dietro il titolo
        glow_surf = pygame.Surface(render_titolo.get_size(), pygame.SRCALPHA)
        glow_surf.blit(render_titolo, (0, 0))
        for _ in range(3):
            glow_espanso = pygame.Surface(
                (glow_surf.get_width() + 20, glow_surf.get_height() + 20),
                pygame.SRCALPHA
            )
            glow_espanso.fill((0, 0, 0, 0))
            glow_espanso.blit(glow_surf, (10, 10))
            glow_surf = glow_espanso
        
        superficie.blit(glow_surf, rect_titolo)
        superficie.blit(render_titolo, rect_titolo)
        
        # Sottotitolo
        testo_sub = "ULTIMATE 5.1"
        render_sub = self.font_grande.render(testo_sub, True, NEON_CIANO)
        rect_sub = render_sub.get_rect(
            centerx=SCHERMO_LARGHEZZA // 2,
            centery=250 + self.titolo_offset
        )
        superficie.blit(render_sub, rect_sub)
        
        # Linea decorativa sotto il titolo
        y_linea = 280 + int(self.titolo_offset)
        larghezza_linea = 300 + int(math.sin(self.animazione * 3) * 20)
        pygame.draw.line(superficie, NEON_CIANO,
                        (SCHERMO_LARGHEZZA // 2 - larghezza_linea // 2, y_linea),
                        (SCHERMO_LARGHEZZA // 2 + larghezza_linea // 2, y_linea), 2)
    
    def _disegna_opzioni(self, superficie):
        """Disegna le opzioni del menu con effetto selezione."""
        y_inizio = 350
        
        for i, opzione in enumerate(self.opzioni):
            y = y_inizio + i * 70
            selezionato = (i == self.opzione_selezionata)
            
            if selezionato:
                # Effetto glow sulla selezione
                colore = NEON_CIANO
                
                # Indicatore freccia
                freccia = "► "
                testo_render = self.font_opzione.render(f"{freccia}{opzione}", True, colore)
                
                # Sfondo selezione
                rect = testo_render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y)
                sfondo_rect = rect.inflate(40, 16)
                sfondo_surf = pygame.Surface(sfondo_rect.size, pygame.SRCALPHA)
                pygame.draw.rect(sfondo_surf, (*NEON_CIANO, 30), 
                               sfondo_surf.get_rect(), border_radius=8)
                superficie.blit(sfondo_surf, sfondo_rect)
                
                # Bordo selezione
                pygame.draw.rect(superficie, NEON_CIANO, sfondo_rect, 
                               width=2, border_radius=8)
            else:
                colore = UI_TESTO_SECONDALE
                testo_render = self.font_opzione.render(f"  {opzione}", True, colore)
            
            rect = testo_render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y)
            superficie.blit(testo_render, rect)
    
    def _disegna_istruzioni(self, superficie):
        """Disegna le istruzioni in basso."""
        y = SCHERMO_ALTEZZA - 60
        
        # Istruzioni
        testo = "↑↓ Seleziona  •  INVIO Conferma"
        render = self.font_piccolo.render(testo, True, UI_TESTO_SECONDALE)
        rect = render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y)
        superficie.blit(render, rect)
        
        # Crediti
        testo2 = "WASD o Frecce per muoversi  •  P per Pausa"
        render2 = self.font_piccolo.render(testo2, True, (80, 80, 120))
        rect2 = render2.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y + 25)
        superficie.blit(render2, rect2)


class SchermataGameOver:
    """
    La schermata di Game Over.
    Mostra il punteggio e le opzioni per continuare.
    """
    
    def __init__(self):
        """Inizializza la schermata game over."""
        self.opzioni = ["RIPROVA", "MENU", "ESCI"]
        self.opzione_selezionata = 0
        self.animazione = 0.0
        self.punteggio = 0
        self.nuovo_record = False
        self.posizione_classifica = 0
        
        # Font
        self.font_titolo = pygame.font.SysFont(FONT_NOME, FONT_GRANDE, bold=True)
        self.font_punteggio = pygame.font.SysFont(FONT_NOME, FONT_MEDIO)
        self.font_opzione = pygame.font.SysFont(FONT_NOME, FONT_MEDIO - 4)
        self.font_piccolo = pygame.font.SysFont(FONT_NOME, FONT_PICCOLO)
    
    def imposta_risultato(self, punteggio, nuovo_record=False, posizione=0):
        """
        Imposta il risultato della partita.
        
        Args:
            punteggio: Punteggio ottenuto
            nuovo_record: Se è un nuovo record
            posizione: Posizione in classifica
        """
        self.punteggio = punteggio
        self.nuovo_record = nuovo_record
        self.posizione_classifica = posizione
        self.opzione_selezionata = 0
        self.animazione = 0.0
    
    def aggiorna(self, dt):
        """Aggiorna le animazioni."""
        self.animazione += dt
    
    def gestisci_input(self, evento):
        """Gestisce gli input nella schermata game over."""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                self.opzione_selezionata = (self.opzione_selezionata - 1) % len(self.opzioni)
                return "selezione"
            
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                self.opzione_selezionata = (self.opzione_selezionata + 1) % len(self.opzioni)
                return "selezione"
            
            elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                return self.opzioni[self.opzione_selezionata].lower()
        
        return None
    
    def disegna(self, superficie):
        """Disegna la schermata game over."""
        # Sfondo scuro
        superficie.fill(NERO)
        
        # Effetto vignette (bordi scuri)
        self._disegna_vignette(superficie)
        
        # Titolo GAME OVER
        self._disegna_titolo_gameover(superficie)
        
        # Punteggio
        self._disegna_punteggio(superficie)
        
        # Nuovo record?
        if self.nuovo_record:
            self._disegna_nuovo_record(superficie)
        
        # Opzioni
        self._disegna_opzioni(superficie)
    
    def _disegna_vignette(self, superficie):
        """Disegna un effetto vignette scuro sui bordi."""
        vignette = pygame.Surface((SCHERMO_LARGHEZZA, SCHERMO_ALTEZZA), pygame.SRCALPHA)
        # Bordo superiore
        for y in range(100):
            alpha = int(150 * (1 - y / 100))
            pygame.draw.line(vignette, (0, 0, 0, alpha), (0, y), (SCHERMO_LARGHEZZA, y))
        superficie.blit(vignette, (0, 0))
    
    def _disegna_titolo_gameover(self, superficie):
        """Disegna il titolo GAME OVER con effetto glitch."""
        # Effetto shake/glitch
        shake_x = int(math.sin(self.animazione * 10) * 2) if self.animazione < 0.5 else 0
        shake_y = int(math.cos(self.animazione * 10) * 2) if self.animazione < 0.5 else 0
        
        colore = NEON_ROSSO
        testo = "GAME OVER"
        render = self.font_titolo.render(testo, True, colore)
        rect = render.get_rect(
            centerx=SCHERMO_LARGHEZZA // 2 + shake_x,
            centery=150 + shake_y
        )
        
        # Glow
        glow_surf = pygame.Surface((render.get_width() + 20, render.get_height() + 20), pygame.SRCALPHA)
        glow_testo = self.font_titolo.render(testo, True, (*NEON_ROSSO, 60))
        glow_surf.blit(glow_testo, (10, 10))
        superficie.blit(glow_surf, (rect.x - 10, rect.y - 10))
        
        superficie.blit(render, rect)
    
    def _disegna_punteggio(self, superficie):
        """Disegna il punteggio ottenuto."""
        y = 280
        
        # Etichetta
        testo_label = "PUNTEGGIO"
        render_label = self.font_piccolo.render(testo_label, True, UI_TESTO_SECONDALE)
        rect_label = render_label.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y)
        superficie.blit(render_label, rect_label)
        
        # Numero punteggio grande
        testo_punteggio = str(self.punteggio)
        render_punteggio = self.font_titolo.render(testo_punteggio, True, NEON_VERDE)
        rect_punteggio = render_punteggio.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y + 60)
        
        # Glow punteggio
        glow_surf = pygame.Surface((render_punteggio.get_width() + 30, render_punteggio.get_height() + 20), pygame.SRCALPHA)
        glow_testo = self.font_titolo.render(testo_punteggio, True, (*NEON_VERDE, 40))
        glow_surf.blit(glow_testo, (15, 10))
        superficie.blit(glow_surf, (rect_punteggio.x - 15, rect_punteggio.y - 10))
        
        superficie.blit(render_punteggio, rect_punteggio)
    
    def _disegna_nuovo_record(self, superficie):
        """Disegna l'indicatore di nuovo record lampeggiante."""
        y = 380
        
        # Lampeggio
        alpha = int(abs(math.sin(self.animazione * 4)) * 255)
        
        testo = "★ NUOVO RECORD! ★"
        font = pygame.font.SysFont(FONT_NOME, FONT_MEDIO, bold=True)
        render = font.render(testo, True, NEON_GIALLO)
        
        # Applica alpha
        render.set_alpha(alpha)
        rect = render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y)
        superficie.blit(render, rect)
    
    def _disegna_opzioni(self, superficie):
        """Disegna le opzioni del game over."""
        y_inizio = 450
        
        for i, opzione in enumerate(self.opzioni):
            y = y_inizio + i * 55
            selezionato = (i == self.opzione_selezionata)
            
            if selezionato:
                colore = NEON_CIANO
                testo_render = self.font_opzione.render(f"► {opzione}", True, colore)
                
                # Sfondo selezione
                rect = testo_render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y)
                sfondo_rect = rect.inflate(30, 12)
                sfondo_surf = pygame.Surface(sfondo_rect.size, pygame.SRCALPHA)
                pygame.draw.rect(sfondo_surf, (*NEON_CIANO, 30),
                               sfondo_surf.get_rect(), border_radius=6)
                superficie.blit(sfondo_surf, sfondo_rect)
                pygame.draw.rect(superficie, NEON_CIANO, sfondo_rect,
                               width=1, border_radius=6)
            else:
                colore = UI_TESTO_SECONDALE
                testo_render = self.font_opzione.render(f"  {opzione}", True, colore)
            
            rect = testo_render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y)
            superficie.blit(testo_render, rect)


class SchermataClassifica:
    """
    La schermata della classifica punteggi.
    Mostra i top 10 punteggi con stile futuristico.
    """
    
    def __init__(self):
        """Inizializza la schermata classifica."""
        self.classifica = []
        self.animazione = 0.0
        
        # Font
        self.font_titolo = pygame.font.SysFont(FONT_NOME, FONT_GRANDE, bold=True)
        self.font_voce = pygame.font.SysFont(FONT_NOME, FONT_PICCOLO + 4)
        self.font_piccolo = pygame.font.SysFont(FONT_NOME, FONT_PICCOLO)
    
    def imposta_classifica(self, classifica):
        """Imposta i dati della classifica."""
        self.classifica = classifica
    
    def aggiorna(self, dt):
        """Aggiorna le animazioni."""
        self.animazione += dt
    
    def gestisci_input(self, evento):
        """Gestisce gli input nella classifica."""
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                return "indietro"
        return None
    
    def disegna(self, superficie):
        """Disegna la schermata classifica."""
        superficie.fill(NERO)
        
        # Titolo
        testo = "CLASSIFICA"
        render = self.font_titolo.render(testo, True, NEON_GIALLO)
        rect = render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=60)
        superficie.blit(render, rect)
        
        # Linea sotto il titolo
        pygame.draw.line(superficie, NEON_GIALLO,
                        (SCHERMO_LARGHEZZA // 2 - 150, 90),
                        (SCHERMO_LARGHEZZA // 2 + 150, 90), 2)
        
        if not self.classifica:
            # Nessun punteggio ancora
            testo_vuoto = "Nessun punteggio ancora!"
            render_vuoto = self.font_voce.render(testo_vuoto, True, UI_TESTO_SECONDALE)
            rect_vuoto = render_vuoto.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=300)
            superficie.blit(render_vuoto, rect_vuoto)
        else:
            # Intestazione
            y = 120
            intestazione = f"{'#':<5}{'NOME':<15}{'PUNTEGGIO':<15}{'DATA':<15}"
            render_int = self.font_piccolo.render(intestazione, True, NEON_CIANO)
            superficie.blit(render_int, (80, y))
            
            pygame.draw.line(superficie, (*NEON_CIANO, 100),
                           (80, y + 25), (SCHERMO_LARGHEZZA - 80, y + 25), 1)
            
            # Voci classifica
            for i, (pos, nome, punteggio, data) in enumerate(self.classifica):
                y = 160 + i * 45
                
                # Colore basato sulla posizione
                if pos == 1:
                    colore = NEON_GIALLO  # Oro
                elif pos == 2:
                    colore = (192, 192, 192)  # Argento
                elif pos == 3:
                    colore = (205, 127, 50)  # Bronzo
                else:
                    colore = UI_TESTO_SECONDALE
                
                # Sfondo alternato
                if i % 2 == 0:
                    sfondo = pygame.Surface((SCHERMO_LARGHEZZA - 160, 40), pygame.SRCALPHA)
                    sfondo.fill((*colore, 10))
                    superficie.blit(sfondo, (80, y - 5))
                
                # Testo voce
                testo_voce = f"{pos:<5}{nome:<15}{punteggio:<15}{data:<15}"
                render_voce = self.font_voce.render(testo_voce, True, colore)
                superficie.blit(render_voce, (80, y))
        
        # Istruzioni in basso
        testo_indietro = "Premi ESC o INVIO per tornare"
        render_indietro = self.font_piccolo.render(testo_indietro, True, UI_TESTO_SECONDALE)
        rect_indietro = render_indietro.get_rect(
            centerx=SCHERMO_LARGHEZZA // 2, centery=SCHERMO_ALTEZZA - 40)
        superficie.blit(render_indietro, rect_indietro)


class SchermataPausa:
    """
    La schermata di pausa sovrapposta al gioco.
    Semi-trasparente con effetto blur.
    """
    
    def __init__(self):
        """Inizializza la schermata pausa."""
        self.opzioni = ["CONTINUA", "MENU", "ESCI"]
        self.opzione_selezionata = 0
        self.animazione = 0.0
        
        # Font
        self.font_titolo = pygame.font.SysFont(FONT_NOME, FONT_GRANDE, bold=True)
        self.font_opzione = pygame.font.SysFont(FONT_NOME, FONT_MEDIO - 4)
    
    def aggiorna(self, dt):
        """Aggiorna le animazioni."""
        self.animazione += dt
    
    def gestisci_input(self, evento):
        """Gestisce gli input nella pausa."""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                return "continua"
            
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                self.opzione_selezionata = (self.opzione_selezionata - 1) % len(self.opzioni)
                return "selezione"
            
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                self.opzione_selezionata = (self.opzione_selezionata + 1) % len(self.opzioni)
                return "selezione"
            
            elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                return self.opzioni[self.opzione_selezionata].lower()
        
        return None
    
    def disegna(self, superficie):
        """Disegna la schermata di pausa semi-trasparente."""
        # Overlay scuro
        overlay = pygame.Surface((SCHERMO_LARGHEZZA, SCHERMO_ALTEZZA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        superficie.blit(overlay, (0, 0))
        
        # Titolo PAUSA
        testo = "PAUSA"
        render = self.font_titolo.render(testo, True, NEON_CIANO)
        rect = render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=200)
        
        # Glow
        glow_surf = pygame.Surface((render.get_width() + 20, render.get_height() + 20), pygame.SRCALPHA)
        glow_testo = self.font_titolo.render(testo, True, (*NEON_CIANO, 50))
        glow_surf.blit(glow_testo, (10, 10))
        superficie.blit(glow_surf, (rect.x - 10, rect.y - 10))
        
        superficie.blit(render, rect)
        
        # Opzioni
        y_inizio = 320
        for i, opzione in enumerate(self.opzioni):
            y = y_inizio + i * 60
            selezionato = (i == self.opzione_selezionata)
            
            if selezionato:
                colore = NEON_CIANO
                testo_render = self.font_opzione.render(f"► {opzione}", True, colore)
                
                # Sfondo
                rect_opz = testo_render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y)
                sfondo_rect = rect_opz.inflate(30, 12)
                sfondo_surf = pygame.Surface(sfondo_rect.size, pygame.SRCALPHA)
                pygame.draw.rect(sfondo_surf, (*NEON_CIANO, 40),
                               sfondo_surf.get_rect(), border_radius=6)
                superficie.blit(sfondo_surf, sfondo_rect)
                pygame.draw.rect(superficie, NEON_CIANO, sfondo_rect,
                               width=1, border_radius=6)
            else:
                colore = UI_TESTO_SECONDALE
                testo_render = self.font_opzione.render(f"  {opzione}", True, colore)
            
            rect_opz = testo_render.get_rect(centerx=SCHERMO_LARGHEZZA // 2, centery=y)
            superficie.blit(testo_render, rect_opz)