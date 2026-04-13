"""
score.py - Sistema di salvataggio punteggi
============================================
Gestisce il salvataggio e caricamento dei punteggi alti.
I punteggi vengono salvati in un file JSON nella cartella 'dati'.
"""

import json
import os
from src.config import *


class GestorePunteggi:
    """
    Gestisce la classifica dei punteggi alti.
    Salva e carica i punteggi da un file JSON.
    """
    
    def __init__(self):
        """Inizializza il gestore punteggi."""
        self.punteggi = []  # Lista di (nome, punteggio, data)
        self.punteggio_alto = 0  # Punteggio record assoluto
        self._carica()
    
    def _carica(self):
        """
        Carica i punteggi dal file JSON.
        Se il file non esiste, crea una lista vuota.
        """
        try:
            # Crea la cartella 'dati' se non esiste
            os.makedirs(os.path.dirname(PERCORSO_PUNTEGGI), exist_ok=True)
            
            if os.path.exists(PERCORSO_PUNTEGGI):
                with open(PERCORSO_PUNTEGGI, 'r') as f:
                    dati = json.load(f)
                    self.punteggi = dati.get('punteggi', [])
                    print(f"[DEBUG] Caricati {len(self.punteggi)} punteggi")
            else:
                self.punteggi = []
                print("[DEBUG] Nessun file punteggi trovato, creo lista vuota")
            
            # Aggiorna il punteggio alto
            if self.punteggi:
                self.punteggio_alto = max(p[1] for p in self.punteggi)
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"[DEBUG] Errore caricamento punteggi: {e}")
            self.punteggi = []
            self.punteggio_alto = 0
    
    def _salva(self):
        """
        Salva i punteggi nel file JSON.
        """
        try:
            os.makedirs(os.path.dirname(PERCORSO_PUNTEGGI), exist_ok=True)
            
            dati = {
                'punteggi': self.punteggi
            }
            
            with open(PERCORSO_PUNTEGGI, 'w') as f:
                json.dump(dati, f, indent=2)
                
            print(f"[DEBUG] Salvati {len(self.punteggi)} punteggi")
            
        except IOError as e:
            print(f"[DEBUG] Errore salvataggio punteggi: {e}")
    
    def aggiungi_punteggio(self, punteggio, nome="Giocatore"):
        """
        Aggiunge un nuovo punteggio alla classifica.
        
        Args:
            punteggio: Il punteggio ottenuto
            nome: Nome del giocatore (default "Giocatore")
        
        Returns:
            Posizione in classifica (1 = primo)
        """
        from datetime import datetime
        
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.punteggi.append([nome, punteggio, data])
        
        # Ordina per punteggio decrescente
        self.punteggi.sort(key=lambda x: x[1], reverse=True)
        
        # Mantieni solo i top 10
        self.punteggi = self.punteggi[:10]
        
        # Aggiorna punteggio alto
        if self.punteggi:
            self.punteggio_alto = self.punteggi[0][1]
        
        # Salva su file
        self._salva()
        
        # Ritorna la posizione
        for i, p in enumerate(self.punteggi):
            if p[1] == punteggio and p[2] == data:
                return i + 1
        
        return len(self.punteggi)
    
    def e_nuovo_record(self, punteggio):
        """
        Controlla se il punteggio è un nuovo record.
        
        Args:
            punteggio: Il punteggio da controllare
        
        Returns:
            True se è un nuovo record
        """
        return punteggio > self.punteggio_alto
    
    def ottieni_classifica(self, limite=10):
        """
        Ritorna la classifica dei migliori punteggi.
        
        Args:
            limite: Quanti punteggi mostrare (default 10)
        
        Returns:
            Lista di (posizione, nome, punteggio, data)
        """
        classifica = []
        for i, (nome, punteggio, data) in enumerate(self.punteggi[:limite]):
            classifica.append((i + 1, nome, punteggio, data))
        return classifica
    
    def ottieni_punteggio_alto(self):
        """Ritorna il punteggio record."""
        return self.punteggio_alto