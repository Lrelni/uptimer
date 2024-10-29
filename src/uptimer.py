import tkinter as tk
from tkinter import ttk
import datetime

class UptimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Uptimer')

        # Window dimensions and positioning
        self.WIDTH, self.HEIGHT, self.MAX_HEIGHT = 280, 206, 350
        self.geometry(f"{self.WIDTH}x{self.MAX_HEIGHT}+{self.winfo_screenwidth() - self.WIDTH}+0")
        self.minsize(self.WIDTH, self.HEIGHT)
        self.maxsize(self.WIDTH, self.MAX_HEIGHT)
        self.resizable(width=False, height=True)
        self.wm_attributes("-topmost", True)
        self.wait_visibility(self)
        self.attributes("-alpha", 0.5)

        # Frame settings
        self.frame = tk.Frame(self, bg="grey")
        self.frame.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Global variables
        self.start_time = datetime.datetime.now()
        self.flash_time = datetime.datetime.now()
        self.flash_interval = 0.05
        self.color_alert_active = False

        # Widgets and layout
        self.create_widgets()
        
        # Update job reference
        self.update_job = None

        # Start the timer update loop
        self.update_timer()

    def create_widgets(self):
        # Timer display label
        self.time_label = tk.Label(self.frame, font=('TkFixedFont', 40, "bold"), background="grey", foreground='white')
        self.time_label.pack(anchor="n")

        # Break button
        self.break_button = ttk.Button(self.frame, text="I took a break", command=self.reset_timer)
        self.break_button.pack()

        # Reminder input section
        self.reminder_label = tk.Label(self.frame, background="grey", foreground="white", text="What am I doing?")
        self.reminder_label.pack()
        self.reminder_text = tk.Text(self.frame, height=4)
        self.reminder_text.pack(anchor="s")

        # Clear reminder button
        self.clear_button = ttk.Button(self.frame, text="Clear reminder", command=self.clear_reminder)
        self.clear_button.pack()

        # Flash alert controls
        self.flash_status_label = tk.Label(self.frame, background="grey", foreground="white", text="Color change alert is OFF")
        self.flash_status_label.pack()
        self.toggle_flash_button = ttk.Button(self.frame, text="Enable color change alert", command=self.toggle_flash_alert)
        self.toggle_flash_button.pack()

        # Flash interval entry and labels
        tk.Label(self.frame, background="grey", foreground="white", text="\nAlert shows after").pack()
        self.vcmd = (self.frame.register(self.validate_number), "%P")
        self.flash_entry = ttk.Entry(self.frame, validate="all", validatecommand=self.vcmd, width=10, justify="center")
        self.flash_entry.delete(0, tk.END)
        self.flash_entry.insert(0, "30")
        self.flash_entry.pack()
        tk.Label(self.frame, background="grey", foreground="white", text="minutes").pack()

        # Bind cleanup to window close event
        self.protocol("WM_DELETE_WINDOW", self.clean_up)

    def validate_number(self, value):
        """Validates if the input is a float or empty string."""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def sanitize(self, value):
        """Sanitizes input value, returns 0 if empty."""
        return float(value) if value else 0

    def update_timer(self):
        """Updates the timer display and controls background color change."""
        if not self.time_label.winfo_exists():
            return

        time_elapsed = datetime.datetime.now() - self.start_time
        time_string = (datetime.datetime.min + time_elapsed).strftime("%H:%M:%S")
        self.time_label.config(text=time_string)

        if (datetime.datetime.now() - self.flash_time) > datetime.timedelta(minutes=self.sanitize(self.flash_entry.get())) and self.color_alert_active:
            self.time_label.config(background="red")
            self.attributes("-alpha", 0.9)
        else:
            self.time_label.config(background="grey")
            self.attributes("-alpha", 0.5)

        self.update_job = self.after(1000, self.update_timer)

    def reset_timer(self):
        """Resets the timer and flash timestamps, restarts update loop."""
        self.start_time = datetime.datetime.now()
        self.flash_time = datetime.datetime.now()

        if self.update_job is not None:
            self.after_cancel(self.update_job)
        self.update_timer()

    def clear_reminder(self):
        """Clears the reminder text field."""
        self.reminder_text.delete(1.0, tk.END)

    def toggle_flash_alert(self):
        """Toggles the flash alert activation status."""
        self.color_alert_active = not self.color_alert_active

        self.flash_status_label.config(
            background="red" if self.color_alert_active else "grey",
            text="Color change alert is ON" if self.color_alert_active else "Color change alert is OFF"
        )
        self.toggle_flash_button.config(
            text="Disable color change alert" if self.color_alert_active else "Enable color change alert"
        )

        if self.update_job is not None:
            self.after_cancel(self.update_job)
        self.update_timer()

    def clean_up(self):
        """Cleanup function to disable validatecommand before window close."""
        if self.update_job is not None:
            self.after_cancel(self.update_job)  # Cancel the update loop if running
        self.destroy()  # Close the main window

if __name__ == "__main__":
    app = UptimerApp()
    app.mainloop()
