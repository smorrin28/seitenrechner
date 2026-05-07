import tkinter as tk
from tkinter import messagebox


def parse_page_ranges(text: str) -> set[int]:
    pages: set[int] = set()
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            halves = part.split("-", 1)
            try:
                start, end = int(halves[0].strip()), int(halves[1].strip())
            except ValueError:
                raise ValueError(f"Ungültiger Bereich: '{part}'")
            if start > end:
                raise ValueError(f"Start größer als Ende: '{part}'")
            if start < 1 or end < 1:
                raise ValueError(f"Seitenzahlen müssen positiv sein: '{part}'")
            pages.update(range(start, end + 1))
        else:
            try:
                n = int(part)
            except ValueError:
                raise ValueError(f"Ungültige Seitenzahl: '{part}'")
            if n < 1:
                raise ValueError(f"Seitenzahlen müssen positiv sein: '{part}'")
            pages.add(n)
    return pages


def berechnen():
    colored_text = entry_colored.get("1.0", tk.END).strip()
    start_text = entry_start.get().strip()
    end_text = entry_end.get().strip()

    if not colored_text:
        messagebox.showerror("Fehler", "Bitte gefärbte Seiten eingeben.")
        return
    if not start_text or not end_text:
        messagebox.showerror(
            "Fehler", "Bitte Start und Ende des Gesamtbereichs eingeben."
        )
        return

    try:
        colored_pages = parse_page_ranges(colored_text)
    except ValueError as e:
        messagebox.showerror("Fehler", str(e))
        return

    try:
        total_start = int(start_text)
        total_end = int(end_text)
    except ValueError:
        messagebox.showerror("Fehler", "Start und Ende müssen ganze Zahlen sein.")
        return

    if total_start < 1 or total_end < 1:
        messagebox.showerror("Fehler", "Seitenzahlen müssen positiv sein.")
        return
    if total_start > total_end:
        messagebox.showerror("Fehler", "Start darf nicht größer als Ende sein.")
        return

    total_pages = set(range(total_start, total_end + 1))

    out_of_range = colored_pages - total_pages
    if out_of_range:
        sample = sorted(out_of_range)[:5]
        sample_str = ", ".join(str(p) for p in sample)
        if len(out_of_range) > 5:
            sample_str += ", …"
        messagebox.showwarning(
            "Hinweis",
            f"Einige gefärbte Seiten liegen außerhalb des Gesamtbereichs:\n{sample_str}",
        )

    complement = sorted(total_pages - colored_pages)

    text_output.config(state=tk.NORMAL)
    text_output.delete("1.0", tk.END)
    if complement:
        text_output.insert(tk.END, ",".join(str(p) for p in complement))
    else:
        text_output.insert(tk.END, "(Alle Seiten sind gefärbt)")
    text_output.config(state=tk.DISABLED)

    lbl_count.config(text=f"Anzahl ungefärbter Seiten: {len(complement)}")
    btn_copy.config(state=tk.NORMAL)


def kopieren():
    result = text_output.get("1.0", tk.END).strip()
    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        lbl_copy_hint.config(text="✓ Kopiert!")
        root.after(2000, lambda: lbl_copy_hint.config(text=""))


if __name__ == "__main__":
    # ── Window setup ──────────────────────────────────────────────────────────

    root = tk.Tk()
    root.title("Seitenrechner")
    root.resizable(True, True)
    root.minsize(480, 460)

    FONT = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")
    FONT_MONO = ("Consolas", 9)
    PAD = 10

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame = tk.Frame(root, padx=PAD * 2, pady=PAD * 2)
    frame.grid(sticky="nsew")
    frame.columnconfigure(0, weight=1)

    row = 0

    # ── Colored pages input ───────────────────────────────────────────────────

    tk.Label(frame, text="Gefärbte Seiten:", font=FONT_BOLD, anchor="w").grid(
        row=row, column=0, sticky="w", pady=(0, 2)
    )
    row += 1
    tk.Label(
        frame,
        text="Bereiche und Einzelseiten, kommagetrennt  (z. B. 2-7, 11, 14)",
        font=("Segoe UI", 8),
        fg="grey",
        anchor="w",
    ).grid(row=row, column=0, sticky="w")
    row += 1

    colored_frame = tk.Frame(frame, bd=1, relief=tk.SOLID)
    colored_frame.grid(row=row, column=0, sticky="ew", pady=(2, PAD))
    colored_frame.columnconfigure(0, weight=1)

    entry_colored = tk.Text(colored_frame, height=3, font=FONT_MONO, wrap=tk.WORD, bd=0)
    entry_colored.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
    scrollbar_colored = tk.Scrollbar(colored_frame, command=entry_colored.yview)
    scrollbar_colored.grid(row=0, column=1, sticky="ns")
    entry_colored.config(yscrollcommand=scrollbar_colored.set)
    row += 1

    # ── Total range input ─────────────────────────────────────────────────────

    tk.Label(frame, text="Gesamtbereich:", font=FONT_BOLD, anchor="w").grid(
        row=row, column=0, sticky="w", pady=(0, 2)
    )
    row += 1

    range_frame = tk.Frame(frame)
    range_frame.grid(row=row, column=0, sticky="w", pady=(2, PAD))

    tk.Label(range_frame, text="Von:", font=FONT).pack(side=tk.LEFT)
    entry_start = tk.Entry(range_frame, font=FONT_MONO, width=8)
    entry_start.pack(side=tk.LEFT, padx=(4, 12))
    entry_start.insert(0, "1")

    tk.Label(range_frame, text="Bis:", font=FONT).pack(side=tk.LEFT)
    entry_end = tk.Entry(range_frame, font=FONT_MONO, width=8)
    entry_end.pack(side=tk.LEFT, padx=(4, 0))
    entry_end.insert(0, "100")

    row += 1

    # ── Calculate button ──────────────────────────────────────────────────────

    btn_calc = tk.Button(
        frame,
        text="Berechnen",
        font=FONT_BOLD,
        command=berechnen,
        padx=16,
        pady=6,
        cursor="hand2",
    )
    btn_calc.grid(row=row, column=0, pady=(0, PAD))
    row += 1

    # ── Result ────────────────────────────────────────────────────────────────

    result_header = tk.Frame(frame)
    result_header.grid(row=row, column=0, sticky="ew")
    result_header.columnconfigure(0, weight=1)

    tk.Label(
        result_header, text="Ergebnis (ungefärbte Seiten):", font=FONT_BOLD, anchor="w"
    ).grid(row=0, column=0, sticky="w")
    lbl_copy_hint = tk.Label(result_header, text="", font=("Segoe UI", 9), fg="#107c10")
    lbl_copy_hint.grid(row=0, column=1, sticky="e")
    row += 1

    output_frame = tk.Frame(frame, bd=1, relief=tk.SOLID)
    output_frame.grid(row=row, column=0, sticky="nsew", pady=(2, 4))
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)
    frame.rowconfigure(row, weight=1)

    text_output = tk.Text(
        output_frame,
        height=5,
        font=FONT_MONO,
        wrap=tk.WORD,
        bd=0,
        state=tk.DISABLED,
    )
    text_output.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
    scrollbar_out = tk.Scrollbar(output_frame, command=text_output.yview)
    scrollbar_out.grid(row=0, column=1, sticky="ns")
    text_output.config(yscrollcommand=scrollbar_out.set)
    row += 1

    # ── Footer row: count + copy button ──────────────────────────────────────

    footer = tk.Frame(frame)
    footer.grid(row=row, column=0, sticky="ew", pady=(0, 4))
    footer.columnconfigure(0, weight=1)

    lbl_count = tk.Label(footer, text="", font=("Segoe UI", 9), fg="grey", anchor="w")
    lbl_count.grid(row=0, column=0, sticky="w")

    btn_copy = tk.Button(
        footer,
        text="In Zwischenablage kopieren",
        font=FONT,
        command=kopieren,
        relief=tk.FLAT,
        bg="#e1e1e1",
        activebackground="#c8c8c8",
        padx=10,
        pady=4,
        cursor="hand2",
        state=tk.DISABLED,
    )
    btn_copy.grid(row=0, column=1, sticky="e")

    # ── Keyboard shortcuts ────────────────────────────────────────────────────

    root.bind("<Return>", lambda _: berechnen())
    entry_start.bind("<Return>", lambda _: berechnen())
    entry_end.bind("<Return>", lambda _: berechnen())

    root.mainloop()
