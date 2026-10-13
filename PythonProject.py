
"""
Time Utility Studio
Digital Clock + Countdown Timer + Stopwatch
Experiential Learning Mini Project

Requirements: Python 3.x
Run: python time_utility_app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time


class TimeUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Utility Studio")
        self.root.geometry("620x520")
        self.root.minsize(560, 470)
        self.root.configure(bg="#101827")

        self.clock_job = None
        self.timer_job = None
        self.stopwatch_job = None

        self.remaining = 0
        self.timer_running = False

        self.elapsed = 0.0
        self.stopwatch_start = None
        self.stopwatch_running = False

        self.setup_style()
        self.build_interface()
        self.update_clock()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TNotebook",
            background="#101827",
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            background="#253247",
            foreground="#ffffff",
            padding=(18, 10),
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "#ffffff")]
        )
        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

    def build_interface(self):
        header = tk.Frame(self.root, bg="#101827")
        header.pack(fill="x", padx=24, pady=(20, 8))

        tk.Label(
            header,
            text="TIME UTILITY STUDIO",
            font=("Segoe UI", 20, "bold"),
            fg="#f8fafc",
            bg="#101827"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Digital Clock | Countdown | Stopwatch",
            font=("Segoe UI", 10),
            fg="#9fb0c8",
            bg="#101827"
        ).pack(anchor="w", pady=4)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=24, pady=14)

        self.clock_tab = tk.Frame(notebook, bg="#172235")
        self.timer_tab = tk.Frame(notebook, bg="#172235")
        self.stopwatch_tab = tk.Frame(notebook, bg="#172235")

        notebook.add(self.clock_tab, text="Digital Clock")
        notebook.add(self.timer_tab, text="Countdown")
        notebook.add(self.stopwatch_tab, text="Stopwatch")

        self.build_clock()
        self.build_timer()
        self.build_stopwatch()

        tk.Label(
            self.root,
            text="Python | Tkinter | Event-driven GUI",
            font=("Segoe UI", 9),
            fg="#71829b",
            bg="#101827"
        ).pack(pady=(0, 12))

    # ---------------- DIGITAL CLOCK ----------------

    def build_clock(self):
        tk.Label(
            self.clock_tab,
            text="CURRENT LOCAL TIME",
            font=("Segoe UI", 11, "bold"),
            fg="#9fb0c8",
            bg="#172235"
        ).pack(pady=(45, 10))

        self.clock_display = tk.Label(
            self.clock_tab,
            text="00:00:00",
            font=("Consolas", 42, "bold"),
            fg="#60a5fa",
            bg="#172235"
        )
        self.clock_display.pack()

        self.date_display = tk.Label(
            self.clock_tab,
            text="",
            font=("Segoe UI", 13),
            fg="#e5edf8",
            bg="#172235"
        )
        self.date_display.pack(pady=8)

    def update_clock(self):
        now = datetime.now()

        self.clock_display.config(
            text=now.strftime("%H:%M:%S")
        )
        self.date_display.config(
            text=now.strftime("%A, %d %B %Y")
        )

        self.clock_job = self.root.after(
            250, self.update_clock
        )

    # ---------------- COUNTDOWN TIMER ----------------

    def build_timer(self):
        tk.Label(
            self.timer_tab,
            text="SET COUNTDOWN DURATION",
            font=("Segoe UI", 11, "bold"),
            fg="#9fb0c8",
            bg="#172235"
        ).pack(pady=(24, 10))

        input_frame = tk.Frame(
            self.timer_tab, bg="#172235"
        )
        input_frame.pack()

        self.minutes_var = tk.StringVar(value="1")
        self.seconds_var = tk.StringVar(value="0")

        tk.Label(
            input_frame,
            text="Minutes",
            fg="white",
            bg="#172235"
        ).grid(row=0, column=0, padx=8, pady=4)

        tk.Label(
            input_frame,
            text="Seconds",
            fg="white",
            bg="#172235"
        ).grid(row=0, column=1, padx=8, pady=4)

        ttk.Entry(
            input_frame,
            textvariable=self.minutes_var,
            width=10,
            justify="center"
        ).grid(row=1, column=0, padx=8)

        ttk.Entry(
            input_frame,
            textvariable=self.seconds_var,
            width=10,
            justify="center"
        ).grid(row=1, column=1, padx=8)

        self.timer_display = tk.Label(
            self.timer_tab,
            text="01:00",
            font=("Consolas", 38, "bold"),
            fg="#34d399",
            bg="#172235"
        )
        self.timer_display.pack(pady=20)

        buttons = tk.Frame(
            self.timer_tab, bg="#172235"
        )
        buttons.pack()

        ttk.Button(
            buttons, text="Start",
            command=self.start_timer
        ).grid(row=0, column=0, padx=4)

        ttk.Button(
            buttons, text="Pause",
            command=self.pause_timer
        ).grid(row=0, column=1, padx=4)

        ttk.Button(
            buttons, text="Resume",
            command=self.resume_timer
        ).grid(row=0, column=2, padx=4)

        ttk.Button(
            buttons, text="Reset",
            command=self.reset_timer
        ).grid(row=0, column=3, padx=4)

        self.timer_status = tk.Label(
            self.timer_tab,
            text="Ready",
            font=("Segoe UI", 10),
            fg="#9fb0c8",
            bg="#172235"
        )
        self.timer_status.pack(pady=10)

    @staticmethod
    def format_timer(seconds):
        minutes, seconds = divmod(max(0, seconds), 60)
        hours, minutes = divmod(minutes, 60)

        if hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        return f"{minutes:02d}:{seconds:02d}"

    def start_timer(self):
        self.cancel_timer_job()

        try:
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())

            if minutes < 0 or not 0 <= seconds <= 59:
                raise ValueError

            total = minutes * 60 + seconds

            if total <= 0:
                messagebox.showwarning(
                    "Invalid Duration",
                    "Enter a duration greater than zero."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter non-negative whole minutes and seconds from 0 to 59."
            )
            return

        self.remaining = total
        self.timer_running = True
        self.timer_status.config(text="Countdown running")
        self.tick_timer()

    def tick_timer(self):
        self.timer_display.config(
            text=self.format_timer(self.remaining)
        )

        if self.remaining <= 0:
            self.timer_running = False
            self.timer_job = None
            self.timer_status.config(text="Completed")
            self.root.bell()

            messagebox.showinfo(
                "Time's Up!",
                "Your countdown has finished."
            )
            return

        self.remaining -= 1
        self.timer_job = self.root.after(
            1000, self.tick_timer
        )

    def pause_timer(self):
        if self.timer_running:
            self.cancel_timer_job()
            self.timer_running = False
            self.timer_status.config(text="Paused")

    def resume_timer(self):
        if not self.timer_running and self.remaining > 0:
            self.timer_running = True
            self.timer_status.config(text="Countdown running")
            self.tick_timer()

    def reset_timer(self):
        self.cancel_timer_job()
        self.timer_running = False

        try:
            minutes = max(0, int(self.minutes_var.get()))
            seconds = int(self.seconds_var.get())

            if not 0 <= seconds <= 59:
                seconds = 0

            self.remaining = minutes * 60 + seconds

        except ValueError:
            self.remaining = 0

        self.timer_display.config(
            text=self.format_timer(self.remaining)
        )
        self.timer_status.config(text="Ready")

    def cancel_timer_job(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    # ---------------- STOPWATCH ----------------

    def build_stopwatch(self):
        tk.Label(
            self.stopwatch_tab,
            text="ELAPSED TIME",
            font=("Segoe UI", 11, "bold"),
            fg="#9fb0c8",
            bg="#172235"
        ).pack(pady=(45, 10))

        self.stopwatch_display = tk.Label(
            self.stopwatch_tab,
            text="00:00.00",
            font=("Consolas", 40, "bold"),
            fg="#fbbf24",
            bg="#172235"
        )
        self.stopwatch_display.pack(pady=10)

        buttons = tk.Frame(
            self.stopwatch_tab, bg="#172235"
        )
        buttons.pack(pady=14)

        ttk.Button(
            buttons, text="Start",
            command=self.start_stopwatch
        ).grid(row=0, column=0, padx=6)

        ttk.Button(
            buttons, text="Pause",
            command=self.pause_stopwatch
        ).grid(row=0, column=1, padx=6)

        ttk.Button(
            buttons, text="Reset",
            command=self.reset_stopwatch
        ).grid(row=0, column=2, padx=6)

    @staticmethod
    def format_stopwatch(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        hundredths = int((seconds % 1) * 100)

        if hours:
            return (
                f"{int(hours):02d}:"
                f"{int(minutes):02d}:"
                f"{int(seconds):02d}.{hundredths:02d}"
            )

        return (
            f"{int(minutes):02d}:"
            f"{int(seconds):02d}.{hundredths:02d}"
        )

    def start_stopwatch(self):
        if self.stopwatch_running:
            return

        self.stopwatch_running = True
        self.stopwatch_start = time.perf_counter()
        self.tick_stopwatch()

    def tick_stopwatch(self):
        if not self.stopwatch_running:
            return

        elapsed = (
            self.elapsed
            + time.perf_counter() - self.stopwatch_start
        )

        self.stopwatch_display.config(
            text=self.format_stopwatch(elapsed)
        )

        self.stopwatch_job = self.root.after(
            30, self.tick_stopwatch
        )

    def pause_stopwatch(self):
        if self.stopwatch_running:
            self.elapsed += (
                time.perf_counter() - self.stopwatch_start
            )
            self.stopwatch_running = False

            if self.stopwatch_job is not None:
                self.root.after_cancel(self.stopwatch_job)
                self.stopwatch_job = None

            self.stopwatch_display.config(
                text=self.format_stopwatch(self.elapsed)
            )

    def reset_stopwatch(self):
        self.stopwatch_running = False

        if self.stopwatch_job is not None:
            self.root.after_cancel(self.stopwatch_job)
            self.stopwatch_job = None

        self.elapsed = 0.0
        self.stopwatch_start = None
        self.stopwatch_display.config(text="00:00.00")

    # ---------------- CLOSE APPLICATION ----------------

    def close_app(self):
        for job in (
            self.clock_job,
            self.timer_job,
            self.stopwatch_job
        ):
            if job is not None:
                try:
                    self.root.after_cancel(job)
                except tk.TclError:
                    pass

        self.root.destroy()


def main():
    root = tk.Tk()
    TimeUtilityApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
