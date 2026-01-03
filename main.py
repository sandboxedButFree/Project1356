import tkinter as tk
from datetime import date, timedelta
from pathlib import Path
import json, pyglet, os

TOTAL_DAYS = 1356
STATE_FILE = Path("start_date.txt")
OBJECTIVES_FILE = Path("objectives.json")
UPDATE_INTERVAL_MS = 1000

#Custom Font
font_path = os.path.join(os.path.dirname(__file__), "SmoothMarker-45d6.ttf") 
pyglet.font.add_file(font_path)


if not STATE_FILE.exists():
    start_date = date.today()
    STATE_FILE.write_text(start_date.isoformat())
else:
    start_date = date.fromisoformat(STATE_FILE.read_text().strip())

if not OBJECTIVES_FILE.exists():
    objectives = {f"Objective {i+1}": False for i in range(6)}
    with open(OBJECTIVES_FILE, "w") as f:
        json.dump(objectives, f, indent=4)
else:
    with open(OBJECTIVES_FILE, "r") as f:
        objectives = json.load(f)

root = tk.Tk()
root.title("Project 1356")
root.configure(bg="#ffffff")
root.geometry("950x750")

board_frame = tk.Frame(root, bg="#ffffff", bd=5, relief="ridge")
board_frame.pack(expand=True, fill="both", padx=20, pady=20)

count_label = tk.Label(
    board_frame,
    text="",
    font=("Smooth Marker", 160, "bold"),
    bg="#ffffff",
    fg="#111111" 
)
count_label.pack(pady=(30,20))

info_label = tk.Label(
    board_frame,
    font=("Smooth Marker", 18),
    bg="#ffffff",
    fg="#111111",
    justify="center"
)
info_label.pack(pady=(0,20))

obj_frame = tk.Frame(board_frame, bg="#ffffff")
obj_frame.pack(pady=(0,20))

obj_labels = []
for name, done in objectives.items():
    lbl = tk.Label(
        obj_frame,
        text="",
        font=("Smooth Marker", 22),
        bg="#ffffff",
        fg="#111111",
        anchor="w",
        width=40
    )
    lbl.pack(pady=5)
    obj_labels.append(lbl)

def update_dashboard():
    global obj_labels

    today = date.today()
    elapsed_days = max(0, (today - start_date).days)
    remaining_days = max(0, TOTAL_DAYS - elapsed_days)
    end_date = start_date + timedelta(days=TOTAL_DAYS)

    count_label.config(text=str(remaining_days))

    with open(OBJECTIVES_FILE, "r") as f:
        objectives = json.load(f)

    for lbl, (name, done) in zip(obj_labels, objectives.items()):
        status = "✅" if done else "❌"
        lbl.config(text=f"{status} {name}")

    root.after(UPDATE_INTERVAL_MS, update_dashboard)

update_dashboard()
root.mainloop()
