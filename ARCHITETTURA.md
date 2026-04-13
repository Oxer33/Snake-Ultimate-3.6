# 🐍 Snake Ultimate 5.1 - Architettura del Progetto

## Panoramica
Snake Ultimate 5.1 è un gioco Snake futuristico con effetti neon, particelle, power-up e suoni sintetizzati. Il progetto è scritto in Python usando Pygame.

## Struttura del Progetto

```
Snake Ultimate 5.1/
├── main.py                  # Punto di ingresso - Game loop principale
├── requirements.txt         # Dipendenze Python
├── ARCHITETTURA.md          # Questo file - Documentazione architettura
├── TODO_LIST.md             # Lista cose da fare/tracciamento progressi
├── src/                     # Codice sorgente (pacchetto Python)
│   ├── __init__.py          # Rende src un pacchetto importabile
│   ├── config.py            # Costanti e configurazione centrale
│   ├── snake.py             # Logica del serpente
│   ├── food.py              # Cibo e power-ups
│   ├── particles.py         # Sistema di particelle ed effetti visivi
│   ├── ui.py                # HUD e griglia di sfondo
│   ├── audio.py             # Suoni sintetizzati procedurali
│   ├── score.py             # Salvataggio/caricamento punteggi
│   └── screens.py           # Schermate (menu, game over, pausa, classifica)
├── assets/                  # Risorse statiche
│   └── icons/               # Icone del gioco
└── dati/                    # Dati di gioco (creati automaticamente)
    └── punteggi.json        # Punteggi salvati
```

## Moduli Dettagliati

### `main.py` - Game Loop Principale
- **Classe `Gioco`**: Orchestratore centrale del gioco
- Gestisce gli stati del gioco: MENU → GIOCO → PAUSA → GAME_OVER → CLASSIFICA
- Pattern: State Machine (macchina a stati finiti)
- Game loop: Input → Aggiorna → Disegna → Ripeti (60 FPS)

### `config.py` - Configurazione Centrale
- Tutte le costanti del gioco in un unico posto
- Colori neon, dimensioni schermo, velocità, probabilità
- Facile da modificare per bilanciare il gameplay

### `snake.py` - Il Serpente
- **Classe `Serpente`**: Gestisce movimento, crescita, collisioni
- Sistema di direzione con buffer (evita inversioni)
- Power-up attivi con timer
- Rendering con glow, scia, occhi animati
- Effetto scudo visivo

### `food.py` - Cibo e Power-ups
- **Classe `Cibo`**: Singolo elemento di cibo/power-up
- **Classe `GestoreCibo`**: Spawna e gestisce tutti i cibi
- Tipi: NORMALE, BONUS, VELOCITÀ, SCUDO, MOLTIPLICATORE, RIDUZIONE
- Ogni tipo ha colore, punteggio e simbolo unici
- I power-up scadono dopo 15 secondi

### `particles.py` - Effetti Particellari
- **Classe `Particella`**: Singola particella con fisica
- **Classe `SistemaParticelle`**: Gestisce tutte le particelle
- Scia del serpente, esplosioni cibo, effetto scudo
- Particelle ambientali di sfondo
- Sistema di glow con superfici alpha

### `ui.py` - Interfaccia Utente
- **Classe `HUD`**: Punteggio, record, power-up attivi, notifiche
- **Classe `GrigliaSfondo`**: Griglia "Tron-style" con scanline
- Pannello superiore semi-trasparente
- Barre di progresso per power-up e velocità

### `audio.py` - Audio Sintetizzato
- **Classe `SistemaAudio`**: Genera suoni proceduralmente
- Nessun file audio esterno necessario!
- Forme d'onda: sinusoidale, quadrata, dente di sega, rumore
- Effetti: sweep, envelope ADSR
- Suoni: mangia, bonus, power-up, game over, collisione, menu

### `score.py` - Sistema Punteggi
- **Classe `GestorePunteggi`**: Salva/carica punteggi in JSON
- Top 10 classifica
- Rilevamento nuovo record
- Persistenza su file

### `screens.py` - Schermate
- **`SchermataMenu`**: Menu principale con titolo animato
- **`SchermataGameOver`**: Risultati e opzioni post-partita
- **`SchermataClassifica`**: Top 10 punteggi
- **`SchermataPausa`**: Overlay semi-trasparente

## Flusso di Gioco

```
[AVVIO] → [MENU] → [GIOCO] → [GAME OVER] → [MENU/RIPROVA]
                      ↕
                    [PAUSA]
                    
[MENU] → [CLASSIFICA] → [MENU]
```

## Controlli

| Tasto | Azione |
|-------|--------|
| ↑/W | Muovi su |
| ↓/S | Muovi giù |
| ←/A | Muovi sinistra |
| →/D | Muovi destra |
| P/ESC | Pausa |
| M | Muto audio |
| INVIO/SPAZIO | Conferma selezione |

## Power-ups

| Power-up | Colore | Effetto | Durata |
|----------|--------|---------|--------|
| Velocità | Ciano | +50% velocità | 5s |
| Scudo | Magenta | Immunità collisioni | 8s |
| x2 Punti | Arancio | Punteggio raddoppiato | 10s |
| Riduzione | Viola | Accorcia serpente | Istantaneo |

## Design Futuristico

- **Tema scuro** con colori neon (verde, ciano, magenta)
- **Effetto glow** su tutti gli elementi
- **Particelle** per scia, esplosioni, ambiente
- **Griglia Tron-style** con scanline animata
- **Suoni sintetizzati** per effetto arcade
- **Animazioni fluide** a 60 FPS

## Requisiti

- Python 3.8+
- Pygame 2.5+

## Stato del Progetto

- [x] Architettura base
- [x] Serpente con movimento e crescita
- [x] Cibo e power-ups
- [x] Sistema particelle
- [x] HUD e griglia
- [x] Audio sintetizzato
- [x] Salvataggio punteggi
- [x] Schermate (menu, game over, pausa, classifica)
- [x] Icona procedurale
- [ ] Effetti schermo shake su collisione
- [ ] Modalità difficoltà (facile/medio/difficile)
- [ ] Wall mode (attraversa i muri)
- [ ] Obstacles (ostacoli casuali)
- [ ] Combo system (mangiare cibo in rapida successione)
