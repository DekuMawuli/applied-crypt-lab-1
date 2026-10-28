"""tkinter front end. The only module that imports tkinter."""
import os
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cipher


class App:
    def __init__(self, root):
        self.root = root
        root.title("Lab 1 - LFSR + Permutation Cipher")
        self.mode = tk.StringVar(value="encrypt")
        self.in_path = tk.StringVar()
        self.out_path = tk.StringVar()
        self.status = tk.StringVar(value="Idle")
        self.q = queue.Queue()
        self.last_suggest = ""
        self.mode.trace_add("write", lambda *a: self.refresh_suggestion())

        f = ttk.Frame(root, padding=12)
        f.grid(sticky="nsew")
        root.columnconfigure(0, weight=1)
        f.columnconfigure(1, weight=1)

        ttk.Radiobutton(f, text="Encrypt", variable=self.mode, value="encrypt").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(f, text="Decrypt", variable=self.mode, value="decrypt").grid(row=0, column=1, sticky="w")
        ttk.Label(f, text="Input file:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(f, textvariable=self.in_path, width=50).grid(row=1, column=1, sticky="ew")
        ttk.Button(f, text="Browse...", command=self.browse_in).grid(row=1, column=2, padx=4)
        ttk.Label(f, text="Output file:").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(f, textvariable=self.out_path, width=50).grid(row=2, column=1, sticky="ew")
        ttk.Button(f, text="Browse...", command=self.browse_out).grid(row=2, column=2, padx=4)
        self.start_btn = ttk.Button(f, text="Start", command=self.start)
        self.start_btn.grid(row=3, column=0, pady=8, sticky="w")
        self.bar = ttk.Progressbar(f, maximum=100, mode="determinate")
        self.bar.grid(row=4, column=0, columnspan=3, sticky="ew")
        ttk.Label(f, textvariable=self.status).grid(row=5, column=0, columnspan=3, sticky="w", pady=4)

    def browse_in(self):
        p = filedialog.askopenfilename()
        if p:
            self.in_path.set(p)
            self.refresh_suggestion()

    def browse_out(self):
        p = filedialog.asksaveasfilename(initialfile=os.path.basename(self.out_path.get()))
        if p:
            self.out_path.set(p)

    def refresh_suggestion(self):
        """Update the output path unless the user has typed or chosen their own."""
        src = self.in_path.get().strip()
        cur = self.out_path.get()
        if src and (not cur or cur == self.last_suggest):
            self.last_suggest = self.suggest(src)
            self.out_path.set(self.last_suggest)

    def suggest(self, p):
        if self.mode.get() == "encrypt":
            return p + ".enc"
        return p[:-4] if p.endswith(".enc") else p + ".dec"

    def start(self):
        src, dst = self.in_path.get().strip(), self.out_path.get().strip()
        if not src or not os.path.isfile(src):
            return messagebox.showerror("Error", "Choose an existing input file.")
        if not dst:
            return messagebox.showerror("Error", "Specify an output file.")
        if os.path.exists(dst) and os.path.samefile(src, dst):
            return messagebox.showerror("Error", "Output file must differ from the input file.")
        if os.path.exists(dst) and not messagebox.askyesno("Overwrite?", f"{dst} exists. Overwrite it?"):
            return
        self.start_btn.state(["disabled"])
        self.bar["value"] = 0
        self.status.set("Running...")
        threading.Thread(target=self.work, args=(src, dst, self.mode.get()), daemon=True).start()
        self.root.after(50, self.poll)

    def work(self, src, dst, mode):
        try:
            n = cipher.process(src, dst, mode, progress=lambda d, t: self.q.put(("p", d, t)))
            self.q.put(("done", n, dst))
        except Exception as e:
            self.q.put(("err", str(e)))

    def poll(self):
        finished = False
        while True:
            try:
                msg = self.q.get_nowait()
            except queue.Empty:
                break
            if msg[0] == "p":
                _, d, t = msg
                self.bar["value"] = 100 * d / t if t else 100
                self.status.set(f"Running... {d} of {t} bytes")
            elif msg[0] == "done":
                self.bar["value"] = 100
                self.status.set(f"Done: {msg[1]} bytes written to {msg[2]}")
                finished = True
            else:
                self.status.set("Error: " + msg[1])
                messagebox.showerror("Error", msg[1])
                finished = True
        if finished:
            self.start_btn.state(["!disabled"])
        else:
            self.root.after(50, self.poll)
