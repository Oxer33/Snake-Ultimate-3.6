"""
main.py - File principale del gioco Snake Ultimate 5.1
=======================================================
Questo è il punto di ingresso del gioco. Contiene il game loop principale
che collega tutti i moduli insieme.

Il game loop funziona così:
1. PROCESSA INPUT → Legge tasti e eventi
2. AGGIORNA → Muove il serpente, controlla collisioni, aggiorna effetti
3. DISEGNA → Disegna tutto sullo schermo
4. RIPETI → 60 volte al secondo!

Autore: Snake Ultimate Team
Versione: 5.1
"""

import pygame
import sys
import os
import math

# Aggiungi la cartella del progetto al path per importare i moduli
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import *
from src.snake import Serpente
from src.food import Cibo, GestoreCibo
from src.particles import SistemaParticelle
from src.ui import HUD, GrigliaSfondo
from src.audio import SistemaAudio
from src.score import GestorePunteggi
from src.screens import SchermataMenu, SchermataGameOver, SchermataClassifica, SchermataPausa


class Gioco:
    """
    Classe principale del gioco Snake Ultimate 5.1.
    
    Gestisce:
    - Il game loop (il ciclo principale del gioco)
    - Gli stati del gioco (menu, gioco, pausa, game over, classifica)
    - Il collegamento tra tutti i moduli
    """
    
    def __init__(self):
        """
        Inizializza il gioco.
        Crea la finestra, carica i moduli e imposta lo stato iniziale.
        """
        # Inizializza pygame
        pygame.init()
        print("[DEBUG] Pygame inizializzato")
        
        # Crea la finestra di gioco
        self.schermo = pygame.display.set_mode((SCHERMO_LARGHEZZA, SCHERMO_ALTEZZA))
        pygame.display.set_caption(TITOLO_GIOCO)
        
        # Clock per controllare gli FPS
        self.clock = pygame.time.Clock()
        
        # Prova a caricare l'icona
        self._carica_icona()
        
        # === INIZIALIZZA TUTTI I MODULI ===
        
        # Serpente (il giocatore)
        self.serpente = Serpente()
        print("[DEBUG] Serpente creato")
        
        # Gestore del cibo e power-up
        self.gestore_cibo = GestoreCibo()
        print("[DEBUG] Gestore cibo creato")
        
        # Sistema di particelle (effetti visivi)
        self.sistema_particelle = SistemaParticelle()
        print("[DEBUG] Sistema particelle creato")
        
        # HUD (interfaccia a schermo)
        self.hud = HUD()
        print("[DEBUG] HUD creato")
        
        # Griglia di sfondo
        self.griglia = GrigliaSfondo()
        print("[DEBUG] Griglia sfondo creata")
        
        # Sistema audio
        self.audio = SistemaAudio()
        print("[DEBUG] Sistema audio creato")
        
        # Gestore punteggi
        self.gestore_punteggi = GestorePunteggi()
        print("[DEBUG] Gestore punteggi creato")
        
        # Schermate
        self.schermata_menu = SchermataMenu()
        self.schermata_gameover = SchermataGameOver()
        self.schermata_classifica = SchermataClassifica()
        self.schermata_pausa = SchermataPausa()
        print("[DEBUG] Schermate create")
        
        # === STATO DEL GIOCO ===
        self.stato = STATO_MENU  # Inizia dal menu
        self.punteggio = 0       # Punteggio attuale
        self.livello = 1         # Livello attuale
        self.in_esecuzione = True  # Il gioco sta girando?
        
        # Contatore cibi mangiati per calcolare il livello
        self.cibi_mangiati = 0
        
        print("[DEBUG] Gioco inizializzato completamente!")
        print(f"[DEBUG] Stato iniziale: {self.stato}")
    
    def _carica_icona(self):
        """Prova a caricare l'icona della finestra."""
        try:
            if os.path.exists(PERCORSO_ICONA):
                icona = pygame.image.load(PERCORSO_ICONA)
                # Scala a 64x64 per la finestra
                icona = pygame.transform.smoothscale(icona, (64, 64))
                pygame.display.set_icon(icona)
                print("[DEBUG] Icona caricata da file")
            else:
                # Crea un'icona procedurale se non esiste
                self._crea_icona_procedurale()
        except pygame.error as e:
            print(f"[DEBUG] Errore caricamento icona: {e}")
            self._crea_icona_procedurale()
    
    def _crea_icona_procedurale(self):
        """Crea un'icona procedurale (serpente stilizzato)."""
        dim = 64
        icona_surf = pygame.Surface((dim, dim), pygame.SRCALPHA)
        
        # Sfondo
        icona_surf.fill((10, 10, 30, 255))
        
        # Serpente stilizzato (cerchi verdi)
        for i in range(5):
            x = 10 + i * 10
            y = dim // 2 + int(math.sin(i * 0.8) * 8)
            r = 6 - i
            colore = (0, max(100, 255 - i * 30), 0)
            pygame.draw.circle(icona_surf, colore, (x, y), r)
        
        # Occhio
        pygame.draw.circle(icona_surf, (255, 255, 255), (14, 28), 2)
        
        # Cibo (pallino rosso)
        pygame.draw.circle(icona_surf, (255, 50, 50), (50, 25), 5)
        
        # Bordo
        pygame.draw.rect(icona_surf, NEON_CIANO, (0, 0, dim, dim), 2)
        
        pygame.display.set_icon(icona_surf)
        print("[DEBUG] Icona procedurale creata")
    
    def esegui(self):
        """
        Il game loop principale.
        Continua finché il giocatore non chiude il gioco.
        """
        print("[DEBUG] Game loop avviato!")
        
        while self.in_esecuzione:
            # Calcola il tempo trascorso dall'ultimo frame
            dt = self.clock.tick(FPS) / 1000.0
            
            # Limita dt per evitare salti enormi (es. quando la finestra viene spostata)
            dt = min(dt, 0.1)
            
            # 1. PROCESSA INPUT
            self._processa_input()
            
            # 2. AGGIORNA (in base allo stato del gioco)
            self._aggiorna(dt)
            
            # 3. DISEGNA
            self._disegna()
        
        # Uscita dal gioco
        self._chiudi()
        print("[DEBUG] Gioco chiuso correttamente")
    
    def _processa_input(self):
        """
        Legge tutti gli eventi (tasti premuti, finestra chiusa, ecc.)
        e li gestisce in base allo stato del gioco.
        """
        for evento in pygame.event.get():
            # Sempre: controlla se la finestra viene chiusa
            if evento.type == pygame.QUIT:
                self.in_esecuzione = False
                return
            
            # Gestisci input in base allo stato
            if self.stato == STATO_MENU:
                self._input_menu(evento)
            
            elif self.stato == STATO_GIOCO:
                self._input_gioco(evento)
            
            elif self.stato == STATO_PAUSA:
                self._input_pausa(evento)
            
            elif self.stato == STATO_GAME_OVER:
                self._input_gameover(evento)
            
            elif self.stato == STATO_OPZIONI:
                self._input_classifica(evento)
    
    # === INPUT PER OGNI STATO ===
    
    def _input_menu(self, evento):
        """Gestisce input nel menu principale."""
        azione = self.schermata_menu.gestisci_input(evento)
        
        if azione == "selezione":
            self.audio.riproduci('menu_selezione')
        
        elif azione == "gioca":
            self.audio.riproduci('menu_conferma')
            self._inizia_partita()
        
        elif azione == "classifica":
            self.audio.riproduci('menu_conferma')
            self.schermata_classifica.imposta_classifica(
                self.gestore_punteggi.ottieni_classifica()
            )
            self.stato = STATO_OPZIONI
        
        elif azione == "esci":
            self.in_esecuzione = False
    
    def _input_gioco(self, evento):
        """Gestisce input durante il gioco."""
        if evento.type == pygame.KEYDOWN:
            # Movimento del serpente
            if evento.key in (pygame.K_UP, pygame.K_w):
                self.serpente.imposta_direzione(SU)
            elif evento.key in (pygame.K_DOWN, pygame.K_s):
                self.serpente.imposta_direzione(GIU)
            elif evento.key in (pygame.K_LEFT, pygame.K_a):
                self.serpente.imposta_direzione(SINISTRA)
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.serpente.imposta_direzione(DESTRA)
            
            # Pausa
            elif evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                self.stato = STATO_PAUSA
                self.schermata_pausa.opzione_selezionata = 0
            
            # Muto
            elif evento.key == pygame.K_m:
                muto = self.audio.toggle_muto()
                if muto:
                    self.hud.aggiungi_notifica("Audio OFF", NEON_ROSSO)
                else:
                    self.hud.aggiungi_notifica("Audio ON", NEON_VERDE)
    
    def _input_pausa(self, evento):
        """Gestisce input nella pausa."""
        azione = self.schermata_pausa.gestisci_input(evento)
        
        if azione == "continua":
            self.stato = STATO_GIOCO
        
        elif azione == "menu":
            self.stato = STATO_MENU
        
        elif azione == "esci":
            self.in_esecuzione = False
    
    def _input_gameover(self, evento):
        """Gestisce input nel game over."""
        azione = self.schermata_gameover.gestisci_input(evento)
        
        if azione == "selezione":
            self.audio.riproduci('menu_selezione')
        
        elif azione == "riprova":
            self.audio.riproduci('menu_conferma')
            self._inizia_partita()
        
        elif azione == "menu":
            self.audio.riproduci('menu_conferma')
            self.stato = STATO_MENU
        
        elif azione == "esci":
            self.in_esecuzione = False
    
    def _input_classifica(self, evento):
        """Gestisce input nella classifica."""
        azione = self.schermata_classifica.gestisci_input(evento)
        
        if azione == "indietro":
            self.stato = STATO_MENU
    
    # === LOGICA DI GIOCO ===
    
    def _inizia_partita(self):
        """Inizializza tutto per una nuova partita."""
        self.serpente.reset()
        self.gestore_cibo.reset()
        self.gestore_cibo.spawna_cibo_iniziale()
        self.sistema_particelle.pulisci()
        self.punteggio = 0
        self.livello = 1
        self.cibi_mangiati = 0
        self.stato = STATO_GIOCO
        print("[DEBUG] Nuova partita iniziata!")
    
    def _aggiorna(self, dt):
        """
        Aggiorna la logica del gioco in base allo stato.
        
        Args:
            dt: Tempo trascorso dall'ultimo frame
        """
        if self.stato == STATO_MENU:
            self.schermata_menu.aggiorna(dt)
            self.sistema_particelle.aggiorna(dt)
        
        elif self.stato == STATO_GIOCO:
            self._aggiorna_gioco(dt)
        
        elif self.stato == STATO_PAUSA:
            self.schermata_pausa.aggiorna(dt)
        
        elif self.stato == STATO_GAME_OVER:
            self.schermata_gameover.aggiorna(dt)
            self.sistema_particelle.aggiorna(dt)
        
        elif self.stato == STATO_OPZIONI:
            self.schermata_classifica.aggiorna(dt)
    
    def _aggiorna_gioco(self, dt):
        """
        Aggiorna la logica durante il gioco attivo.
        Qui avviene tutta la magia!
        """
        # Aggiorna il serpente
        self.serpente.aggiorna(dt)
        
        # Aggiorna il cibo
        self.gestore_cibo.aggiorna(dt)
        
        # Aggiorna le particelle
        self.sistema_particelle.aggiorna(dt)
        
        # Aggiorna la griglia
        self.griglia.aggiorna(dt)
        
        # Aggiorna l'HUD
        self.hud.aggiorna(dt, self.punteggio)
        
        # Controlla se il serpente ha mangiato qualcosa
        testa = self.serpente.corpo[0]
        cibo_mangiato = self.gestore_cibo.controlla_collisione(testa)
        
        if cibo_mangiato:
            self._gestisci_cibo_mangiato(cibo_mangiato)
        
        # Controlla collisioni con muri
        if self.serpente.controlla_collisione_muro():
            if self.serpente.scudo_attivo:
                # Lo scudo protegge! Ma si consuma
                self.serpente.scudo_attivo = False
                self.hud.aggiungi_notifica("Scudo distrutto!", NEON_ROSSO)
                self.audio.riproduci('collisione')
                # Rimbalza: rimetti la testa nella posizione precedente
                self.serpente.corpo.pop(0)
                if len(self.serpente.corpo) > 0:
                    self.serpente.corpo.insert(0, self.serpente.corpo[0])
            else:
                self._game_over()
                return
        
        # Controlla collisioni con se stesso
        if self.serpente.controlla_collisione_se_stesso():
            if self.serpente.scudo_attivo:
                self.serpente.scudo_attivo = False
                self.hud.aggiungi_notifica("Scudo distrutto!", NEON_ROSSO)
                self.audio.riproduci('collisione')
            else:
                self._game_over()
                return
    
    def _gestisci_cibo_mangiato(self, cibo):
        """
        Gestisce cosa succede quando il serpente mangia un cibo.
        
        Args:
            cibo: Il cibo che è stato mangiato
        """
        # Posizione in pixel per gli effetti
        px, py = cibo.ottieni_posizione_pixel()
        
        # Calcola punteggio
        moltiplicatore = 2 if self.serpente.moltiplicatore_attivo else 1
        punti = cibo.punteggio * moltiplicatore
        self.punteggio += punti
        
        # Effetti visivi
        if cibo.e_powerup:
            self.sistema_particelle.crea_esplosione_powerup(px, py, cibo.colore)
            self.audio.riproduci('powerup')
        else:
            self.sistema_particelle.crea_esplosione(px, py, cibo.colore)
            if cibo.tipo == Cibo.BONUS:
                self.audio.riproduci('bonus')
            else:
                self.audio.riproduci('mangia')
        
        # Effetti del cibo
        if cibo.tipo == Cibo.NORMALE or cibo.tipo == Cibo.BONUS:
            # Il serpente cresce
            crescita = 1 if cibo.tipo == Cibo.NORMALE else 3
            self.serpente.cresci(crescita)
            self.cibi_mangiati += 1
            
            # Aumenta velocità ogni 5 cibi
            if self.cibi_mangiati % 5 == 0:
                self.serpente.velocita = min(
                    VELOCITA_MAX,
                    self.serpente.velocita + VELOCITA_INCREMENTO * 3
                )
                self.livello += 1
                self.hud.aggiungi_notifica(f"Livello {self.livello}!", NEON_CIANO)
            else:
                # Piccolo incremento di velocità per ogni cibo
                self.serpente.velocita = min(
                    VELOCITA_MAX,
                    self.serpente.velocita + VELOCITA_INCREMENTO
                )
            
            # Notifica bonus
            if cibo.tipo == Cibo.BONUS:
                testo_notifica = f"+{punti} BONUS!"
                self.hud.aggiungi_notifica(testo_notifica, NEON_GIALLO)
        
        # Effetti power-up
        elif cibo.tipo == Cibo.VELOCITA:
            self.serpente.attiva_velocita()
            self.hud.aggiungi_notifica("Boost Velocità!", NEON_CIANO)
            self.audio.riproduci('scudo')
        
        elif cibo.tipo == Cibo.SCUDO:
            self.serpente.attiva_scudo()
            self.hud.aggiungi_notifica("Scudo Attivato!", NEON_MAGENTA)
            self.audio.riproduci('scudo')
        
        elif cibo.tipo == Cibo.MOLTIPLICATORE:
            self.serpente.attiva_moltiplicatore()
            self.hud.aggiungi_notifica("Punti x2!", NEON_ARANCIO)
            self.audio.riproduci('scudo')
        
        elif cibo.tipo == Cibo.RIDUZIONE:
            self.serpente.riduci(3)
            self.hud.aggiungi_notifica("Serpente Ridotto!", NEON_VIOLA)
            self.audio.riproduci('scudo')
        
        # Rimuovi il cibo e spawnane uno nuovo
        self.gestore_cibo.gestisci_mangiato(cibo, self.serpente.corpo)
    
    def _game_over(self):
        """Il serpente è morto! Mostra la schermata game over."""
        self.serpente.vivo = False
        self.stato = STATO_GAME_OVER
        
        # Effetto esplosione sulla testa
        testa_x, testa_y = self.serpente.ottieni_testa_pixel()
        self.sistema_particelle.crea_esplosione_powerup(testa_x, testa_y, NEON_ROSSO)
        
        # Suono game over
        self.audio.riproduci('gameover')
        
        # Controlla se è un nuovo record
        nuovo_record = self.gestore_punteggi.e_nuovo_record(self.punteggio)
        posizione = self.gestore_punteggi.aggiungi_punteggio(self.punteggio)
        
        # Imposta la schermata game over
        self.schermata_gameover.imposta_risultato(
            self.punteggio, nuovo_record, posizione
        )
        
        print(f"[DEBUG] Game Over! Punteggio: {self.punteggio}, Record: {nuovo_record}")
    
    # === DISEGNO ===
    
    def _disegna(self):
        """Disegna tutto sullo schermo in base allo stato."""
        if self.stato == STATO_MENU:
            self._disegna_menu()
        
        elif self.stato == STATO_GIOCO:
            self._disegna_gioco()
        
        elif self.stato == STATO_PAUSA:
            self._disegna_gioco()  # Disegna il gioco sotto
            self.schermata_pausa.disegna(self.schermo)  # Overlay pausa sopra
        
        elif self.stato == STATO_GAME_OVER:
            self._disegna_gameover()
        
        elif self.stato == STATO_OPZIONI:
            self.schermata_classifica.disegna(self.schermo)
        
        # Aggiorna il display (mostra tutto ciò che è stato disegnato)
        pygame.display.flip()
    
    def _disegna_menu(self):
        """Disegna il menu principale con particelle di sfondo."""
        self.schermo.fill(NERO)
        
        # Particelle ambientali nel menu
        self.sistema_particelle.disegna(self.schermo)
        
        # Menu
        self.schermata_menu.disegna(self.schermo)
    
    def _disegna_gioco(self):
        """Disegna tutto il gioco: sfondo, griglia, cibo, serpente, HUD."""
        # Sfondo nero
        self.schermo.fill(GRIGIO_SCURO)
        
        # Griglia di sfondo
        self.griglia.disegna(self.schermo)
        
        # Particelle ambientali (dietro tutto)
        self.sistema_particelle.disegna(self.schermo)
        
        # Cibo
        self.gestore_cibo.disegna(self.schermo)
        
        # Serpente
        self.serpente.disegna(self.schermo, self.sistema_particelle)
        
        # HUD (sopra tutto)
        self.hud.disegna(
            self.schermo, self.punteggio,
            self.gestore_punteggi.ottieni_punteggio_alto(),
            self.serpente, self.livello
        )
    
    def _disegna_gameover(self):
        """Disegna la schermata game over con particelle."""
        # Prima disegna il gioco (sfocato/sotto)
        self._disegna_gioco()
        
        # Poi la schermata game over sopra
        self.schermata_gameover.disegna(self.schermo)
        
        # Particelle
        self.sistema_particelle.disegna(self.schermo)
    
    def _chiudi(self):
        """Chiude il gioco pulitamente."""
        print("[DEBUG] Chiusura gioco in corso...")
        pygame.quit()
        sys.exit()


# === PUNTO DI INGRESSO ===
# Questo codice viene eseguito quando avvii il file main.py direttamente

if __name__ == "__main__":
    print("=" * 50)
    print("  🐍 SNAKE ULTIMATE 5.1 🐍")
    print("  Avvio del gioco...")
    print("=" * 50)
    
    # Crea e avvia il gioco
    gioco = Gioco()
    gioco.esegui()
