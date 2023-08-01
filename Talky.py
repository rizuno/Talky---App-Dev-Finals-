import tkinter as tk
from tkinter import messagebox
import datetime as dt
import time
import pyttsx3

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

stop_alarm_flag = False
alarm_in_progress = False

def set_alarm():
    global stop_alarm_flag, alarm_in_progress
    alarm_hour = int(hour_entry.get())
    alarm_minute = int(minute_entry.get())
    
    if alarm_in_progress:
        # An alarm is already in progress, don't start a new one
        messagebox.showwarning("Warning", "An alarm is already in progress. Please stop the current alarm first.")
        return   
    alarm_in_progress = True

    # Current date and time
    current_time = dt.datetime.now()

    # Set alarm_time to the current day initially
    alarm_time = dt.datetime(current_time.year, current_time.month, current_time.day, alarm_hour, alarm_minute)

    # If the alarm time has already passed, add a day to set it for tomorrow
    if alarm_time <= current_time:
        alarm_time += dt.timedelta(days=1)

    stop_button.config(state=tk.NORMAL)  # Enable the "Stop" button when the alarm is set

    while not stop_alarm_flag:
        current_time = dt.datetime.now()
        if current_time >= alarm_time:
            break
        remaining_time = alarm_time - current_time
        countdown_label.config(text=format_time(int(remaining_time.total_seconds())))
        app.update()  # Update the app window to refresh the countdown label
        time.sleep(1)

    stop_alarm_flag = False  # Reset the stop_alarm_flag

    countdown_label.config(text="00:00:00")
    app.update()  # Update the app window to refresh the countdown label

    stop_button.config(state=tk.DISABLED)  # Disable the "Stop" button after the alarm is triggered

    if not stop_alarm_flag:
        alarm_message = text_entry.get()
        alarms_listbox.insert(tk.END, f"{alarm_time.strftime('%H:%M')} - {alarm_message}")
        speak_alarm(alarm_message)
        messagebox.showinfo("Alarm", "Alarm Done!")

def stop_alarm():
    global stop_alarm_flag, alarm_in_progress
    stop_alarm_flag = True
    alarm_in_progress = False
    alarms_listbox.delete(0, tk.END)  # Clear all alarms in the listbox

def speak_alarm(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

app = tk.Tk()
app.title("Talky - Custom Alarm Clock Finals for App Dev")
app.geometry("500x400")

# Custom Colors
app.config(bg="#1E1E1E")
app_label = tk.Label(app, text="Talky", font=("Fira Code", 20), bg="#1E1E1E", fg="white")
app_label.pack(pady=10)

# Hour and Minute Input
time_frame = tk.Frame(app, bg="#1E1E1E")
time_frame.pack(pady=5)

hour_label = tk.Label(time_frame, text="Hour:", bg="#1E1E1E", fg="white")
hour_label.pack(side=tk.LEFT, padx=10)

hour_entry = tk.Entry(time_frame, bg="white", width=5)
hour_entry.pack(side=tk.LEFT)

minute_label = tk.Label(time_frame, text="Minute:", bg="#1E1E1E", fg="white")
minute_label.pack(side=tk.LEFT, padx=10)

minute_entry = tk.Entry(time_frame, bg="white", width=5)
minute_entry.pack(side=tk.LEFT)

# Custom Text Entry
text_label = tk.Label(app, text="Enter Text:", bg="#1E1E1E", fg="white")
text_label.pack(pady=5)

text_entry = tk.Entry(app, bg="white", width=30)
text_entry.pack()

# Set and Stop Buttons
buttons_frame = tk.Frame(app, bg="#1E1E1E")
buttons_frame.pack(pady=10)

set_button = tk.Button(buttons_frame, text="Set Alarm", command=set_alarm, bg="#007BFF", fg="white")
set_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(buttons_frame, text="Stop", state=tk.DISABLED, command=stop_alarm, bg="#DC3545", fg="white")
stop_button.pack(side=tk.LEFT, padx=5)

# Countdown Label
countdown_label = tk.Label(app, text="00:00:00", font=("Fira Code", 24, "bold"), bg="#1E1E1E", fg="white")
countdown_label.pack(pady=10)

# Alarm List
alarms_label = tk.Label(app, text="Alarm History", bg="#1E1E1E", fg="white")
alarms_label.pack(pady=5)

alarms_listbox = tk.Listbox(app, width=30, height=8, bg="white")
alarms_listbox.pack(pady=5)

app.mainloop()