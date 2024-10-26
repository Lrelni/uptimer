#uptimer
import tkinter as tk
from tkinter import ttk
 
import datetime

root = tk.Tk()
root.title('Uptimer')
w=280
h=200
root.resizable(width=False, height=False)
ws = root.winfo_screenwidth() - w
hs = root.winfo_screenheight()
root.geometry(f"{w}x{h}+{ws}+0")
root.wm_attributes("-topmost", True)
root.wait_visibility(root)
root.attributes("-alpha", 0.5)


f = tk.Frame(root, bg="grey")
f.grid(sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

timestamp = datetime.datetime.now()
print(timestamp)

 
def time1():
    string = (datetime.datetime.min + (datetime.datetime.now()-timestamp)).strftime("%H:%M:%S")
    lbl.config(text=string)
    lbl.after(1000, time1)
 
 
lbl = tk.Label(f, font=('TkFixedFont', 40, "bold"),
               background="grey",
            foreground='white')

lbl.pack(anchor="n")
time1()

def button_press():
    global timestamp
    timestamp = datetime.datetime.now()
    time1()
    
btn = ttk.Button(f, text="Break", command=button_press)
btn.pack()

lbl2 = tk.Label(f, background="grey", foreground="white", text="What am I doing?")
lbl2.pack()

txt = tk.Text(f, height=10)

txt.pack(anchor="s")

tk.mainloop()
