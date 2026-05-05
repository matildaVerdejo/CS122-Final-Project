import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from data_analysis import compute_magnitude_stats, compute_frequency_trend
from data_visualization import build_results_figure

class ResultsWindow:
    def __init__(self, root, earthquakes):
        self.window = tk.Toplevel(root)
        self.window.title("FaultLine: Results")
        self.window.resizable(True, True)
        self.earthquakes = earthquakes

        self._build_ui()

    def _build_ui(self):
        # title
        tk.Label(
            self.window,
            text="Earthquake Results",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(20, 4))

        tk.Label(
            self.window,
            text=f"{len(self.earthquakes)} event(s) found",
            font=("Helvetica", 10),
            fg="gray"
        ).grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # stats panel
        self._build_stats_panel()

        # charts
        self._build_charts()

        # table
        self._build_table()

        # buttons
        self._build_buttons()

    def _build_stats_panel(self):
        stats = compute_magnitude_stats(self.earthquakes)

        if not stats:
            return
        
        frame = tk.LabelFrame(
            self.window,
            text="Magnitude Statistics",
            font=("Helvetica", 11, "bold"),
            padx=10, pady=8
        )
        frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")

        fields = [
            ("Count", str(stats["count"])),
            ("Mean", f"{stats['mean']:.2f}"),
            ("Median", f"{stats['median']:.2f}"),
            ("Std Dev", f"{stats['std_dev']:.2f}"),
            ("Min", f"{stats['min']:.1f}"),
            ("Max", f"{stats['max']:.1f}"),
        ]
        
        for col, (label, value) in enumerate(fields):
            cell = tk.Frame(frame)
            cell.grid(row=0, column=col, padx=16, pady=4)
            tk.Label(cell, text=value, font=("Helvetica", 14, "bold"), fg="darkblue").pack()
            tk.Label(cell, text=label, font=("Helvetica", 9), fg="gray").pack()

    def _build_charts(self):
        freq_data = compute_frequency_trend(self.earthquakes)
        fig = build_results_figure(self.earthquakes, freq_data)
        if fig is None:
            return
        
        frame = tk.Frame(self.window)
        frame.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _build_table(self):
        frame = tk.LabelFrame(
            self.window,
            text="Event List",
            font=("Helvetica", 11, "bold"),
            padx=10, pady=8
        )
        frame.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="nsew")
        self.window.rowconfigure(4, weight=1)
        self.window.columnconfigure(0, weight=1)
        columns = ("Time (UTC)", "Location", "Magnitude", "Depth (km)", "Lat", "Lon")

        tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        widths = [145, 280, 80, 85, 75, 80]
        for col, w in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="w" if col == "Location" else "center")

        for eq in self.earthquakes:
            tree.insert("", "end", values=(
                eq.get("time", "—"),
                eq.get("location", "—"),
                f"{eq['magnitude']:.1f}" if eq.get("magnitude") is not None else "—",
                f"{eq['depth_km']:.1f}"  if eq.get("depth_km")  is not None else "—",
                f"{eq['latitude']:.3f}"  if eq.get("latitude")  is not None else "—",
                f"{eq['longitude']:.3f}" if eq.get("longitude") is not None else "—",
            ))

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def _build_buttons(self):
        frame = tk.Frame(self.window)
        frame.grid(row=5, column=0, columnspan=2, pady=(4, 16))

        tk.Button(
            frame,
            text="Close",
            font=("Helvetica", 11),
            bg="darkblue",
            fg="white",
            padx=16, pady=6,
            command=self.window.destroy
        ).pack()


