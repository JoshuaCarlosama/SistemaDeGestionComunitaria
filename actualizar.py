import tkinter as tk
from tkinter import ttk, messagebox
import os
import re

archivo = "Datos/usuarios.txt"

color_lila_claro = "#D1A8E1"
color_morado_fuerte = "#A546B6"

def validar_id(nuevo):
    if len(nuevo) > 10:
        return False
    return re.match("^[A-Za-z0-9]*$", nuevo) is not None

def validar_texto_30(nuevo):
    if len(nuevo) > 30:
        return False
    return re.match("^[A-Za-zÁÉÍÓÚáéíóúÑñ ]*$", nuevo) is not None

def validar_telefono(nuevo):
    if len(nuevo) > 10:
        return False
    return nuevo.isdigit() or nuevo == ""

def limpiar():
    entry_id.delete(0, tk.END)
    nombre.set("")
    apellido.set("")
    telefono.set("")
    ciudad.set("")
    actividad.current(0)
    disponibilidad.current(0)

def actualizar():
    id_usuario = entry_id.get().strip()
    nom = nombre.get().strip()
    ape = apellido.get().strip()
    tel = telefono.get().strip()
    ciu = ciudad.get().strip()
    act = actividad.get()
    disp = disponibilidad.get()

    if not id_usuario or not nom or not ape or not tel or not ciu:
        messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
        return

    if not (7 <= len(tel) <= 15):
        messagebox.showerror("Error Teléfono", "Debe tener entre 7 y 15 dígitos.")
        return

    if not os.path.exists(archivo):
        messagebox.showerror("Error", "El archivo usuarios.txt no existe.")
        return

    nuevas_lineas = []
    encontrado = False

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            datos = [p.strip() for p in linea.split("|")]

            if datos[0] == id_usuario:
                datos[1] = nom
                datos[2] = ape
                datos[3] = act
                datos[4] = disp
                datos[5] = tel
                datos[6] = ciu
                nuevas_lineas.append(" | ".join(datos) + "\n")
                encontrado = True
            else:
                nuevas_lineas.append(linea)

    if not encontrado:
        messagebox.showerror("Error", "ID no encontrado.")
        return

    with open(archivo, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)

    messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
    limpiar()

ventana = tk.Tk()
ventana.title("Actualizar Usuario")
ventana.geometry("450x560")

vcmd_id = ventana.register(validar_id)
vcmd_texto = ventana.register(validar_texto_30)
vcmd_tel = ventana.register(validar_telefono)

tk.Label(
    ventana,
    text="ACTUALIZAR USUARIO",
    font=("Arial", 16, "bold"),
    bg=color_morado_fuerte,
    fg="white",
    pady=10
).pack(fill=tk.X)

frame = tk.Frame(ventana)
frame.pack(pady=15)

def campo(texto, fila):
    tk.Label(
        frame, text=texto,
        bg=color_lila_claro,
        font=("Arial", 10, "bold"),
        width=20, anchor="w"
    ).grid(row=fila, column=0, padx=5, pady=5)

nombre = tk.StringVar()
apellido = tk.StringVar()
telefono = tk.StringVar()
ciudad = tk.StringVar()

campo("ID Usuario:", 0)
entry_id = tk.Entry(frame, width=30,validate="key",validatecommand=(vcmd_id, "%P"))
entry_id.grid(row=0, column=1)

campo("Nombre:", 1)
tk.Entry(frame, textvariable=nombre, width=30,validate="key",validatecommand=(vcmd_texto, "%P")
).grid(row=1, column=1)

campo("Apellido:", 2)
tk.Entry(frame, textvariable=apellido, width=30,validate="key",validatecommand=(vcmd_texto, "%P")
).grid(row=2, column=1)

campo("Teléfono:", 3)
tk.Entry(frame, textvariable=telefono, width=30,validate="key",validatecommand=(vcmd_tel, "%P")
).grid(row=3, column=1)

campo("Ciudad:", 4)
tk.Entry(frame, textvariable=ciudad, width=30,validate="key",validatecommand=(vcmd_texto, "%P")
).grid(row=4, column=1)

campo("Actividad:", 5)
actividad = ttk.Combobox(frame,values=[
        "Reciclaje",
        "Reforestación",
        "Adopción de animales",
        "Cuidado de vía pública",
        "Ayuda a personas mayores"
    ],state="readonly",width=28
)
actividad.grid(row=5, column=1)
actividad.current(0)

campo("Disponibilidad:", 6)
disponibilidad = ttk.Combobox(frame,values=["Disponible", "Ocupado"],state="readonly",width=28)
disponibilidad.grid(row=6, column=1)
disponibilidad.current(0)

btn_frame = tk.Frame(ventana)
btn_frame.pack(pady=20)

tk.Button(btn_frame,text="Actualizar",command=actualizar,bg=color_morado_fuerte,fg="white",font=("Arial", 11, "bold"),width=14
).grid(row=0, column=0, padx=10)

tk.Button(btn_frame,text="Limpiar",command=limpiar,bg=color_lila_claro,font=("Arial", 11, "bold"),width=14
).grid(row=0, column=1, padx=10)

ventana.mainloop()