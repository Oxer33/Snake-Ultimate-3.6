"""
config.py - Configurazione centrale del gioco Snake Ultimate 5.1
==============================================================
Questo file contiene TUTTE le costanti e impostazioni del gioco.
Se vuoi cambiare qualcosa (colori, velocità, dimensioni), fallo qui!
"""

import pygame

# === IMPOSTAZIONI FINESTRA ===
SCHERMO_LARGHEZZA = 900  # Larghezza della finestra in pixel
SCHERMO_ALTEZZA = 700   # Altezza della finestra in pixel
FPS = 60                # Fotogrammi al secondo (fluidità del gioco)
TITOLO_GIOCO = "🐍 Snake Ultimate 5.1"

# === GRIGLIA DI GIOCO ===
# La griglia è lo spazio dove si muove il serpente
CELLA_DIMENSIONE = 25   # Dimensione di ogni cella della griglia in pixel
GRIGLIA_LARGHEZZA = SCHERMO_LARGHEZZA // CELLA_DIMENSIONE  # 36 celle
GRIGLIA_ALTEZZA = SCHERMO_ALTEZZA // CELLA_DIMENSIONE      # 28 celle

# === COLORI NEON FUTURISTICI ===
# Formato: (Rosso, Verde, Blu) - valori da 0 a 255
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)
GRIGIO_SCURO = (15, 15, 25)
GRIGIO_MEDIO = (30, 30, 50)

# Colori neon principali
NEON_CIANO = (0, 255, 255)
NEON_MAGENTA = (255, 0, 255)
NEON_VERDE = (57, 255, 20)
NEON_BLU = (0, 150, 255)
NEON_ROSSO = (255, 50, 50)
NEON_GIALLO = (255, 255, 0)
NEON_ARANCIO = (255, 165, 0)
NEON_VIOLA = (180, 0, 255)
NEON_ROSA = (255, 20, 147)

# Colori del serpente
SERPENTE_TESTA_COLORE = NEON_VERDE
SERPENTE_CORPO_COLORE = (0, 200, 100)
SERPENTE_CONTORNO = NEON_CIANO

# Colori del cibo
CIBO_NORMALE_COLORE = NEON_ROSSO
CIBO_BONUS_COLORE = NEON_GIALLO

# Colori power-up
POWERUP_VELOCITA_COLORE = NEON_CIANO
POWERUP_SCUDO_COLORE = NEON_MAGENTA
POWERUP_MOLTIPLICATORE_COLORE = NEON_ARANCIO
POWERUP_RIDUZIONE_COLORE = NEON_VIOLA

# Colori UI
UI_TESTO_COLORE = NEON_CIANO
UI_TESTO_SECONDALE = (150, 150, 200)
UI_SFONDO_PANNELLO = (10, 10, 30, 180)  # Con trasparenza alpha

# === IMPOSTAZIONI GAMEPLAY ===
VELOCITA_INIZIALE = 8      # Celle al secondo all'inizio
VELOCITA_MAX = 20          # Velocità massima raggiungibile
VELOCITA_INCREMENTO = 0.3  # Quanto aumenta la velocità per ogni cibo mangiato
PUNTEGGIO_CIBO = 10        # Punti per cibo normale
PUNTEGGIO_BONUS = 50       # Punti per cibo bonus

# === DURATA POWER-UP (in secondi) ===
DURATA_VELOCITA = 5.0
DURATA_SCUDO = 8.0
DURATA_MOLTIPLICATORE = 10.0

# === PROBABILITÀ SPAWN ===
PROB_CIBO_BONUS = 0.15     # 15% di probabilità per cibo bonus
PROB_POWERUP = 0.08        # 8% di probabilità per power-up

# === EFFETTI VISIVI ===
GLOW_INTENSITA = 2         # Intensità dell'effetto glow (1-5)
PARTICELLE_PER_CELLA = 3   # Particelle generate per cella del serpente
PARTICELLE_ESPLOSIONE = 30 # Particelle per esplosione cibo
GRIGLIA_OPACITA = 40       # Opacità linee griglia (0-255)
SCIA_LUNGHEZZA = 8         # Lunghezza scia luminosa del serpente

# === FONT ===
FONT_NOME = "consolas"     # Font monospace per look futuristico
FONT_PICCOLO = 18
FONT_MEDIO = 28
FONT_GRANDE = 48
FONT_TITOLARE = 72

# === STATI DEL GIOCO ===
# Questi sono i vari "stati" in cui può trovarsi il gioco
STATO_MENU = "menu"
STATO_GIOCO = "gioco"
STATO_PAUSA = "pausa"
STATO_GAME_OVER = "game_over"
STATO_OPZIONI = "opzioni"

# === PERCORSI FILE ===
PERCORSO_PUNTEGGI = "dati/punteggi.json"
PERCORSO_IMPOSTAZIONI = "dati/impostazioni.json"
PERCORSO_ICONA = "assets/icons/icona.png"

# === DIREZIONI ===
SU = (0, -1)
GIU = (0, 1)
SINISTRA = (-1, 0)
DESTRA = (1, 0)
DIREZIONI_OPPOST = {SU: GIU, GIU: SU, SINISTRA: DESTRA, DESTRA: SINISTRA}
