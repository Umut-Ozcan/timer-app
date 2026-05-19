import tkinter as tk
from tkinter import ttk, font, messagebox, colorchooser

DEFAULT_THEME = {
    "bg":       "#1a1a2e",
    "card":     "#16213e",
    "accent":   "#e94560",
    "text":     "#eaeaea",
    "muted":    "#888899",
    "btn_bg":   "#0f3460",
    "entry_bg": "#0d0d1a",
    "timer_fg": "#eaeaea",
}

PRESET_THEMES = [
    ("🌙 Koyu Mavi",  {"bg":"#1a1a2e","card":"#16213e","accent":"#e94560","text":"#eaeaea","muted":"#888899","btn_bg":"#0f3460","entry_bg":"#0d0d1a","timer_fg":"#eaeaea"}),
    ("🌿 Orman",      {"bg":"#1b2e1f","card":"#162618","accent":"#4caf50","text":"#e8f5e9","muted":"#7a9b7c","btn_bg":"#2e5233","entry_bg":"#0d1a0f","timer_fg":"#a5d6a7"}),
    ("🌅 Gün Batımı", {"bg":"#2e1a0e","card":"#3d2010","accent":"#ff7043","text":"#fff3e0","muted":"#a07060","btn_bg":"#5d3318","entry_bg":"#1a0d06","timer_fg":"#ffab91"}),
    ("💜 Mor Gece",   {"bg":"#1a0a2e","card":"#16072a","accent":"#bb86fc","text":"#ede7f6","muted":"#8070a0","btn_bg":"#2d1060","entry_bg":"#0d0518","timer_fg":"#ce93d8"}),
    ("🩵 Buz",        {"bg":"#0a1929","card":"#0d2137","accent":"#00b0ff","text":"#e3f2fd","muted":"#607d8b","btn_bg":"#0d3b5e","entry_bg":"#050e1a","timer_fg":"#80d8ff"}),
    ("🤍 Açık",       {"bg":"#f5f5f5","card":"#ffffff","accent":"#e94560","text":"#212121","muted":"#9e9e9e","btn_bg":"#e0e0e0","entry_bg":"#fafafa","timer_fg":"#212121"}),
]

FONTS_LIST = [
    "Arial", "Arial Black", "Arial Narrow", "Arial Rounded MT Bold",
    "Calibri", "Calibri Light", "Cambria", "Candara",
    "Century Gothic", "Century Schoolbook", "Comic Sans MS", "Consolas",
    "Constantia", "Corbel", "Courier New", "Dubai",
    "Ebrima", "Franklin Gothic Medium", "Gabriola", "Gadugi",
    "Georgia", "Gill Sans MT", "Gloucester MT Extra Condensed",
    "Helvetica", "Impact", "Ink Free", "Javanese Text",
    "Leelawadee UI", "Lucida Console", "Lucida Handwriting",
    "Lucida Sans Unicode", "Malgun Gothic", "Microsoft Sans Serif",
    "MV Boli", "Myanmar Text", "Palatino Linotype", "Perpetua",
    "Rockwell", "Segoe Print", "Segoe Script", "Segoe UI",
    "Segoe UI Black", "Segoe UI Light", "Segoe UI Semibold",
    "Sylfaen", "Tahoma", "Times New Roman", "Trebuchet MS",
    "Tw Cen MT", "Verdana", "Vivaldi", "Vladimir Script",
    "Wide Latin", "Yu Gothic", "Yu Gothic Light", "Yu Gothic Medium",
]

TEXT_COLORS = ["#eaeaea","#e94560","#00d4ff","#00ff99","#ffcc00","#ff69b4","#bb86fc"]
PRESETS = [1, 5, 10, 25, 45, 60]


def get_monitors():
    monitors = []
    try:
        import ctypes
        MonitorEnumProc = ctypes.WINFUNCTYPE(
            ctypes.c_bool, ctypes.c_ulong, ctypes.c_ulong,
            ctypes.POINTER(ctypes.c_long * 4), ctypes.c_double)
        def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
            r = lprcMonitor.contents
            monitors.append({"x":r[0],"y":r[1],"w":r[2]-r[0],"h":r[3]-r[1]})
            return True
        ctypes.windll.user32.EnumDisplayMonitors(0, 0, MonitorEnumProc(callback), 0)
    except Exception:
        pass
    if not monitors:
        root = tk.Tk(); root.withdraw()
        monitors.append({"x":0,"y":0,"w":root.winfo_screenwidth(),"h":root.winfo_screenheight()})
        root.destroy()
    return monitors


class DisplayWindow(tk.Toplevel):
    def __init__(self, master, monitor, app):
        super().__init__(master)
        self.app = app
        self.configure(bg=app.C["bg"])
        self.overrideredirect(True)
        self.geometry(f"{monitor['w']}x{monitor['h']}+{monitor['x']}+{monitor['y']}")
        self.attributes("-topmost", True)

        self.display_font_size = 120

        self.lbl_time = tk.Label(self, text="00:00",
                                 font=("Courier New", self.display_font_size, "bold"),
                                 bg=app.C["bg"], fg=app.C["timer_fg"])
        self.lbl_time.place(relx=0.5, rely=0.38, anchor="center")

        self.lbl_note = tk.Label(self, text="",
                                 font=("Arial", 22), bg=app.C["bg"], fg=app.C["muted"],
                                 wraplength=monitor['w']-100, justify="center")
        self.lbl_note.place(relx=0.5, rely=0.65, anchor="center")

        self.lbl_alert = tk.Label(self, text="",
                                  font=("Arial", 28, "bold"),
                                  bg=app.C["bg"], fg=app.C["accent"])
        self.lbl_alert.place(relx=0.5, rely=0.82, anchor="center")

        btn = tk.Button(self, text="✕  Kapat", font=("Arial", 12),
                        bg=app.C["bg"], fg=app.C["muted"], relief="flat", bd=0,
                        cursor="hand2", command=self.close_display)
        btn.place(relx=0.98, rely=0.02, anchor="ne")
        btn.bind("<Enter>", lambda e: btn.config(fg=app.C["accent"]))
        btn.bind("<Leave>", lambda e: btn.config(fg=app.C["muted"]))

        self.bind("<Escape>", lambda e: self.close_display())

    def _size_up(self):
        self.display_font_size = min(300, self.display_font_size + 10)
        self.lbl_time.config(font=("Courier New", self.display_font_size, "bold"))
        self.lbl_size.config(text=str(self.display_font_size))

    def _size_down(self):
        self.display_font_size = max(40, self.display_font_size - 10)
        self.lbl_time.config(font=("Courier New", self.display_font_size, "bold"))
        self.lbl_size.config(text=str(self.display_font_size))

    def refresh_colors(self):
        C = self.app.C
        self.configure(bg=C["bg"])
        self.lbl_time.config(bg=C["bg"], fg=C["timer_fg"])
        self.lbl_note.config(bg=C["bg"])
        self.lbl_alert.config(bg=C["bg"], fg=C["accent"])

    def update_time(self, t):  self.lbl_time.config(text=t)
    def update_note(self, text, fam, size, color, bold, italic):
        f = font.Font(family=fam, size=max(16, size+6),
                      weight="bold" if bold else "normal",
                      slant="italic" if italic else "roman")
        self.lbl_note.config(text=text, font=f, fg=color)
    def show_alert(self, t):   self.lbl_alert.config(text=t)
    def close_display(self):
        self.app.display_win = None
        self.app.btn_display.config(text="📺  Ekranda Göster")
        self.destroy()


class ColorPanel(tk.Toplevel):
    """Sol üstte açılıp kapanan renk & tema penceresi."""
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg=app.C["card"])

        self._build()
        self._position()

        # Dışarı tıklayınca kapat
        self.bind("<FocusOut>", self._on_focus_out)
        self.focus_force()

    def _position(self):
        self.update_idletasks()
        # Ana pencerenin sol üstüne hizala
        mx = self.app.winfo_rootx()
        my = self.app.winfo_rooty()
        self.geometry(f"340x480+{mx+10}+{my+10}")

    def _on_focus_out(self, e):
        # Kendi alt widget'larına tıklanınca kapanmasın
        try:
            focused = self.focus_get()
            if focused and str(focused).startswith(str(self)):
                return
        except Exception:
            pass
        self.close()

    def close(self):
        try:
            self.app.color_panel = None
            self.app.btn_color.config(text="🎨  Tema & Renkler")
        except Exception:
            pass
        self.destroy()

    def _build(self):
        C = self.app.C

        # Başlık çubuğu
        title_bar = tk.Frame(self, bg=C["accent"], cursor="fleur")
        title_bar.pack(fill="x")
        tk.Label(title_bar, text="🎨  Tema & Renkler", font=("Arial", 10, "bold"),
                 bg=C["accent"], fg="white").pack(side="left", padx=10, pady=6)
        tk.Button(title_bar, text="✕", font=("Arial", 11, "bold"),
                  bg=C["accent"], fg="white", relief="flat", bd=0,
                  cursor="hand2", command=self.close).pack(side="right", padx=8)

        # Sürükle
        title_bar.bind("<ButtonPress-1>",   self._drag_start)
        title_bar.bind("<B1-Motion>",       self._drag_move)

        inner = tk.Frame(self, bg=C["card"])
        inner.pack(fill="both", expand=True, padx=12, pady=10)

        # Kaydırılabilir alan
        canvas = tk.Canvas(inner, bg=C["card"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(inner, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(canvas, bg=C["card"])
        canvas_win = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def on_resize(e):
            canvas.itemconfig(canvas_win, width=canvas.winfo_width())
        def on_frame_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_resize)
        scroll_frame.bind("<Configure>", on_frame_configure)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        # Hazır Temalar
        tk.Label(scroll_frame, text="Hazır Temalar", font=("Arial", 9, "bold"),
                 bg=C["card"], fg=C["muted"]).pack(anchor="w", pady=(0, 6))

        theme_grid = tk.Frame(scroll_frame, bg=C["card"])
        theme_grid.pack(fill="x", pady=(0, 12))
        for i, (name, theme) in enumerate(PRESET_THEMES):
            b = tk.Button(theme_grid, text=name, font=("Arial", 9),
                          bg=theme["btn_bg"], fg=theme["text"], relief="flat", bd=0,
                          padx=6, pady=4, cursor="hand2",
                          command=lambda t=theme: [self.app._apply_preset(t), self.close()])
            b.grid(row=i//2, column=i%2, padx=3, pady=3, sticky="ew")
            theme_grid.columnconfigure(i%2, weight=1)

        # Özel Renkler
        tk.Label(scroll_frame, text="Özel Renkler", font=("Arial", 9, "bold"),
                 bg=C["card"], fg=C["muted"]).pack(anchor="w", pady=(4, 6))

        for key, label in [
            ("bg",       "Arka Plan"),
            ("card",     "Kart"),
            ("accent",   "Vurgu"),
            ("text",     "Yazı"),
            ("timer_fg", "Timer"),
            ("btn_bg",   "Buton"),
            ("entry_bg", "Giriş Alanı"),
        ]:
            self._color_row(scroll_frame, label, key)

    def _color_row(self, parent, label, key):
        C = self.app.C
        row = tk.Frame(parent, bg=C["card"])
        row.pack(fill="x", pady=2)

        tk.Label(row, text=label, font=("Arial", 10),
                 bg=C["card"], fg=C["muted"], width=10, anchor="w").pack(side="left")

        preview = tk.Label(row, bg=C[key], width=3, height=1,
                           relief="solid", cursor="hand2")
        preview.pack(side="left", padx=(6, 4))

        hex_var = tk.StringVar(value=C[key])
        entry = tk.Entry(row, textvariable=hex_var, font=("Courier New", 9),
                         bg=C["entry_bg"], fg=C["text"],
                         insertbackground=C["text"],
                         relief="flat", bd=2, width=9)
        entry.pack(side="left", padx=(0, 4))

        def pick(k=key, pv=preview, hv=hex_var):
            color = colorchooser.askcolor(color=self.app.C[k], title=f"{label} rengi")
            if color and color[1]:
                self.app.C[k] = color[1]
                pv.config(bg=color[1])
                hv.set(color[1])
                self.app._apply_theme()

        def apply_hex(e=None, k=key, pv=preview, hv=hex_var):
            val = hv.get().strip()
            if len(val) in (7, 4) and val.startswith("#"):
                try:
                    self.winfo_rgb(val)
                    self.app.C[k] = val
                    pv.config(bg=val)
                    self.app._apply_theme()
                except Exception:
                    pass

        entry.bind("<Return>", apply_hex)
        entry.bind("<FocusOut>", apply_hex)

        btn = tk.Button(row, text="🎨", font=("Arial", 10),
                        bg=C["btn_bg"], fg=C["text"], relief="flat", bd=0,
                        padx=4, cursor="hand2", command=pick)
        btn.pack(side="left")
        btn.bind("<Enter>", lambda e, w=btn: w.config(bg=C["accent"]))
        btn.bind("<Leave>", lambda e, w=btn: w.config(bg=C["btn_bg"]))

    def _drag_start(self, e):
        self._dx = e.x_root - self.winfo_rootx()
        self._dy = e.y_root - self.winfo_rooty()

    def _drag_move(self, e):
        self.geometry(f"+{e.x_root - self._dx}+{e.y_root - self._dy}")


class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timer & Not Uygulaması")
        self.geometry("600x700")
        self.resizable(True, True)
        self.minsize(500, 600)

        self.C = dict(DEFAULT_THEME)
        self.configure(bg=self.C["bg"])

        self.total_secs  = 25 * 60
        self.remaining   = self.total_secs
        self.running     = False
        self._job        = None
        self.note_color  = self.C["text"]
        self.note_size   = 14
        self.note_font   = "Arial"
        self.bold        = False
        self.italic      = False
        self.display_win     = None
        self.color_panel     = None
        self.timer_font_size = 68
        self.monitors        = get_monitors()

        self._build_ui()
        self._update_display()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        if self.display_win: self.display_win.destroy()
        self.destroy()

    def _timer_size_up(self):
        self.timer_font_size = min(300, self.timer_font_size + 10)
        self._refresh_timer_font()

    def _timer_size_down(self):
        self.timer_font_size = max(40, self.timer_font_size - 10)
        self._refresh_timer_font()

    def _refresh_timer_font(self):
        try:
            self.lbl_timer_size.config(text=str(self.timer_font_size))
        except Exception:
            pass
        if self.display_win:
            try:
                self.display_win.display_font_size = self.timer_font_size
                self.display_win.lbl_time.config(font=("Courier New", self.timer_font_size, "bold"))
            except Exception:
                pass

    # ══════════════════════════════════════════════════
    #  Tema uygulama
    # ══════════════════════════════════════════════════
    def _apply_theme(self):
        self.configure(bg=self.C["bg"])
        try:
            self.lbl_time.config(fg=self.C["timer_fg"], bg=self.C["card"])
            self.lbl_alert.config(fg=self.C["accent"], bg=self.C["card"])
            self.note_text.config(bg=self.C["entry_bg"], fg=self.note_color,
                                  insertbackground=self.C["text"])
        except Exception:
            pass
        if self.display_win:
            self.display_win.refresh_colors()

    def _apply_preset(self, theme):
        self.C.update(theme)
        self._rebuild_ui()

    def _rebuild_ui(self):
        for w in self.outer.winfo_children():
            w.destroy()
        self.configure(bg=self.C["bg"])
        self.outer.configure(bg=self.C["bg"])
        self._build_timer_card(self.outer)
        self._build_note_card(self.outer)
        self._update_display()
        if self.display_win:
            self.display_win.refresh_colors()

    # ══════════════════════════════════════════════════
    #  UI
    # ══════════════════════════════════════════════════
    def _build_ui(self):
        self.outer = tk.Frame(self, bg=self.C["bg"])
        self.outer.pack(fill="both", expand=True, padx=18, pady=18)
        self._build_timer_card(self.outer)
        self._build_note_card(self.outer)

    def _card(self, parent):
        f = tk.Frame(parent, bg=self.C["card"], highlightthickness=1,
                     highlightbackground="#2a2a4a")
        f.pack(fill="x", pady=(0, 14))
        return f

    def _build_timer_card(self, parent):
        card  = self._card(parent)
        inner = tk.Frame(card, bg=self.C["card"])
        inner.pack(fill="x", padx=20, pady=18)

        # Üst satır: başlık + 🎨 buton sol üstte
        top_row = tk.Frame(inner, bg=self.C["card"])
        top_row.pack(fill="x", pady=(0, 4))
        tk.Label(top_row, text="ZAMANLAYICI", font=("Arial", 9, "bold"),
                 bg=self.C["card"], fg=self.C["muted"]).pack(side="left")

        size_frame = tk.Frame(top_row, bg=self.C["card"])
        size_frame.pack(side="left", padx=(12, 0))
        self._btn_small(size_frame, "A−", self._timer_size_down).pack(side="left", padx=1)
        self.lbl_timer_size = tk.Label(size_frame, text=str(self.timer_font_size),
                                       font=("Arial", 9), bg=self.C["card"],
                                       fg=self.C["muted"], width=3)
        self.lbl_timer_size.pack(side="left")
        self._btn_small(size_frame, "A+", self._timer_size_up).pack(side="left", padx=1)

        self.btn_color = tk.Button(top_row, text="🎨  Tema & Renkler",
                                   font=("Arial", 9, "bold"),
                                   bg=self.C["btn_bg"], fg=self.C["text"],
                                   relief="flat", bd=0, padx=8, pady=3,
                                   cursor="hand2", command=self._toggle_color_panel)
        self.btn_color.pack(side="right")
        self.btn_color.bind("<Enter>", lambda e: self.btn_color.config(bg=self.C["accent"]))
        self.btn_color.bind("<Leave>", lambda e: self.btn_color.config(bg=self.C["btn_bg"]))

        self.lbl_time = tk.Label(inner, text="25:00",
                                 font=("Courier New", 68, "bold"),
                                 bg=self.C["card"], fg=self.C["timer_fg"], cursor="hand2")
        self.lbl_time.pack(pady=(4, 0))
        self.lbl_time.bind("<Button-1>", lambda e: self._ask_custom())

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("T.Horizontal.TProgressbar",
                        troughcolor=self.C["entry_bg"], background=self.C["accent"],
                        thickness=5, borderwidth=0)
        self.progress = ttk.Progressbar(inner, orient="horizontal",
                                        mode="determinate", style="T.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(8, 12))
        self.progress["maximum"] = 100
        self.progress["value"]   = 100

        row = tk.Frame(inner, bg=self.C["card"])
        row.pack()
        self.btn_start = self._btn(row, "▶  Başlat", self._toggle, primary=True)
        self.btn_start.pack(side="left", padx=(0, 8))
        self._btn(row, "↺  Sıfırla", self._reset).pack(side="left")

        self.btn_display = self._btn(inner, "📺  Ekranda Göster", self._show_display_menu)
        self.btn_display.pack(pady=(10, 0))

        preset_row = tk.Frame(inner, bg=self.C["card"])
        preset_row.pack(pady=(10, 0))
        tk.Label(preset_row, text="Hızlı:", font=("Arial", 10),
                 bg=self.C["card"], fg=self.C["muted"]).pack(side="left", padx=(0, 6))
        for m in PRESETS:
            lbl = "1 sa" if m == 60 else f"{m} dk"
            b = tk.Button(preset_row, text=lbl, font=("Arial", 10),
                          bg=self.C["btn_bg"], fg=self.C["text"], relief="flat", bd=0,
                          padx=8, pady=3, cursor="hand2",
                          command=lambda x=m: self._set_preset(x))
            b.pack(side="left", padx=2)
            b.bind("<Enter>", lambda e, w=b: w.config(bg=self.C["accent"]))
            b.bind("<Leave>", lambda e, w=b: w.config(bg=self.C["btn_bg"]))

        # Süre ekleme satırı
        add_row = tk.Frame(inner, bg=self.C["card"])
        add_row.pack(pady=(10, 0))
        tk.Label(add_row, text="+ Ekle:", font=("Arial", 10),
                 bg=self.C["card"], fg=self.C["muted"]).pack(side="left", padx=(0, 4))
        for add_m in [1, 5, 10]:
            b = tk.Button(add_row, text=f"+{add_m}dk", font=("Arial", 10),
                          bg=self.C["btn_bg"], fg=self.C["text"], relief="flat", bd=0,
                          padx=6, pady=3, cursor="hand2",
                          command=lambda x=add_m: self._add_time(x))
            b.pack(side="left", padx=2)
            b.bind("<Enter>", lambda e, w=b: w.config(bg=self.C["accent"]))
            b.bind("<Leave>", lambda e, w=b: w.config(bg=self.C["btn_bg"]))

        # Süre düşürme satırı
        sub_row = tk.Frame(inner, bg=self.C["card"])
        sub_row.pack(pady=(6, 0))
        tk.Label(sub_row, text="− Düş:", font=("Arial", 10),
                 bg=self.C["card"], fg=self.C["muted"]).pack(side="left", padx=(0, 4))
        for sub_m in [1, 5, 10]:
            b = tk.Button(sub_row, text=f"−{sub_m}dk", font=("Arial", 10),
                          bg=self.C["btn_bg"], fg=self.C["text"], relief="flat", bd=0,
                          padx=6, pady=3, cursor="hand2",
                          command=lambda x=sub_m: self._sub_time(x))
            b.pack(side="left", padx=2)
            b.bind("<Enter>", lambda e, w=b: w.config(bg=self.C["accent"]))
            b.bind("<Leave>", lambda e, w=b: w.config(bg=self.C["btn_bg"]))

        # Manuel ekleme/düşürme
        manual_row = tk.Frame(inner, bg=self.C["card"])
        manual_row.pack(pady=(6, 0))
        tk.Label(manual_row, text="Manuel:", font=("Arial", 10),
                 bg=self.C["card"], fg=self.C["muted"]).pack(side="left", padx=(0, 4))
        self.add_entry = tk.Entry(manual_row, font=("Arial", 10),
                                  bg=self.C["entry_bg"], fg=self.C["text"],
                                  insertbackground=self.C["text"],
                                  relief="flat", bd=2, width=5, justify="center")
        self.add_entry.pack(side="left", padx=(0, 2))
        self.add_entry.bind("<Return>", lambda e: self._add_manual_time())

        b_clear = tk.Button(manual_row, text="✕", font=("Arial", 10, "bold"),
                            bg=self.C["btn_bg"], fg=self.C["muted"], relief="flat", bd=0,
                            padx=5, pady=3, cursor="hand2",
                            command=lambda: self.add_entry.delete(0, "end"))
        b_clear.pack(side="left", padx=(0, 4))
        b_clear.bind("<Enter>", lambda e: b_clear.config(bg=self.C["accent"], fg=self.C["text"]))
        b_clear.bind("<Leave>", lambda e: b_clear.config(bg=self.C["btn_bg"], fg=self.C["muted"]))

        b_add = tk.Button(manual_row, text="+ Ekle", font=("Arial", 10),
                          bg=self.C["btn_bg"], fg=self.C["text"], relief="flat", bd=0,
                          padx=8, pady=3, cursor="hand2",
                          command=self._add_manual_time)
        b_add.pack(side="left", padx=2)
        b_add.bind("<Enter>", lambda e: b_add.config(bg=self.C["accent"]))
        b_add.bind("<Leave>", lambda e: b_add.config(bg=self.C["btn_bg"]))

        b_sub = tk.Button(manual_row, text="− Düş", font=("Arial", 10),
                          bg=self.C["btn_bg"], fg=self.C["text"], relief="flat", bd=0,
                          padx=8, pady=3, cursor="hand2",
                          command=self._sub_manual_time)
        b_sub.pack(side="left", padx=2)
        b_sub.bind("<Enter>", lambda e: b_sub.config(bg=self.C["accent"]))
        b_sub.bind("<Leave>", lambda e: b_sub.config(bg=self.C["btn_bg"]))

        self.lbl_alert = tk.Label(inner, text="", font=("Arial", 12, "bold"),
                                  bg=self.C["card"], fg=self.C["accent"])
        self.lbl_alert.pack(pady=(8, 0))

    def _build_note_card(self, parent):
        card  = self._card(parent)
        inner = tk.Frame(card, bg=self.C["card"])
        inner.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(inner, text="NOT ALANI", font=("Arial", 9, "bold"),
                 bg=self.C["card"], fg=self.C["muted"]).pack(anchor="w", pady=(0, 8))

        tk.Label(inner, text="Font:", font=("Arial", 10),
                 bg=self.C["card"], fg=self.C["muted"]).pack(anchor="w")
        font_row = tk.Frame(inner, bg=self.C["card"])
        font_row.pack(fill="x", pady=(4, 8))

        self.font_var = tk.StringVar(value="Arial")
        font_menu = ttk.Combobox(font_row, textvariable=self.font_var,
                                 values=FONTS_LIST, state="readonly", width=20)
        font_menu.pack(side="left")
        font_menu.bind("<<ComboboxSelected>>", lambda e: self._apply_font())

        tk.Label(font_row, text="  Boyut:", font=("Arial", 10),
                 bg=self.C["card"], fg=self.C["muted"]).pack(side="left")
        self._btn_small(font_row, "A−", lambda: self._change_size(-1)).pack(side="left", padx=2)
        self.lbl_size = tk.Label(font_row, text="14", font=("Arial", 10),
                                 bg=self.C["card"], fg=self.C["text"], width=3)
        self.lbl_size.pack(side="left")
        self._btn_small(font_row, "A+", lambda: self._change_size(1)).pack(side="left", padx=2)
        tk.Label(font_row, text="  ", bg=self.C["card"]).pack(side="left")
        self.btn_bold   = self._btn_small(font_row, "K", self._toggle_bold)
        self.btn_italic = self._btn_small(font_row, "İ", self._toggle_italic)
        self.btn_bold.pack(side="left", padx=2)
        self.btn_italic.pack(side="left", padx=2)

        tk.Label(inner, text="Not Rengi:", font=("Arial", 10),
                 bg=self.C["card"], fg=self.C["muted"]).pack(anchor="w", pady=(0, 4))
        color_row = tk.Frame(inner, bg=self.C["card"])
        color_row.pack(anchor="w", pady=(0, 8))
        self.color_btns = []
        for hex_ in TEXT_COLORS:
            b = tk.Label(color_row, bg=hex_, width=2, height=1,
                         relief="flat", cursor="hand2")
            b.pack(side="left", padx=3)
            b.bind("<Button-1>", lambda e, c=hex_: self._set_color(c))
            self.color_btns.append(b)

        # Renk ekleme butonu
        self.btn_add_color = tk.Button(color_row, text="+", font=("Arial", 12, "bold"),
                                       bg=self.C["btn_bg"], fg=self.C["text"],
                                       relief="flat", bd=0, padx=6, pady=0,
                                       cursor="hand2", command=self._pick_custom_color)
        self.btn_add_color.pack(side="left", padx=3)
        self.btn_add_color.bind("<Enter>", lambda e: self.btn_add_color.config(bg=self.C["accent"]))
        self.btn_add_color.bind("<Leave>", lambda e: self.btn_add_color.config(bg=self.C["btn_bg"]))

        self._mark_color(self.C["text"])

        self.note_text = tk.Text(inner, font=("Arial", 14),
                                 bg=self.C["entry_bg"], fg=self.C["text"],
                                 insertbackground=self.C["text"],
                                 relief="flat", bd=0, wrap="word", height=8,
                                 padx=10, pady=8)
        self.note_text.pack(fill="both", expand=True, pady=(0, 8))
        self.note_text.bind("<KeyRelease>", self._update_chars)

        footer = tk.Frame(inner, bg=self.C["card"])
        footer.pack(fill="x")
        self.lbl_chars = tk.Label(footer, text="0 karakter", font=("Arial", 10),
                                  bg=self.C["card"], fg=self.C["muted"])
        self.lbl_chars.pack(side="left")
        self._btn(footer, "Kopyala", self._copy_note).pack(side="right", padx=(4, 0))
        self._btn(footer, "Temizle", self._clear_note).pack(side="right", padx=4)

    # ══════════════════════════════════════════════════
    #  Renk paneli aç/kapat
    # ══════════════════════════════════════════════════
    def _toggle_color_panel(self):
        if self.color_panel:
            self.color_panel.close()
        else:
            self.color_panel = ColorPanel(self, self)
            self.btn_color.config(text="✕  Kapat")

    # ══════════════════════════════════════════════════
    #  Yardımcı
    # ══════════════════════════════════════════════════
    def _btn(self, parent, text, cmd, primary=False):
        bg = self.C["accent"] if primary else self.C["btn_bg"]
        b = tk.Button(parent, text=text, font=("Arial", 11, "bold"),
                      bg=bg, fg=self.C["text"], relief="flat", bd=0,
                      padx=14, pady=6, cursor="hand2", command=cmd)
        b.bind("<Enter>", lambda e: b.config(bg=self.C["accent"]))
        b.bind("<Leave>", lambda e: b.config(bg=(self.C["accent"] if primary else self.C["btn_bg"])))
        return b

    def _btn_small(self, parent, text, cmd):
        b = tk.Button(parent, text=text, font=("Arial", 9, "bold"),
                      bg=self.C["btn_bg"], fg=self.C["text"], relief="flat", bd=0,
                      padx=6, pady=2, cursor="hand2", command=cmd)
        b.bind("<Enter>", lambda e: b.config(bg=self.C["accent"]))
        b.bind("<Leave>", lambda e: b.config(bg=self.C["btn_bg"]))
        return b

    # ══════════════════════════════════════════════════
    #  Ekran seçimi
    # ══════════════════════════════════════════════════
    def _show_display_menu(self):
        if self.display_win:
            self.display_win.close_display()
            return
        if len(self.monitors) == 1:
            self._open_display(0)
            return
        win = tk.Toplevel(self)
        win.title("Ekran Seç")
        win.configure(bg=self.C["bg"])
        win.resizable(False, False)
        win.grab_set()
        tk.Label(win, text="Hangi ekranda gösterilsin?",
                 font=("Arial", 13, "bold"), bg=self.C["bg"], fg=self.C["text"]).pack(pady=(22,14), padx=30)
        for i, mon in enumerate(self.monitors):
            lbl = f"  Ekran {i+1}  —  {mon['w']} × {mon['h']}  "
            b = tk.Button(win, text=lbl, font=("Arial", 11),
                          bg=self.C["btn_bg"], fg=self.C["text"], relief="flat", bd=0,
                          padx=14, pady=8, cursor="hand2",
                          command=lambda idx=i: [win.destroy(), self._open_display(idx)])
            b.pack(pady=5, padx=30, fill="x")
            b.bind("<Enter>", lambda e, w=b: w.config(bg=self.C["accent"]))
            b.bind("<Leave>", lambda e, w=b: w.config(bg=self.C["btn_bg"]))
        tk.Label(win, text="ESC ile tam ekrandan çıkılır",
                 font=("Arial", 9), bg=self.C["bg"], fg=self.C["muted"]).pack(pady=(10,16))
        win.update_idletasks()
        w2 = win.winfo_reqwidth(); h2 = win.winfo_reqheight()
        win.geometry(f"{w2}x{h2}+{self.winfo_x()+(self.winfo_width()-w2)//2}+{self.winfo_y()+(self.winfo_height()-h2)//2}")

    def _open_display(self, idx):
        self.display_win = DisplayWindow(self, self.monitors[idx], self)
        self.btn_display.config(text="📺  Ekranı Kapat")
        self._sync_display()

    def _sync_display(self):
        if not self.display_win: return
        m, s = divmod(self.remaining, 60)
        self.display_win.update_time(f"{m:02d}:{s:02d}")
        note = self.note_text.get("1.0", "end-1c")
        self.display_win.update_note(note, self.note_font, self.note_size,
                                     self.note_color, self.bold, self.italic)

    # ══════════════════════════════════════════════════
    #  Timer
    # ══════════════════════════════════════════════════
    def _update_display(self):
        m, s = divmod(self.remaining, 60)
        txt = f"{m:02d}:{s:02d}"
        try: self.lbl_time.config(text=txt)
        except: pass
        pct = (self.remaining / self.total_secs * 100) if self.total_secs else 100
        try: self.progress["value"] = pct
        except: pass
        if self.display_win: self.display_win.update_time(txt)

    def _tick(self):
        if not self.running: return
        self.remaining -= 1
        self._update_display()
        self._update_warning_color()
        if self.remaining <= 0:
            self.running = False
            try: self.btn_start.config(text="▶  Başlat")
            except: pass
            try: self.lbl_alert.config(text="⏰  Süre doldu!")
            except: pass
            if self.display_win: self.display_win.show_alert("⏰  Süre Doldu!")
            self._play_alarm()
            self._show_alert_popup()
            return
        self._job = self.after(1000, self._tick)

    def _update_warning_color(self):
        try:
            if self.remaining <= 60:
                color = "#e94560"  # kırmızı
            elif self.remaining <= 120:
                color = "#ff8c00"  # turuncu
            else:
                color = self.C["timer_fg"]  # normal
            self.lbl_time.config(fg=color)
            if self.display_win:
                self.display_win.lbl_time.config(fg=color)
        except Exception:
            pass

    def _play_alarm(self):
        import threading
        def beep():
            try:
                import winsound
                for _ in range(5):
                    winsound.Beep(880, 300)
                    winsound.Beep(660, 200)
            except Exception:
                for _ in range(5):
                    self.bell()
        threading.Thread(target=beep, daemon=True).start()

    def _show_alert_popup(self):
        win = tk.Toplevel(self)
        win.title("Süre Doldu!")
        win.configure(bg=self.C["bg"])
        win.resizable(False, False)
        win.attributes("-topmost", True)

        # Yanıp sönen çerçeve efekti
        win.configure(highlightthickness=3, highlightbackground=self.C["accent"])

        tk.Label(win, text="⏰", font=("Arial", 48),
                 bg=self.C["bg"]).pack(pady=(24, 0))
        tk.Label(win, text="SÜRE DOLDU!", font=("Arial", 22, "bold"),
                 bg=self.C["bg"], fg=self.C["accent"]).pack(pady=(8, 4))
        tk.Label(win, text="Zamanlayıcı tamamlandı.",
                 font=("Arial", 12), bg=self.C["bg"], fg=self.C["muted"]).pack(pady=(0, 16))

        btn = tk.Button(win, text="Tamam", font=("Arial", 13, "bold"),
                        bg=self.C["accent"], fg=self.C["text"], relief="flat", bd=0,
                        padx=24, pady=8, cursor="hand2", command=win.destroy)
        btn.pack(pady=(0, 24))

        win.update_idletasks()
        w = win.winfo_reqwidth()
        h = win.winfo_reqheight()
        x = self.winfo_x() + (self.winfo_width() - w) // 2
        y = self.winfo_y() + (self.winfo_height() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

        # Yanıp sönme efekti
        self._blink_popup(win, 0)

    def _blink_popup(self, win, count):
        if count >= 10 or not win.winfo_exists():
            try: win.configure(highlightbackground=self.C["accent"])
            except: pass
            return
        color = self.C["accent"] if count % 2 == 0 else self.C["bg"]
        try:
            win.configure(highlightbackground=color)
            self.after(300, lambda: self._blink_popup(win, count + 1))
        except Exception:
            pass

    def _add_time(self, mins):
        self.remaining += mins * 60
        self.total_secs += mins * 60
        self._update_display()
        try:
            self.lbl_alert.config(text=f"+{mins} dk eklendi!")
            self.after(1500, lambda: self.lbl_alert.config(text=""))
        except Exception:
            pass

    def _add_manual_time(self):
        try:
            val = self.add_entry.get().strip()
            mins = int(val)
            if mins > 0:
                self._add_time(mins)
                self.add_entry.delete(0, "end")
        except ValueError:
            pass

    def _sub_time(self, mins):
        self.remaining = max(1, self.remaining - mins * 60)
        self.total_secs = max(1, self.total_secs - mins * 60)
        self._update_display()
        try:
            self.lbl_alert.config(text=f"−{mins} dk düşürüldü!")
            self.after(1500, lambda: self.lbl_alert.config(text=""))
        except Exception:
            pass

    def _sub_manual_time(self):
        try:
            val = self.add_entry.get().strip()
            mins = int(val)
            if mins > 0:
                self._sub_time(mins)
                self.add_entry.delete(0, "end")
        except ValueError:
            pass

    def _toggle(self):
        if self.running:
            self.running = False
            if self._job: self.after_cancel(self._job)
            self.btn_start.config(text="▶  Devam")
        else:
            if self.remaining <= 0: return
            self.lbl_alert.config(text="")
            if self.display_win: self.display_win.show_alert("")
            self.running = True
            self.btn_start.config(text="⏸  Duraklat")
            self._tick()

    def _reset(self):
        self.running = False
        if self._job: self.after_cancel(self._job)
        self.remaining = self.total_secs
        self._update_display()
        self.lbl_alert.config(text="")
        if self.display_win: self.display_win.show_alert("")
        self.btn_start.config(text="▶  Başlat")
        try:
            self.lbl_time.config(fg=self.C["timer_fg"])
            if self.display_win: self.display_win.lbl_time.config(fg=self.C["timer_fg"])
        except: pass

    def _set_preset(self, mins):
        self.running = False
        if self._job: self.after_cancel(self._job)
        self.total_secs = mins * 60
        self.remaining  = self.total_secs
        self._update_display()
        self.lbl_alert.config(text="")
        if self.display_win: self.display_win.show_alert("")
        self.btn_start.config(text="▶  Başlat")

    def _ask_custom(self):
        if self.running: return
        win = tk.Toplevel(self)
        win.title("Süre Gir")
        win.geometry("300x160")
        win.configure(bg=self.C["bg"])
        win.resizable(False, False)

        tk.Label(win, text="Süre girin (SS:DD)", font=("Arial", 12),
                 bg=self.C["bg"], fg=self.C["text"]).pack(pady=(16, 4))

        row = tk.Frame(win, bg=self.C["bg"])
        row.pack()

        cur_h = self.remaining // 3600
        cur_m = (self.remaining % 3600) // 60

        # Saat
        h_var = tk.StringVar(value=f"{cur_h:02d}")
        h_entry = tk.Entry(row, textvariable=h_var, font=("Courier New", 20),
                           bg=self.C["entry_bg"], fg=self.C["text"],
                           insertbackground=self.C["text"],
                           justify="center", relief="flat", bd=4, width=4)
        h_entry.pack(side="left")

        tk.Label(row, text=":", font=("Courier New", 22, "bold"),
                 bg=self.C["bg"], fg=self.C["text"]).pack(side="left", padx=4)

        # Dakika
        m_var = tk.StringVar(value=f"{cur_m:02d}")
        m_entry = tk.Entry(row, textvariable=m_var, font=("Courier New", 20),
                           bg=self.C["entry_bg"], fg=self.C["text"],
                           insertbackground=self.C["text"],
                           justify="center", relief="flat", bd=4, width=4)
        m_entry.pack(side="left")

        tk.Label(win, text="saat  :  dakika", font=("Arial", 9),
                 bg=self.C["bg"], fg=self.C["muted"]).pack(pady=(4, 0))

        h_entry.focus()

        def confirm(e=None):
            try:
                h = int(h_var.get())
                m = int(m_var.get())
                total = h * 60 + m
                if total > 0:
                    self._set_preset(total)
            except ValueError:
                pass
            win.destroy()

        h_entry.bind("<Return>", confirm)
        m_entry.bind("<Return>", confirm)

        tk.Button(win, text="Tamam", font=("Arial", 11, "bold"),
                  bg=self.C["accent"], fg=self.C["text"], relief="flat", bd=0,
                  padx=12, pady=4, command=confirm).pack(pady=10)

    # ══════════════════════════════════════════════════
    #  Not
    # ══════════════════════════════════════════════════
    def _pick_custom_color(self):
        color = colorchooser.askcolor(title="Not rengi seç")
        if color and color[1]:
            hex_ = color[1]
            # Renk zaten listede varsa sadece seç
            for b in self.color_btns:
                if b["bg"].lower() == hex_.lower():
                    self._set_color(hex_)
                    return
            # Yeni renk kutusu ekle
            b = tk.Label(self.color_btns[0].master, bg=hex_, width=2, height=1,
                         relief="flat", cursor="hand2")
            b.pack(side="left", padx=3, before=self.btn_add_color)
            b.bind("<Button-1>", lambda e, c=hex_: self._set_color(c))
            self.color_btns.append(b)
            self._set_color(hex_)

    def _apply_font(self):
        self.note_font = self.font_var.get()
        self._refresh_note_font()

    def _refresh_note_font(self):
        f = font.Font(family=self.note_font, size=self.note_size,
                      weight="bold" if self.bold else "normal",
                      slant="italic" if self.italic else "roman")
        self.note_text.config(font=f, fg=self.note_color)
        self._sync_display()

    def _change_size(self, d):
        self.note_size = max(9, min(36, self.note_size + d))
        self.lbl_size.config(text=str(self.note_size))
        self._refresh_note_font()

    def _set_color(self, c):
        self.note_color = c
        self._mark_color(c)
        self._refresh_note_font()

    def _mark_color(self, c):
        for b in self.color_btns:
            b.config(relief="sunken" if b["bg"] == c else "flat")

    def _toggle_bold(self):
        self.bold = not self.bold
        self.btn_bold.config(bg=self.C["accent"] if self.bold else self.C["btn_bg"])
        self._refresh_note_font()

    def _toggle_italic(self):
        self.italic = not self.italic
        self.btn_italic.config(bg=self.C["accent"] if self.italic else self.C["btn_bg"])
        self._refresh_note_font()

    def _copy_note(self):
        content = self.note_text.get("1.0", "end-1c")
        if content.strip():
            self.clipboard_clear(); self.clipboard_append(content)
            messagebox.showinfo("Kopyalandı", "Not panoya kopyalandı!")

    def _clear_note(self):
        if self.note_text.get("1.0", "end-1c").strip():
            if messagebox.askyesno("Temizle", "Notu silmek istiyor musun?"):
                self.note_text.delete("1.0", "end")
                self.lbl_chars.config(text="0 karakter")
                self._sync_display()

    def _update_chars(self, e=None):
        n = len(self.note_text.get("1.0", "end-1c"))
        self.lbl_chars.config(text=f"{n} karakter")
        self._sync_display()


if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()
