import tkinter as tk
from tkinter import ttk, messagebox
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

def validar_texto(nuevo):
    if len(nuevo) > 30:
        return False
    return re.match("^[A-Za-zÁÉÍÓÚáéíóúÑñ ]*$", nuevo) is not None

ventana = tk.Tk()
ventana.title("Buscar Usuario")
ventana.geometry("750x500")
ventana.config(bg=color_fondo)

vcmd_id = ventana.register(validar_id)
vcmd_texto = ventana.register(validar_texto)

tk.Label(
    ventana,
    text="BUSCAR USUARIO",
    font=("Arial", 16, "bold"),
    bg=color_morado_fuerte,
    fg="white",
    pady=10
).pack(fill=tk.X)

form = tk.Frame(ventana, bg=color_fondo)
form.pack(pady=15)

tk.Label(form, text="Buscar por ID:", bg=color_lila_claro, width=20, anchor="w").grid(row=0, column=0, padx=5, pady=5)
entry_id = tk.Entry(form, width=30, validate="key", validatecommand=(vcmd_id, "%P"))
entry_id.grid(row=0, column=1)

tk.Label(form, text="Buscar por Nombre:", bg=color_lila_claro, width=20, anchor="w").grid(row=1, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(form, width=30, validate="key", validatecommand=(vcmd_texto, "%P"))
entry_nombre.grid(row=1, column=1)

tk.Label(form, text="Buscar por Apellido:", bg=color_lila_claro, width=20, anchor="w").grid(row=2, column=0, padx=5, pady=5)
entry_apellido = tk.Entry(form, width=30, validate="key", validatecommand=(vcmd_texto, "%P"))
entry_apellido.grid(row=2, column=1)

frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=15, fill=tk.BOTH, expand=True)

tabla = ttk.Treeview(
    frame_tabla,
    columns=("ID", "Nombre", "Apellido", "Actividad", "Estado", "Telefono", "Ciudad"),
    show="headings"
)

for col in tabla["columns"]:
    tabla.heading(col, text=col)
    tabla.column(col, anchor="center", width=100)

tabla.pack(fill=tk.BOTH, expand=True)

def buscar():
    tabla.delete(*tabla.get_children())

    if not os.path.exists(archivo):
        messagebox.showerror("Error", "No existe el archivo usuarios.txt")
        return

    id_b = entry_id.get().strip()
    nom_b = entry_nombre.get().strip().lower()
    ape_b = entry_apellido.get().strip().lower()

    encontrado = False

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            datos = [p.strip() for p in linea.split("|")]
            if len(datos) != 7:
                continue

            if (
                (id_b and datos[0] == id_b) or
                (nom_b and datos[1].lower() == nom_b) or
                (ape_b and datos[2].lower() == ape_b)
            ):
                tabla.insert("", tk.END, values=datos)
                encontrado = True

    if not encontrado:
        messagebox.showinfo("Resultado", "No se encontraron coincidencias.")

def limpiar():
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    tabla.delete(*tabla.get_children())

btns = tk.Frame(ventana, bg=color_fondo)
btns.pack(pady=10)

tk.Button(btns, text="Buscar", command=buscar, bg=color_morado_fuerte, fg="white", width=12).grid(row=0, column=0, padx=10)
tk.Button(btns, text="Limpiar", command=limpiar, bg=color_lila_claro, width=12).grid(row=0, column=1, padx=10)

ventana.mainloop()
