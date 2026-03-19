"""
MRT Shortest Path Finder — Tkinter GUI
Calls dijkstra() from algorithms/dijkstra.py and the graph from data/mrt_graph.py
Run from the project root:  python -m app.gui
"""

import tkinter as tk
from tkinter import ttk, font
import sys, os

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.mrt_graph import graph
from algorithms.dijkstra import dijkstra

# ── Colour constants ────────────────────────────────────────────────────────
BG        = "#0e0f13"
SURFACE   = "#16181f"
SURFACE2  = "#1e2029"
BORDER    = "#2a2c36"
TEXT      = "#e8e9ef"
MUTED     = "#6b6e80"
ACCENT    = "#39d353"   # green  (path highlight)
ACCENT2   = "#f0c040"   # amber  (endpoints)
WALL      = "#111318"
CARD_BG   = "#16181f"

LINE_COLORS = {
    "NS": "#e8311a",
    "EW": "#009645",
    "NE": "#9b26af",
    "CC": "#fa9e0d",
    "DT": "#005ec4",
    "TE": "#9d5b25",
}

# ── Station → line codes ─────────────────────────────────────────────────────
NS = ["Jurong East","Bukit Batok","Bukit Gombak","Choa Chu Kang","Yew Tee",
      "Kranji","Marsiling","Woodlands","Admiralty","Sembawang","Canberra",
      "Yishun","Khatib","Yio Chu Kang","Ang Mo Kio","Bishan","Braddell",
      "Toa Payoh","Novena","Newton","Orchard","Somerset","Dhoby Ghaut",
      "City Hall","Raffles Place","Marina Bay","Marina South Pier"]

EW = ["Pasir Ris","Tampines","Simei","Tanah Merah","Bedok","Kembangan","Eunos",
      "Paya Lebar","Aljunied","Kallang","Lavender","Bugis","City Hall",
      "Raffles Place","Tanjong Pagar","Outram Park","Tiong Bahru","Redhill",
      "Queenstown","Commonwealth","Buona Vista","Dover","Clementi","Jurong East",
      "Chinese Garden","Lakeside","Boon Lay","Pioneer","Joo Koon","Gul Circle",
      "Tuas Crescent","Tuas West Road","Tuas Link"]

NE = ["HarbourFront","Outram Park","Chinatown","Clarke Quay","Dhoby Ghaut",
      "Little India","Farrer Park","Boon Keng","Potong Pasir","Woodleigh",
      "Serangoon","Kovan","Hougang","Buangkok","Sengkang","Punggol"]

CC = ["Dhoby Ghaut","Bras Basah","Esplanade","Promenade","Nicoll Highway",
      "Stadium","Mountbatten","Dakota","Paya Lebar","MacPherson","Tai Seng",
      "Bartley","Serangoon","Lorong Chuan","Bishan","Marymount","Caldecott",
      "Botanic Gardens","Farrer Road","Holland Village","Buona Vista",
      "one-north","Kent Ridge","Haw Par Villa","Pasir Panjang","Labrador Park",
      "Telok Blangah","HarbourFront"]

DT = ["Bukit Panjang","Cashew","Hillview","Hume","Beauty World",
      "King Albert Park","Sixth Avenue","Tan Kah Kee","Botanic Gardens",
      "Stevens","Newton","Little India","Rochor","Bugis","Promenade",
      "Bayfront","Downtown","Telok Ayer","Chinatown","Fort Canning",
      "Bencoolen","Jalan Besar","Bendemeer","Geylang Bahru","Mattar",
      "MacPherson","Ubi","Kaki Bukit","Bedok North","Bedok Reservoir",
      "Tampines West","Tampines","Tampines East","Upper Changi","Expo"]

TE = ["Woodlands North","Woodlands","Woodlands South","Springleaf","Lentor",
      "Mayflower","Bright Hill","Upper Thomson","Caldecott","Stevens",
      "Napier","Orchard Boulevard","Orchard","Great World","Havelock",
      "Outram Park","Maxwell","Shenton Way","Marina Bay","Gardens by the Bay",
      "Tanjong Rhu","Katong Park","Tanjong Katong","Marine Parade",
      "Marine Terrace","Siglap","Bayshore","Bedok South","Sungei Bedok"]

LINE_STATIONS = {"NS": NS, "EW": EW, "NE": NE, "CC": CC, "DT": DT, "TE": TE}

station_lines: dict[str, list[str]] = {}
for code, stations in LINE_STATIONS.items():
    for s in stations:
        station_lines.setdefault(s, [])
        if code not in station_lines[s]:
            station_lines[s].append(code)

def primary_color(station: str) -> str:
    codes = station_lines.get(station, [])
    return LINE_COLORS.get(codes[0], MUTED) if codes else MUTED

# ── Coordinates matched to official LTA System Map 2025 ─────────────────────
# Logical space 900×600. EW line ~y=355, NS spine ~x=480, NE diagonal top-right.
COORDS: dict[str, tuple[int, int]] = {

    # EW Line — long horizontal band ~y=355
    "Tuas Link":        ( 20, 382), "Tuas West Road":   ( 44, 378),
    "Tuas Crescent":    ( 68, 374), "Gul Circle":       ( 92, 370),
    "Joo Koon":         (116, 368), "Pioneer":          (142, 364),
    "Boon Lay":         (170, 362), "Lakeside":         (198, 362),
    "Chinese Garden":   (222, 362), "Jurong East":      (248, 362),
    "Clementi":         (275, 362), "Dover":            (300, 362),
    "Buona Vista":      (323, 357), "Commonwealth":     (346, 353),
    "Queenstown":       (368, 349), "Redhill":          (388, 342),
    "Tiong Bahru":      (406, 335), "Outram Park":      (424, 327),
    "Tanjong Pagar":    (442, 335), "Raffles Place":    (460, 335),
    "City Hall":        (460, 315), "Bugis":            (478, 303),
    "Lavender":         (498, 303), "Kallang":          (520, 303),
    "Aljunied":         (542, 303), "Paya Lebar":       (564, 297),
    "Eunos":            (586, 303), "Kembangan":        (608, 307),
    "Bedok":            (630, 312), "Tanah Merah":      (653, 312),
    "Simei":            (674, 309), "Tampines":         (698, 302),
    "Pasir Ris":        (722, 296),

    # NS Line — vertical spine, west-centre of map
    "Woodlands North":  (350,  18), "Woodlands":        (350,  42),
    "Marsiling":        (330,  60), "Kranji":           (312,  78),
    "Admiralty":        (374,  42), "Sembawang":        (398,  34),
    "Canberra":         (420,  34), "Yishun":           (442,  34),
    "Khatib":           (442,  58), "Yio Chu Kang":     (458,  84),
    "Ang Mo Kio":       (470, 110), "Bishan":           (481, 137),
    "Braddell":         (481, 160), "Toa Payoh":        (481, 183),
    "Novena":           (481, 206), "Newton":           (481, 230),
    "Orchard":          (467, 260), "Somerset":         (467, 280),
    "Dhoby Ghaut":      (467, 300),
    "Marina Bay":       (470, 405), "Marina South Pier":(470, 428),

    # NS west branch (Jurong East ↔ Choa Chu Kang)
    "Yew Tee":          (248, 166), "Choa Chu Kang":    (248, 188),
    "Bukit Gombak":     (248, 211), "Bukit Batok":      (248, 234),

    # NE Line — diagonal from Punggol (top-right) to HarbourFront (bottom-left)
    "Punggol":          (628,  48), "Sengkang":         (605,  74),
    "Buangkok":         (582,  98), "Hougang":          (560, 122),
    "Kovan":            (538, 146), "Serangoon":        (516, 170),
    "Woodleigh":        (500, 188), "Potong Pasir":     (488, 206),
    "Boon Keng":        (482, 228), "Farrer Park":      (482, 248),
    "Little India":     (482, 270), "Clarke Quay":      (450, 310),
    "Chinatown":        (442, 327), "HarbourFront":     (406, 445),

    # CC Line — large oval loop
    "Marymount":        (460, 148), "Caldecott":        (444, 171),
    "Lorong Chuan":     (503, 151), "Bartley":          (524, 161),
    "Tai Seng":         (544, 174), "MacPherson":       (562, 190),
    "Mattar":           (544, 208), "Geylang Bahru":    (526, 221),
    "Bendemeer":        (512, 238), "Jalan Besar":      (502, 255),
    "Bencoolen":        (492, 271), "Bras Basah":       (478, 295),
    "Esplanade":        (478, 311), "Promenade":        (490, 325),
    "Nicoll Highway":   (504, 319), "Stadium":          (522, 319),
    "Mountbatten":      (540, 319), "Dakota":           (560, 312),
    "Farrer Road":      (394, 256), "Holland Village":  (372, 278),
    "one-north":        (350, 299), "Kent Ridge":       (330, 316),
    "Haw Par Villa":    (312, 333), "Pasir Panjang":    (298, 349),
    "Labrador Park":    (312, 365), "Telok Blangah":    (336, 379),

    # DT Line — diagonal top-left → through centre → east
    "Bukit Panjang":    (210, 170), "Cashew":           (224, 186),
    "Hillview":         (238, 200), "Hume":             (251, 210),
    "Beauty World":     (263, 220), "King Albert Park": (275, 230),
    "Sixth Avenue":     (287, 240), "Tan Kah Kee":      (299, 248),
    "Botanic Gardens":  (312, 257), "Stevens":          (450, 216),
    "Rochor":           (490, 291), "Fort Canning":     (453, 304),
    "Downtown":         (470, 322), "Bayfront":         (482, 336),
    "Telok Ayer":       (458, 336),
    "Ubi":              (566, 324), "Kaki Bukit":       (580, 328),
    "Bedok North":      (596, 332), "Bedok Reservoir":  (612, 336),
    "Tampines West":    (676, 291), "Tampines East":    (712, 291),
    "Upper Changi":     (726, 304), "Expo":             (740, 312),

    # TE Line — Woodlands north, down through Orchard/CBD, east coast
    "Woodlands South":  (364,  56), "Springleaf":       (394,  60),
    "Lentor":           (414,  76), "Mayflower":        (426,  93),
    "Bright Hill":      (438, 112), "Upper Thomson":    (446, 135),
    "Napier":           (456, 240), "Orchard Boulevard":(462, 250),
    "Great World":      (454, 288), "Havelock":         (448, 300),
    "Maxwell":          (452, 346), "Shenton Way":      (462, 358),
    "Gardens by the Bay":(496, 414),
    "Tanjong Rhu":      (508, 389), "Katong Park":      (523, 378),
    "Tanjong Katong":   (538, 368), "Marine Parade":    (553, 360),
    "Marine Terrace":   (569, 354), "Siglap":           (586, 350),
    "Bayshore":         (604, 348), "Bedok South":      (624, 351),
    "Sungei Bedok":     (644, 356),
}

# ── Main Application ─────────────────────────────────────────────────────────
class MRTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MRT Shortest Path Finder — Dijkstra's Algorithm")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(1100, 680)

        self._build_styles()
        self._build_ui()
        self._draw_map([])

    # ── Styles ────────────────────────────────────────────────────────────────
    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=SURFACE2, background=SURFACE2,
                        foreground=TEXT, selectbackground=SURFACE2,
                        selectforeground=TEXT, bordercolor=BORDER,
                        arrowcolor=MUTED, insertcolor=TEXT)
        style.map("TCombobox", fieldbackground=[("readonly", SURFACE2)])
        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=SURFACE)
        style.configure("TLabel", background=BG, foreground=TEXT,
                        font=("Syne", 11))
        style.configure("Muted.TLabel", background=SURFACE, foreground=MUTED,
                        font=("DM Mono", 9))
        style.configure("CardTitle.TLabel", background=SURFACE, foreground=MUTED,
                        font=("DM Mono", 8))
        style.configure("Big.TLabel", background=SURFACE, foreground=TEXT,
                        font=("Syne", 22, "bold"))
        style.configure("StopName.TLabel", background=SURFACE, foreground=TEXT,
                        font=("Syne", 11, "bold"))
        style.configure("SmallStop.TLabel", background=SURFACE, foreground=TEXT,
                        font=("Syne", 10))

    # ── UI layout ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Top header bar
        header = tk.Frame(self, bg=SURFACE, height=56, bd=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        icon = tk.Label(header, text="MRT", bg=ACCENT2, fg="#000",
                        font=("Syne", 11, "bold"), width=4, height=1,
                        padx=6, pady=4)
        icon.pack(side="left", padx=16, pady=10)

        tk.Label(header, text="Path Finder", bg=SURFACE, fg=TEXT,
                 font=("Syne", 14, "bold")).pack(side="left", padx=4)
        tk.Label(header, text="Singapore MRT Network", bg=SURFACE, fg=MUTED,
                 font=("DM Mono", 9)).pack(side="left", padx=8, pady=2)
        tk.Label(header, text="DIJKSTRA'S ALGORITHM", bg=SURFACE2, fg=ACCENT2,
                 font=("DM Mono", 8), padx=10, pady=4).pack(side="right", padx=16)

        # Separator
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # Body: left panel + right canvas
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=14)

        self._build_left(body)
        self._build_right(body)

    def _build_left(self, parent):
        left = tk.Frame(parent, bg=SURFACE, width=300, bd=0,
                        highlightthickness=1, highlightbackground=BORDER)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        pad = tk.Frame(left, bg=SURFACE)
        pad.pack(fill="both", expand=True, padx=16, pady=16)

        tk.Label(pad, text="ROUTE PLANNER", bg=SURFACE, fg=MUTED,
                 font=("DM Mono", 8), anchor="w").pack(fill="x", pady=(0, 12))

        # Station dropdowns
        all_stations = sorted(graph.keys())

        tk.Label(pad, text="● ORIGIN", bg=SURFACE, fg=ACCENT2,
                 font=("DM Mono", 9), anchor="w").pack(fill="x")
        self.var_from = tk.StringVar(value="Jurong East")
        cb_from = ttk.Combobox(pad, textvariable=self.var_from,
                               values=all_stations, state="readonly",
                               font=("Syne", 11))
        cb_from.pack(fill="x", pady=(4, 10))

        # Swap button
        swap_row = tk.Frame(pad, bg=SURFACE)
        swap_row.pack(fill="x")
        tk.Frame(swap_row, bg=BORDER, height=1).pack(fill="x", side="left", expand=True, pady=9)
        swap_btn = tk.Button(swap_row, text="⇅", bg=SURFACE2, fg=MUTED,
                             font=("Syne", 12), bd=0, padx=8, pady=2,
                             cursor="hand2", activebackground=SURFACE2,
                             activeforeground=ACCENT2,
                             command=self._swap_stations)
        swap_btn.pack(side="left", padx=6)
        tk.Frame(swap_row, bg=BORDER, height=1).pack(fill="x", side="left", expand=True, pady=9)

        tk.Label(pad, text="● DESTINATION", bg=SURFACE, fg=MUTED,
                 font=("DM Mono", 9), anchor="w").pack(fill="x")
        self.var_to = tk.StringVar(value="Punggol")
        cb_to = ttk.Combobox(pad, textvariable=self.var_to,
                             values=all_stations, state="readonly",
                             font=("Syne", 11))
        cb_to.pack(fill="x", pady=(4, 14))

        # Find button
        find_btn = tk.Button(pad, text="FIND SHORTEST PATH  →",
                             bg=ACCENT, fg="#000",
                             font=("Syne", 11, "bold"),
                             bd=0, padx=12, pady=10, cursor="hand2",
                             activebackground="#2ecc55", activeforeground="#000",
                             command=self._find_path)
        find_btn.pack(fill="x")

        # Stats cards
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=14)

        stats_row = tk.Frame(pad, bg=SURFACE)
        stats_row.pack(fill="x")
        self._stat_stops   = self._stat_card(stats_row, "STOPS",     "—")
        self._stat_time    = self._stat_card(stats_row, "EST. TIME", "—")
        self._stat_tr      = self._stat_card(stats_row, "TRANSFERS", "—")

        # Line legend
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=14)
        tk.Label(pad, text="LINES", bg=SURFACE, fg=MUTED,
                 font=("DM Mono", 8), anchor="w").pack(fill="x", pady=(0, 8))
        leg_grid = tk.Frame(pad, bg=SURFACE)
        leg_grid.pack(fill="x")
        for i, (code, col) in enumerate(LINE_COLORS.items()):
            row_f = tk.Frame(leg_grid, bg=SURFACE)
            row_f.grid(row=i//2, column=i%2, sticky="w", padx=(0,12), pady=2)
            tk.Label(row_f, text="  ", bg=col, width=2).pack(side="left")
            tk.Label(row_f, text=f" {code} Line", bg=SURFACE, fg=MUTED,
                     font=("DM Mono", 9)).pack(side="left")

        # Route list (scrollable)
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=14)
        tk.Label(pad, text="ROUTE", bg=SURFACE, fg=MUTED,
                 font=("DM Mono", 8), anchor="w").pack(fill="x", pady=(0, 6))

        route_container = tk.Frame(pad, bg=SURFACE)
        route_container.pack(fill="both", expand=True)

        self.route_canvas = tk.Canvas(route_container, bg=SURFACE,
                                      highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(route_container, orient="vertical",
                                 command=self.route_canvas.yview,
                                 bg=SURFACE2, troughcolor=SURFACE)
        self.route_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.route_canvas.pack(side="left", fill="both", expand=True)

        self.route_frame = tk.Frame(self.route_canvas, bg=SURFACE)
        self.route_canvas_win = self.route_canvas.create_window(
            (0, 0), window=self.route_frame, anchor="nw")
        self.route_frame.bind("<Configure>", self._on_route_resize)
        self.route_canvas.bind("<Configure>", self._on_canvas_resize)

        self._show_empty_route()

    def _stat_card(self, parent, label, value):
        card = tk.Frame(parent, bg=SURFACE2, padx=10, pady=8,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Label(card, text=label, bg=SURFACE2, fg=MUTED,
                 font=("DM Mono", 7)).pack(anchor="w")
        val_lbl = tk.Label(card, text=value, bg=SURFACE2, fg=TEXT,
                           font=("Syne", 18, "bold"))
        val_lbl.pack(anchor="w")
        return val_lbl

    def _build_right(self, parent):
        right = tk.Frame(parent, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="NETWORK MAP", bg=BG, fg=MUTED,
                 font=("DM Mono", 8), anchor="w").pack(fill="x", pady=(0, 6))

        self.canvas = tk.Canvas(right, bg=WALL, bd=0,
                                highlightthickness=1,
                                highlightbackground=BORDER)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw_map(self._current_path))

        self._current_path = []

    # ── Route panel helpers ───────────────────────────────────────────────────
    def _on_route_resize(self, event):
        self.route_canvas.configure(scrollregion=self.route_canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self.route_canvas.itemconfig(self.route_canvas_win, width=event.width)

    def _show_empty_route(self):
        for w in self.route_frame.winfo_children():
            w.destroy()
        tk.Label(self.route_frame, text="Select stations\nand find a path",
                 bg=SURFACE, fg=MUTED, font=("DM Mono", 9),
                 justify="center").pack(pady=20)

    def _update_route_list(self, path: list[str]):
        for w in self.route_frame.winfo_children():
            w.destroy()

        for i, station in enumerate(path):
            col = primary_color(station)
            is_end = i == 0 or i == len(path) - 1
            is_transfer = (i > 0 and
                           station_lines.get(station, [None])[0] !=
                           station_lines.get(path[i-1], [None])[0])

            row = tk.Frame(self.route_frame, bg=SURFACE)
            row.pack(fill="x", pady=1)

            # Coloured line indicator
            tk.Label(row, text="  ", bg=col,
                     width=2, pady=2 if is_end else 1).pack(side="left")

            info = tk.Frame(row, bg=SURFACE)
            info.pack(side="left", fill="x", expand=True, padx=6, pady=2)

            name_font = ("Syne", 10, "bold") if is_end else ("Syne", 10)
            tk.Label(info, text=station, bg=SURFACE, fg=TEXT,
                     font=name_font, anchor="w").pack(fill="x")

            codes = station_lines.get(station, [])
            if codes:
                tag_row = tk.Frame(info, bg=SURFACE)
                tag_row.pack(fill="x")
                for code in codes:
                    tc = LINE_COLORS.get(code, MUTED)
                    tk.Label(tag_row, text=f" {code} ", bg=SURFACE2,
                             fg=tc, font=("DM Mono", 7),
                             padx=3, pady=1).pack(side="left", padx=(0, 3))

            if is_transfer:
                tk.Label(row, text="⇄ TRANSFER", bg=SURFACE2,
                         fg=ACCENT2, font=("DM Mono", 7),
                         padx=5, pady=2).pack(side="right", padx=6)

    # ── Core actions ──────────────────────────────────────────────────────────
    def _swap_stations(self):
        a, b = self.var_from.get(), self.var_to.get()
        self.var_from.set(b)
        self.var_to.set(a)

    def _find_path(self):
        frm, to = self.var_from.get(), self.var_to.get()

        if frm not in graph or to not in graph:
            self._show_status("Invalid station name.", error=True)
            return
        if frm == to:
            self._show_status("Please select two different stations.", error=True)
            return

        cost, path = dijkstra(graph, frm, to)

        if not path:
            self._show_status("No route found between these stations.", error=True)
            self._current_path = []
            self._draw_map([])
            return

        stops = len(path) - 1
        mins  = round(cost * 1.8)
        transfers = sum(
            1 for i in range(1, len(path))
            if station_lines.get(path[i], [None])[0] !=
               station_lines.get(path[i-1], [None])[0]
        )

        self._stat_stops.config(text=str(stops))
        self._stat_time.config(text=f"{mins}m")
        self._stat_tr.config(text=str(transfers))

        self._current_path = path
        self._update_route_list(path)
        self._draw_map(path)

    def _show_status(self, msg, error=False):
        self._stat_stops.config(text="—")
        self._stat_time.config(text="—")
        self._stat_tr.config(text="—")
        self._show_empty_route()
        # Flash header with message
        popup = tk.Toplevel(self)
        popup.title("")
        popup.configure(bg=SURFACE)
        popup.resizable(False, False)
        tk.Label(popup, text=msg, bg=SURFACE,
                 fg="#e85555" if error else ACCENT,
                 font=("Syne", 11), padx=24, pady=16).pack()
        tk.Button(popup, text="OK", bg=SURFACE2, fg=TEXT,
                  font=("Syne", 10), bd=0, padx=16, pady=6,
                  command=popup.destroy).pack(pady=(0, 12))
        popup.grab_set()
        self.wait_window(popup)

    # ── Map drawing ───────────────────────────────────────────────────────────
    def _draw_map(self, active_path: list[str]):
        c = self.canvas
        c.delete("all")
        W = c.winfo_width()  or 820
        H = c.winfo_height() or 560

        # Scale coords to fit canvas with padding
        raw_xs = [v[0] for v in COORDS.values()]
        raw_ys = [v[1] for v in COORDS.values()]
        min_x, max_x = min(raw_xs), max(raw_xs)
        min_y, max_y = min(raw_ys), max(raw_ys)
        pad = 40

        def tx(x):
            return pad + (x - min_x) / (max_x - min_x) * (W - 2 * pad)
        def ty(y):
            return pad + (y - min_y) / (max_y - min_y) * (H - 2 * pad)

        active_set  = set(active_path)
        endpoints   = set(active_path[0:1] + (active_path[-1:] if len(active_path) > 1 else []))

        # ── Layer 1: dim network edges ────────────────────────────────────────
        for code, line_data in LINE_STATIONS.items():
            col = LINE_COLORS[code]
            for i in range(len(line_data) - 1):
                a, b = line_data[i], line_data[i + 1]
                if a not in COORDS or b not in COORDS:
                    continue
                x1, y1 = tx(COORDS[a][0]), ty(COORDS[a][1])
                x2, y2 = tx(COORDS[b][0]), ty(COORDS[b][1])
                c.create_line(x1, y1, x2, y2, fill=col, width=1.5,
                              stipple="gray25")   # very dim background

        # ── Layer 2: bright highlighted path (drawn on top of network) ────────
        if len(active_path) > 1:
            # White glow underneath
            for i in range(len(active_path) - 1):
                a, b = active_path[i], active_path[i + 1]
                if a not in COORDS or b not in COORDS:
                    continue
                x1, y1 = tx(COORDS[a][0]), ty(COORDS[a][1])
                x2, y2 = tx(COORDS[b][0]), ty(COORDS[b][1])
                c.create_line(x1, y1, x2, y2, fill="#ffffff",
                              width=7, capstyle="round")
            # Green path on top
            for i in range(len(active_path) - 1):
                a, b = active_path[i], active_path[i + 1]
                if a not in COORDS or b not in COORDS:
                    continue
                x1, y1 = tx(COORDS[a][0]), ty(COORDS[a][1])
                x2, y2 = tx(COORDS[b][0]), ty(COORDS[b][1])
                c.create_line(x1, y1, x2, y2, fill=ACCENT,
                              width=4, capstyle="round")

        # ── Layer 3: all station dots + dim labels ────────────────────────────
        for station, (sx, sy) in COORDS.items():
            if station not in graph:
                continue
            if station in active_set:
                continue   # draw active ones in layer 4
            x, y = tx(sx), ty(sy)
            col = primary_color(station)
            c.create_oval(x - 2, y - 2, x + 2, y + 2,
                          fill=SURFACE2, outline=col, width=1)
            # Dim station name label
            c.create_text(x + 4, y - 6, text=station,
                          fill=MUTED, font=("Courier", 6),
                          anchor="sw")

        # ── Layer 4: active path dots + bright labels (drawn last = on top) ───
        for station in active_path:
            if station not in COORDS:
                continue
            sx, sy = COORDS[station]
            x, y   = tx(sx), ty(sy)
            col    = primary_color(station)

            if station in endpoints:
                # Large amber endpoint circle
                r = 9
                c.create_oval(x - r - 2, y - r - 2, x + r + 2, y + r + 2,
                              fill="#ffffff", outline="#ffffff")
                c.create_oval(x - r, y - r, x + r, y + r,
                              fill=ACCENT2, outline=ACCENT2)
                # Bold amber label with dark shadow for readability
                c.create_text(x + 1, y - r - 7, text=station,
                              fill=WALL, font=("Courier", 8, "bold"),
                              anchor="sw")
                c.create_text(x, y - r - 8, text=station,
                              fill=ACCENT2, font=("Courier", 8, "bold"),
                              anchor="sw")
            else:
                # Smaller green dot for intermediate stops
                r = 4
                c.create_oval(x - r, y - r, x + r, y + r,
                              fill=ACCENT, outline="#ffffff", width=1)
                # Bright white label
                c.create_text(x + 1, y - r - 5, text=station,
                              fill=WALL, font=("Courier", 7, "bold"),
                              anchor="sw")
                c.create_text(x, y - r - 6, text=station,
                              fill="#ffffff", font=("Courier", 7, "bold"),
                              anchor="sw")


if __name__ == "__main__":
    app = MRTApp()
    app.mainloop()
