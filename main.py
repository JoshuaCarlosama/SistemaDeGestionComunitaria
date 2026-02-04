import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import time

color_lila_claro = "#D1A8E1"
color_morado_fuerte = "#A546B6"
color_verde_fuerte = "#00674F"
color_fondo = "#F0F0F0"

ARCHIVO = "Datos/usuarios.txt"

class VentanaPrincipal:

    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Ventana Principal")
        self.app.geometry("1200x550")
        self.app.config(bg=color_fondo)

        self.ultima_modificacion = 0

        self.crear_layout()
        self.actualizar_tabla()

        self.app.mainloop()

    def crear_layout(self):
        contenedor = tk.Frame(self.app, bg=color_fondo)
        contenedor.pack(fill=tk.BOTH, expand=True)

        panel_izq = tk.Frame(contenedor, bg=color_lila_claro, width=260)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y)
        panel_izq.pack_propagate(False)

        img = Image.open("Recursos/PoliLogo.png")
        img = img.resize((200, 120), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(img)

        tk.Label(panel_izq, image=self.logo, bg=color_lila_claro).pack(pady=15)

        self.crear_boton(panel_izq, "Agregar", "agregar.py")
        self.crear_boton(panel_izq, "Buscar", "buscar.py")
        self.crear_boton(panel_izq, "Actualizar", "actualizar.py")
        self.crear_boton(panel_izq, "Eliminar", "eliminar.py")

        tk.Label(panel_izq, bg=color_lila_claro).pack(pady=10)

        self.crear_boton(panel_izq, "Completar", "completar.py")
        self.crear_boton(panel_izq, "Recompensas", "recompensas.py")

        panel_der = tk.Frame(contenedor, bg=color_fondo)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tabla = ttk.Treeview(
            panel_der,
            columns=(
                "ID",
                "Nombre",
                "Apellido",
                "Actividad",
                "Estado",
                "Telefono",
                "Ciudad",
                "Puntaje"
            ),
            show="headings"
        )
        columnas = [
            ("ID", 80),
            ("Nombre", 120),
            ("Apellido", 120),
            ("Actividad", 160),
            ("Estado", 110),
            ("Telefono", 120),
            ("Ciudad", 120),
            ("Puntaje", 90)
        ]
        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def crear_boton(self, parent, texto, archivo):
        tk.Button(
            parent,
            text=texto,
            width=18,
            bg=color_morado_fuerte,
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: os.system(f"python {archivo}")
        ).pack(pady=6)

    def cargar_datos(self):
        datos = []
        if os.path.exists(ARCHIVO):
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = [p.strip() for p in linea.split("|")]

                    if len(partes) == 7:
                        partes.append("0")

                    if len(partes) == 8:
                        datos.append(partes)
        return datos
    
    def actualizar_tabla(self):
        if os.path.exists(ARCHIVO):
            modificado = os.path.getmtime(ARCHIVO)

            if modificado != self.ultima_modificacion:
                self.ultima_modificacion = modificado

                self.tabla.delete(*self.tabla.get_children())
                for fila in self.cargar_datos():
                    self.tabla.insert("", tk.END, values=fila)

        self.app.after(1000, self.actualizar_tabla)

if __name__ == "__main__":
    VentanaPrincipal()