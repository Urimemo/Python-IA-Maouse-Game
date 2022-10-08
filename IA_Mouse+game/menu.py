from tkinter import Tk
import tkinter as tk
from _tkinter import *
import MouseVirtual as MV

#Hacer el frame
frame = Tk()
frame.geometry("640x480")
tk.Wm.wm_title(frame, "Titulo guapo")
frame.configure(background="black")

def game():
    MV.Program.game(self="")

def mouse():
    MV.Program.mouse(self="")

tk.Button(
    frame,
    text="Mode de Joc",
    font=("Verdana", 15),
    bg="#000F59",
    foreground="white",
    command=game
).pack(
    fill=tk.BOTH,
    expand=True
)

tk.Button(
    frame,
    text="Mode ratolí",
    font=("Verdana", 15),
    bg="#001786",
    foreground="white",
    command=mouse
).pack(
    fill=tk.BOTH,
    expand=True
)

frame.mainloop()



