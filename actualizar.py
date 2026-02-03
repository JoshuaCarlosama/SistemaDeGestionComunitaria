import tkinter as tk
from tkinter import ttk, messagebox
import os

archivo = "usuarios.txt"

def actualizar():
    id_usuario = entry_id.get().strip()
    nom = nombre.get().strip()
    ape = apellido.get().strip()
    tel = telefono.get().strip()
    ciu = ciudad.get().strip()
    act = actividad.get()
    disp = disponibilidad.get()

    if id_usuario == "" or nom == "" or ape == "" or tel == "" or ciu == "":
        messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
        return

    if len(nom) > 100 or len(ape) > 100 or len(ciu) > 100:
        messagebox.showerror("Error", "Máximo 100 caracteres permitidos.")
        return

    if not nom.isalpha() or not ape.isalpha() or not ciu.isalpha():
        messagebox.showerror(
            "Error",
            "Nombre, apellido y ciudad no deben contener números ni símbolos."
        )
        return

    if not tel.isdigit() or len(tel) < 10:
        messagebox.showerror("Error", "El teléfono debe tener al menos 10 dígitos.")
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
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Actualizar Usuario")
ventana.geometry("420x500")

tk.Label(
    ventana,
    text="ACTUALIZAR USUARIO",
    font=("Arial", 14, "bold")
).pack(pady=10)

tk.Label(ventana, text="ID Usuario").pack()
entry_id = tk.Entry(ventana)
entry_id.pack()

nombre = tk.StringVar()
apellido = tk.StringVar()
telefono = tk.StringVar()
ciudad = tk.StringVar()
actividad = tk.StringVar()
disponibilidad = tk.StringVar()

tk.Label(ventana, text="Nombre").pack()
tk.Entry(ventana, textvariable=nombre).pack()

tk.Label(ventana, text="Apellido").pack()
tk.Entry(ventana, textvariable=apellido).pack()

tk.Label(ventana, text="Teléfono").pack()
tk.Entry(ventana, textvariable=telefono).pack()

tk.Label(ventana, text="Ciudad").pack()
tk.Entry(ventana, textvariable=ciudad).pack()

tk.Label(ventana, text="Actividad").pack()
ttk.Combobox(
    ventana,
    textvariable=actividad,
    values=[
        "Reciclaje",
        "Reforestación",
        "Adopción de animales",
        "Cuidado de vía pública",
        "Ayuda a personas mayores"
    ],
    state="readonly"
).pack()

tk.Label(ventana, text="Disponibilidad").pack()
ttk.Combobox(
    ventana,
    textvariable=disponibilidad,
    values=["Disponible", "Ocupado"],
    state="readonly"
).pack()

tk.Button(
    ventana,
    text="Actualizar",
    command=actualizar
).pack(pady=20)

ventana.mainloop()