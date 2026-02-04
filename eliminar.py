import tkinter as tk
from tkinter import messagebox
import os
import re

directorio = os.path.dirname(os.path.abspath(__file__))

archivo = os.path.join(directorio, "Datos", "usuarios.txt")

color_lila_claro = "#D1A8E1"
color_morado_fuerte = "#A546B6"
color_fondo = "#F0F0F0"

def validar_id(nuevo):
    if len(nuevo) > 10:
        return False
    return re.match("^[A-Za-z0-9]*$", nuevo) is not None

def eliminar():
    id_usuario = entry_id.get().strip()

    if not id_usuario:
        messagebox.showwarning("Campo vacío", "Ingrese un ID.")
        return

    if not os.path.exists(archivo):
        messagebox.showerror("Error", "Archivo usuarios.txt no existe.")
        return

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Seguro que desea eliminar el usuario {id_usuario}?"
    )

    if not confirmar:
        return

    nuevas_lineas = []
    eliminado = False

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            datos = [p.strip() for p in linea.split("|")]
            if datos[0] == id_usuario:
                eliminado = True
            else:
                nuevas_lineas.append(linea)

    if not eliminado:
        messagebox.showerror("Error", "ID no encontrado.")
        return

    with open(archivo, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)

    messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
    entry_id.delete(0, tk.END)

ventana = tk.Tk()
ventana.title("Eliminar Usuario")
ventana.geometry("400x250")
ventana.config(bg=color_fondo)

vcmd = ventana.register(validar_id)

tk.Label(ventana,text="ELIMINAR USUARIO",font=("Arial", 16, "bold"),bg=color_morado_fuerte,fg="white",pady=10
).pack(fill=tk.X)

frame = tk.Frame(ventana, bg=color_fondo)
frame.pack(pady=30)

tk.Label(frame,text="ID Usuario:",bg=color_lila_claro,width=20,anchor="w"
).grid(row=0, column=0, padx=5, pady=5)

entry_id = tk.Entry(frame,width=25,validate="key",validatecommand=(vcmd, "%P"))
entry_id.grid(row=0, column=1)

tk.Button(ventana,text="Eliminar",command=eliminar,bg=color_morado_fuerte,fg="white",font=("Arial", 11, "bold"),width=14
).pack(pady=15)

ventana.mainloop()
