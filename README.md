![Logo](./logo.jng)

# ✈️ volA*i 

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**Progetto per il corso di Intelligenza Artificiale – Università degli Studi di Napoli Federico II**  
_Antonio Marco Vanacore – Chiara Improta_  
_A.A. 2024/2025 – Prof. Giancarlo Sperlì_

---

## 📌 Obiettivo

Il progetto consiste nello sviluppo di un'applicazione intelligente in grado di calcolare il **percorso aereo più efficiente tra due città**, utilizzando una rete di voli ispirata a dati reali. Il problema è modellato come un grafo e risolto attraverso l’algoritmo di **ricerca informata A\***.

L’applicazione fornisce:
- Percorso più breve (con penalizzazione per scali)
- Costo totale del viaggio
- Durata stimata
- Visualizzazione interattiva su mappa (via browser)

---

## 🧠 Algoritmo A\*

L’algoritmo A\* è utilizzato per calcolare il percorso minimo in un grafo, secondo la formula:

```
f(n) = g(n) + h(n)
```

- `g(n)` = costo accumulato
- `h(n)` = distanza geografica stimata (formula di Haversine)

Il sistema penalizza automaticamente i percorsi con scali, preferendo voli diretti quando possibile.

---

## 🗂️ Struttura del progetto

```
├── gui_astar.py          # Interfaccia grafica tkinter
├── motore_astar.py       # Logica A* e parsing dataset
├── voli.pl               # Dataset in stile Prolog
├── volAI.pdf             # Tesina descrittiva completa
└── requirements.txt      # Requisiti da installare
└── README.md             # Questo file
```

---

## 🖥️ Requisiti

- Python 3.8+
- Librerie specificate nel file requirements.txt

Installa i moduli richiesti:

```bash
pip install -r requirements.txt
```

---

## 🚀 Come eseguire

Dal terminale (nella cartella del progetto):

```bash
python gui_astar.py
```

1. Seleziona città di partenza e arrivo
2. Clicca su **"Trova percorso"**
3. Visualizza i risultati e apri la mappa cliccando su **"Mostra mappa"**

---

## 🌍 Dataset

Il file `voli.pl` contiene circa **500 voli** tra le principali città del mondo.  
Ogni riga ha la forma:

```prolog
flight(parigi, berlino, 100, 2, airfrance).
```

> Il file è trattato come testo strutturato e convertito in grafo tramite parsing Python.

---

## 🗺️ Visualizzazione con Folium

L’app genera automaticamente una **mappa HTML interattiva**, in cui:
- Le rotte disponibili sono grigie
- Il percorso scelto è evidenziato in rosso
- Le città selezionate hanno un marker

La mappa si apre nel browser al termine del calcolo.

---

## 📈 Risultati

Il sistema è stato testato su diverse rotte (es. Parigi → Bruxelles, Roma → Tokyo)  
I percorsi generati sono coerenti con la rete dei voli, e la penalizzazione per gli scali funziona correttamente.

![Demo](./demo.gif)

---

## 🔧 Estensioni possibili

- Gestione orari e frequenze dei voli
- Filtri per compagnie aeree o classi di volo
- Integrazione con motore logico Prolog
- Pianificazione multiscopo (costo + tempo + scali)

---

## 📄 Licenza

Distribuito per scopi didattici.  
© 2024 Antonio Marco Vanacore, Chiara Improta – Università degli Studi di Napoli Federico II.
