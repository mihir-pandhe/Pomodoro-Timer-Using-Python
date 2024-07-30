import tkinter as tk
import threading
import time


class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")

        self.time_var = tk.StringVar()
        self.time_var.set("25:00")

        self.label = tk.Label(master, textvariable=self.time_var, font=("Arial", 48))
        self.label.pack(pady=20)

        self.start_button = tk.Button(master, text="START", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(master, text="RESET", command=self.reset_timer)
        self.reset_button.pack(pady=5)

        self.session_label = tk.Label(master, text="Session: 1", font=("Arial", 14))
        self.session_label.pack(pady=5)

        self.task_label = tk.Label(master, text="Tasks", font=("Arial", 14))
        self.task_label.pack(pady=5)

        self.task_listbox = tk.Listbox(master)
        self.task_listbox.pack(pady=5)

        self.task_entry = tk.Entry(master)
        self.task_entry.pack(pady=5)

        self.add_task_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.long_break_duration = 15 * 60
        self.sessions = 0
        self.timer_running = False
        self.is_break = False

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def reset_timer(self):
        self.timer_running = False
        self.work_duration = 25 * 60
        self.time_var.set("25:00")
        self.sessions = 0
        self.session_label.config(text="Session: 1")

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def update_timer(self):
        if self.timer_running:
            if not self.is_break:
                minutes, seconds = divmod(self.work_duration, 60)
                self.time_var.set(f"{minutes:02d}:{seconds:02d}")
                if self.work_duration > 0:
                    self.work_duration -= 1
                    self.master.after(1000, self.update_timer)
                else:
                    self.is_break = True
                    self.sessions += 1
                    if self.sessions % 4 == 0:
                        self.break_duration = self.long_break_duration
                    self.session_label.config(text=f"Session: {self.sessions + 1}")
                    self.update_timer()
            else:
                minutes, seconds = divmod(self.break_duration, 60)
                self.time_var.set(f"{minutes:02d}:{seconds:02d}")
                if self.break_duration > 0:
                    self.break_duration -= 1
                    self.master.after(1000, self.update_timer)
                else:
                    self.is_break = False
                    self.break_duration = 5 * 60
                    self.work_duration = 25 * 60
                    self.update_timer()


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
