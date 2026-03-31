# 🏗️ ARCHITETTURA - Snake Ultimate 3.6

## Panoramica del Progetto

Snake Ultimate 3.6 è un gioco Snake moderno costruito con Next.js 15, React 19 e TypeScript. Il progetto segue un'architettura modulare e component-based per garantire manutenibilità e scalabilità.

## Stack Tecnologico

| Tecnologia | Versione | Scopo |
|------------|----------|-------|
| Next.js | 15.1+ | Framework React (App Router) |
| React | 19+ | Libreria UI |
| TypeScript | 5.7+ | Type safety |
| TailwindCSS | 3.4+ | Styling utility-first |
| Zustand | 5.0+ | State management |
| Canvas API | Native | Rendering grafico |

## Struttura del Progetto

```
Snake Ultimate 3.6/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── globals.css         # Stili globali e animazioni CSS
│   │   ├── layout.tsx          # Layout root (metadata, viewport)
│   │   └── page.tsx            # Pagina principale
│   │
│   ├── components/             # Componenti React
│   │   ├── game/               # Componenti di gioco
│   │   │   ├── GameCanvas.tsx  # Rendering Canvas del gioco
│   │   │   └── GameContainer.tsx # Componente principale integratore
│   │   └── ui/                 # Componenti UI riutilizzabili
│   │       ├── TouchControls.tsx  # Controlli touch per mobile
│   │       ├── ScoreDisplay.tsx   # Display punteggio/stats
│   │       ├── MainMenu.tsx       # Menu principale
│   │       └── GameOver.tsx       # Schermata Game Over
│   │
│   ├── store/                  # State management
│   │   └── gameStore.ts        # Store Zustand per stato globale
│   │
│   ├── types/                  # Definizioni TypeScript
│   │   └── game.ts             # Interfacce e tipi del gioco
│   │
│   ├── utils/                  # Utility e logica
│   │   └── gameEngine.ts       # Motore di gioco principale
│   │
│   └── assets/                 # Risorse statiche (immagini, suoni)
│
├── public/                     # File statici pubblici
├── package.json                # Dipendenze e scripts
├── tsconfig.json               # Configurazione TypeScript
├── next.config.ts              # Configurazione Next.js
├── tailwind.config.ts          # Configurazione TailwindCSS
└── postcss.config.mjs          # Configurazione PostCSS
```

## Architettura dei Componenti

### Flusso di Rendering

```
page.tsx
  └── GameContainer.tsx
        ├── MainMenu.tsx (stato: menu)
        ├── GameCanvas.tsx (stato: playing)
        │     └── Rendering su Canvas 2D
        ├── ScoreDisplay.tsx (HUD punteggio)
        ├── TouchControls.tsx (controlli mobile)
        └── GameOver.tsx (stato: gameover)
```

### Flusso dei Dati

```
gameEngine.ts (logica core)
  └── Callbacks → gameStore.ts (Zustand store)
        └── State updates → Componenti React (re-render)
              └── Input utente → gameEngine.ts (cambio direzione)
```

## Motore di Gioco (gameEngine.ts)

Il motore di gioco è una classe singleton che gestisce:

- **Game Loop**: Utilizza `requestAnimationFrame` con accumulatore per aggiornamenti a tick fisso
- **Movimento Serpente**: Calcola la nuova posizione della testa e aggiorna i segmenti
- **Collisioni**: Rileva collisioni con se stesso e con i bordi
- **Cibo**: Genera cibo in posizioni casuali e gestisce il consumo
- **Particelle**: Sistema di effetti visivi per feedback visivo
- **Punteggio**: Tiene traccia del punteggio e del livello

## State Management (gameStore.ts)

Zustand gestisce lo stato globale dell'applicazione:

- Stato del gioco (menu, playing, paused, gameover)
- Entità di gioco (serpente, cibo, ostacoli, particelle)
- Statistiche (punteggio, livello, record)
- Configurazione (modalità, difficoltà, impostazioni)

## Design Pattern Utilizzati

1. **Singleton**: `gameEngine` è un'istanza singleton
2. **Observer**: Callbacks per eventi di gioco
3. **State Machine**: Stati del gioco ben definiti con transizioni
4. **Component Pattern**: Componenti React modulari e riutilizzabili
5. **Store Pattern**: Zustand per stato globale centralizzato

## Modalità di Gioco

| Modalità | Descrizione | Velocità | Ostacoli | Power-up |
|----------|-------------|----------|----------|----------|
| Classic | Tradizionale | Normale | No | No |
| Speed | Veloce | Alta | No | Sì |
| Obstacles | Con ostacoli | Media | Sì | Sì |
| Zen | Rilassante | Lenta | No | No |
| Challenge | Estrema | Molto alta | Sì | Sì |

## Responsive Design

Il gioco è progettato per funzionare su tutti i dispositivi:

- **Desktop**: Controlli da tastiera (frecce/WASD)
- **Mobile**: Controlli touch (D-pad virtuale)
- **Tablet**: Entrambi i metodi supportati

## SEO e Accessibilità

- Semantic HTML5
- ARIA labels per controlli
- Keyboard navigation completa
- Contrasto WCAG compliant
- Metadata OpenGraph

## Performance

- Canvas rendering ottimizzato
- requestAnimationFrame per game loop
- React memoization dove appropriato
- Static generation per pagine Next.js

## Aggiornamenti Futuri

- [ ] Sistema audio con Howler.js
- [ ] Classifica online
- [ ] Modalità multiplayer
- [ ] Skin personalizzate
- [ ] Achievement system
- [ ] PWA support