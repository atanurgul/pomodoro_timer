import tkinter as tk
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Constants
FONT_NAME = "Segoe UI"
WORK_MIN = 25  # Çalışma süresi: 1 dakika
SHORT_BREAK_MIN = 5  # Kısa mola süresi: 5 dakika
LONG_BREAK_MIN = 20  # Uzun mola süresi: 20 dakika

# Colors
TOMATO_RED = "#FFC080"
GREEN = "#34C759"
YELLOW = "#F7DC6F"
DARK_GREY = "#333333"

class PomodoroTimer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pomodoro Timer")
        self.window.config(padx=20, pady=20, bg=DARK_GREY)
        self.reps = 0
        self.timer = None
        self.running = False
        self.paused = False
        self.break_time = False
        self.count = 0

        # Header
        self.header_frame = tk.Frame(self.window, bg=DARK_GREY)
        self.header_frame.pack(fill="x")
        self.timer_label = tk.Label(self.header_frame, text="Pomodoro Timer", bg=DARK_GREY, fg=TOMATO_RED, font=(FONT_NAME, 24, "bold"))
        self.timer_label.pack(pady=10)
        self.session_type_label = tk.Label(self.header_frame, text="", bg=DARK_GREY, fg="white", font=(FONT_NAME, 18))
        self.session_type_label.pack(pady=10)

        # Timer
        self.timer_frame = tk.Frame(self.window, bg=DARK_GREY)
        self.timer_frame.pack(fill="x")
        self.canvas = tk.Canvas(self.timer_frame, width=200, height=224, bg=DARK_GREY, highlightthickness=0)
        self.canvas.pack(pady=20)
        self.tomato_img = tk.PhotoImage(file="tomato.png")
        self.canvas.create_image(100, 112, image=self.tomato_img)
        self.timer_text = self.canvas.create_text(103, 130, text="00:00", fill="white", font=(FONT_NAME, 24, "bold"))

        # Buttons
        self.button_frame = tk.Frame(self.window, bg=DARK_GREY)
        self.button_frame.pack(fill="x", pady=20)
        self.start_button = tk.Button(self.button_frame, text="Start", bg=GREEN, fg="white", highlightthickness=0, font=(FONT_NAME, 12, "bold"), command=self.start_timer)
        self.start_button.pack(side="left", padx=(50, 10), pady=10)
        self.reset_button = tk.Button(self.button_frame, text="Reset", bg=YELLOW, fg="white", highlightthickness=0, font=(FONT_NAME, 12, "bold"), command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10, pady=10)
        self.pause_button = tk.Button(self.button_frame, text="Pause", bg=TOMATO_RED, fg="white", highlightthickness=0, font=(FONT_NAME, 12, "bold"), command=self.pause_timer)
        self.pause_button.pack(side="left", padx=(10, 50), pady=10)

        # Checkmarks
        self.check_frame = tk.Frame(self.window, bg=DARK_GREY)
        self.check_frame.pack(fill="x")
        self.check_label = tk.Label(self.check_frame, fg=GREEN, bg=DARK_GREY, font=(FONT_NAME, 12))
        self.check_label.pack(pady=10)

        # Footer
        self.footer_frame = tk.Frame(self.window, bg=DARK_GREY)
        self.footer_frame.pack(fill="x")
        self.footer_label = tk.Label(self.footer_frame, text="Made with love by Ödenata", bg=DARK_GREY, fg="dark green", font=(FONT_NAME,10,"bold"))
        self.footer_label.pack(pady=10)

    def reset_timer(self):
        self.window.after_cancel(self.timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.timer_label.config(text="Pomodoro Timer")
        self.session_type_label.config(text="")
        self.check_label.config(text="")
        self.reps = 0
        self.running = False
        self.paused = False
        self.break_time = False
        self.count = 0

    def start_timer(self):
        if not self.running:
            self.reps += 1
            self.running = True
            if self.reps % 8 == 0:
                self.session_type_label.config(text="Long Break")
                self.count_down(LONG_BREAK_MIN * 60)
            elif self.reps % 2 == 0:
                self.session_type_label.config(text="Short Break")
                self.count_down(SHORT_BREAK_MIN * 60)
            else:
                self.session_type_label.config(text="Work Session")
                self.count_down(WORK_MIN * 60)

    def pause_timer(self):
        if self.running and not self.paused:
            self.paused = True
            self.window.after_cancel(self.timer)
            self.pause_button.config(text="Resume")
        elif self.paused:
            self.paused = False
            self.count_down(self.count)
            self.pause_button.config(text="Pause")

    def count_down(self, count):
        self.count = count
        minutes, seconds = divmod(count, 60)
        time_str = f"{minutes:02}:{seconds:02}"
        self.canvas.itemconfig(self.timer_text, text=time_str)
        if count > 0 and not self.break_time:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        elif count == 0 and not self.break_time:
            self.running = False
            if self.reps % 2 == 0:
                self.check_label.config(text=self.check_label.cget("text") + "✔")
            self.start_timer()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    timer = PomodoroTimer()
    timer.run()