import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import folium
from motore_astar import carica_voli_da_pl, percorso_astar, coord

# === Visualizzazione mappa con Folium ===
def mostra_percorso_folium(G, percorso):
    lat0, lon0 = coord[percorso[0]]
    mappa = folium.Map(location=[lat0, lon0], zoom_start=3)

    for u, v in G.edges:
        if u in coord and v in coord:
            folium.PolyLine([coord[u], coord[v]], color="lightgray", weight=1, opacity=0.4).add_to(mappa)

    for city in percorso:
        if city in coord:
            folium.Marker(
                location=coord[city],
                popup=city.capitalize(),
                icon=folium.Icon(color="blue", icon="plane", prefix="fa")
            ).add_to(mappa)

    for u, v in zip(percorso[:-1], percorso[1:]):
        if u in coord and v in coord:
            folium.PolyLine([coord[u], coord[v]], color="red", weight=3).add_to(mappa)

    mappa.save("mappa_astar.html")
    webbrowser.open("mappa_astar.html")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("volA*i")
        self.root.geometry("480x400")
        self.root.resizable(True, True)
        self.root.configure(bg="#eaf3fc")  # Azzurro chiarissimo di sfondo

        # Stile moderno blu
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#eaf3fc")
        style.configure("TLabel", background="#eaf3fc", foreground="#0d3b66", font=("Segoe UI", 10))
        style.configure("TButton", background="#0d3b66", foreground="white", font=("Segoe UI", 10), padding=6)
        style.map("TButton", background=[("active", "#125ea3")])
        style.configure("TCombobox", padding=5, font=("Segoe UI", 10))

        self.G = carica_voli_da_pl("voli.pl")

        messagebox.showinfo(
            "Informazione",
            "Questa applicazione usa l'algoritmo A* per trovare il percorso migliore tra città,\n\n"
            "In base alla distanza geografica e alla presenza di voli diretti, l'algoritmo A* trova il percorso più naturale tra le città.")

        # Layout principale
        frame = ttk.Frame(root, padding=20)
        frame.grid(sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Interfaccia
        ttk.Label(frame, text="Città di partenza:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.cb_partenza = ttk.Combobox(frame, values=sorted(self.G.nodes), state="readonly")
        self.cb_partenza.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(frame, text="Città di arrivo:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cb_arrivo = ttk.Combobox(frame, values=sorted(self.G.nodes), state="readonly")
        self.cb_arrivo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.btn_cerca = ttk.Button(frame, text="Trova percorso", command=self.cerca_percorso)
        self.btn_cerca.grid(row=2, column=0, columnspan=2, pady=15)

        self.lbl_output = ttk.Label(frame, text="", justify="left", font=("Segoe UI", 10), wraplength=400)
        self.lbl_output.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.btn_grafo = ttk.Button(frame, text="Mostra mappa", command=self.mostra_grafo)
        self.btn_grafo.grid(row=4, column=0, columnspan=2, pady=10)
        self.btn_grafo.state(["disabled"])

        self.ultimo_percorso = None

    def cerca_percorso(self):
        part = self.cb_partenza.get().strip().lower()
        arr = self.cb_arrivo.get().strip().lower()

        if not part or not arr or part == arr:
            messagebox.showwarning("Attenzione", "Inserisci due città valide e diverse.")
            return

        risultato = percorso_astar(self.G, part, arr)
        if risultato:
            percorso, costo, durata = risultato
            self.ultimo_percorso = percorso
            testo = (
                f"Percorso trovato:\n"
                f"{' → '.join(percorso)}\n\n"
                f"Costo totale: {costo}\n"
                f"Durata stimata: {int(durata)} ore\n\n"
                f"Calcolato con algoritmo A* su base costi e distanza."
            )
            self.lbl_output.config(text=testo)
            self.btn_grafo.state(["!disabled"])
        else:
            self.lbl_output.config(text="Nessun percorso trovato.")
            self.btn_grafo.state(["disabled"])

    def mostra_grafo(self):
        if self.ultimo_percorso:
            mostra_percorso_folium(self.G, self.ultimo_percorso)

# === Avvio ===
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
