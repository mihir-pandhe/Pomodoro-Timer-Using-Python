import tkinter as tk
from tkinter import ttk
from plyer import notification


class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.geometry("400x500")
        self.master.configure(bg="#D95550")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.style.configure(
            "TLabel", background="#D95550", foreground="white", font=("Arial", 14)
        )

        self.time_var = tk.StringVar()
        self.time_var.set("25:00")

        self.label = ttk.Label(master, textvariable=self.time_var, font=("Arial", 48))
        self.label.pack(pady=20)

        self.start_button = ttk.Button(master, text="START", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(master, text="STOP", command=self.stop_timer)
        self.stop_button.pack(pady=5)

        self.reset_button = ttk.Button(master, text="RESET", command=self.reset_timer)
        self.reset_button.pack(pady=5)

        self.session_label = ttk.Label(master, text="Session: 1")
        self.session_label.pack(pady=5)

        self.task_label = ttk.Label(master, text="Tasks")
        self.task_label.pack(pady=5)

        self.task_frame = ttk.Frame(master)
        self.task_frame.pack(pady=5)

        self.task_listbox = tk.Listbox(self.task_frame, height=5, width=30)
        self.task_listbox.pack(side=tk.LEFT, padx=(0, 10))

        self.task_scrollbar = ttk.Scrollbar(self.task_frame)
        self.task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.task_scrollbar.set)
        self.task_scrollbar.config(command=self.task_listbox.yview)

        self.task_entry = ttk.Entry(master)
        self.task_entry.pack(pady=5)

        self.add_task_button = ttk.Button(
            master, text="Add Task", command=self.add_task
        )
        self.add_task_button.pack(pady=5)

        self.mark_done_button = ttk.Button(
            master, text="Mark as Done", command=self.mark_task_done
        )
        self.mark_done_button.pack(pady=5)

        self.edit_task_button = ttk.Button(
            master, text="Edit Task", command=self.edit_task
        )
        self.edit_task_button.pack(pady=5)

        self.work_duration = 25 * 60
        self.sessions = 0
        self.timer_running = False

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

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

    def mark_task_done(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task = self.task_listbox.get(selected_task_index)
            self.task_listbox.delete(selected_task_index)
            self.task_listbox.insert(selected_task_index, f"{selected_task} (Done)")

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.task_listbox.get(selected_task_index)
            new_task = self.simple_input_dialog("Edit Task", "Edit the task:", task)
            if new_task:
                self.task_listbox.delete(selected_task_index)
                self.task_listbox.insert(selected_task_index, new_task)

    def simple_input_dialog(self, title, prompt, initial_value=""):
        user_input = ""

        dialog = tk.Toplevel(self.master)
        dialog.title(title)

        label = ttk.Label(dialog, text=prompt)
        label.pack(pady=10)

        entry = ttk.Entry(dialog)
        entry.pack(pady=5)
        entry.insert(0, initial_value)

        def on_ok():
            nonlocal user_input
            user_input = entry.get()
            dialog.destroy()

        ok_button = ttk.Button(dialog, text="OK", command=on_ok)
        ok_button.pack(pady=5)

        dialog.transient(self.master)
        dialog.grab_set()
        self.master.wait_window(dialog)

        return user_input

    def update_timer(self):
        if self.timer_running:
            minutes, seconds = divmod(self.work_duration, 60)
            self.time_var.set(f"{minutes:02d}:{seconds:02d}")
            if self.work_duration > 0:
                self.work_duration -= 1
                self.master.after(1000, self.update_timer)
            else:
                self.sessions += 1
                self.session_label.config(text=f"Session: {self.sessions + 1}")
                self.show_notification(
                    "Pomodoro Timer", "Time's up! Take a break or start a new session."
                )
                self.reset_timer()

    def show_notification(self, title, message):
        notification.notify(title=title, message=message, timeout=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
