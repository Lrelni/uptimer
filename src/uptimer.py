#uptimer
import tkinter as tk
from tkinter import ttk
 
import datetime

root = tk.Tk()
root.title('Uptimer')
w=280
h=206
h2=350
root.minsize(280,h)
root.maxsize(280,h2)
root.resizable(width=False, height=True)
ws = root.winfo_screenwidth() - w
hs = root.winfo_screenheight()
root.geometry(f"{w}x{h2}+{ws}+0")
root.wm_attributes("-topmost", True)
root.wait_visibility(root)
root.attributes("-alpha", 0.5)


f = tk.Frame(root, bg="grey")
f.grid(sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

timestamp = datetime.datetime.now()
flash = datetime.datetime.now()
flash_limit = 0.05
will_flash = False

def validate_number(value):
    if value == "":
        return True
    try:
        a = float(value)
    except ValueError:
        return False
    else:
        return True

vcmd = (f.register(validate_number), "%P")
flash_ent = ttk.Entry(f, textvariable=flash_limit, validate="all", validatecommand=vcmd, text="10", width=10, justify="center")
flash_ent.delete(0,tk.END)
flash_ent.insert(0,"30")

def sanitize(value):
    if value == "":
        return 0
    else:
        return float(value)
    
job = None
def update():
    global job
    time_elapsed = (datetime.datetime.now()-timestamp)
    string = (datetime.datetime.min + time_elapsed).strftime("%H:%M:%S")
    lbl.config(text=string)
    job = lbl.after(1000, update)
    print(root.winfo_height())
    if (datetime.datetime.now()-flash) > datetime.timedelta(minutes=sanitize(flash_ent.get())) and will_flash:
        lbl.config(background="red")
        root.attributes("-alpha", 0.9)
    else:
        lbl.config(background="grey")
        root.attributes("-alpha", 0.5)
 
 
lbl = tk.Label(f, font=('TkFixedFont', 40, "bold"),
               background="grey",
            foreground='white')


update()

def button_press():
    global timestamp
    global flash
    timestamp = datetime.datetime.now()
    flash = datetime.datetime.now()
    if job is not None:
        root.after_cancel(job)
    update()
    
btn = ttk.Button(f, text="I took a break", command=button_press)


lbl2 = tk.Label(f, background="grey", foreground="white", text="What am I doing?")


txt = tk.Text(f, height=4)



def clear_text():
    txt.delete(1.0, tk.END)
    
btn2 = ttk.Button(f, text="Clear reminder", command=clear_text)


flash_lbl = tk.Label(f, background="grey", foreground="white", text="Color change alert is OFF")


def toggle_color_change():
    global will_flash
    if will_flash:
        flash_lbl.config(background="grey", text="Color change alert is OFF")
        ft_btn.config(text="Enable color change alert")
        will_flash = False
    else:
        flash_lbl.config(background="red", text="Color change alert is ON")
        ft_btn.config(text="Disable color change alert")
        will_flash = True
        
    if job is not None:
        root.after_cancel(job)
    update()

ft_btn = ttk.Button(f, text="Enable color change alert", command=toggle_color_change)




lbl.pack(anchor="n")
btn.pack()
lbl2.pack()
txt.pack(anchor="s")
btn2.pack()
flash_lbl.pack()
ft_btn.pack()
tk.Label(f, background="grey", foreground="white", text="\nAlert shows after").pack()
flash_ent.pack()
tk.Label(f, background="grey", foreground="white", text="minutes").pack()


tk.mainloop()
