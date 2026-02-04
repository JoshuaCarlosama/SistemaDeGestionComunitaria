import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

archivo = "Datos/usuarios.txt"

recompensa1 = "Recursos/boletin.png"
recompensa2 = "Recursos/peluche.png"
recompensa3 = "Recursos/llavero.png"

class VentanaRecompensas:
    def __init__(self, root):
        self.root = root
        self.root.title("Recompensas")
        self.root.geometry("600x580")

        self.usuario = None
        self.puntaje_actual = 0
        self.id_usuario = ""

        color_lila = "#D1A8E1"
        color_morado = "#A546B6"

        tk.Label(
            root,
            text="RECOMPENSAS",
            font=("Arial", 18, "bold"),
            bg=color_morado,
            fg="white"
        ).pack(fill=tk.X, pady=10)

        buscar_frame = tk.Frame(root)
        buscar_frame.pack(pady=10)

        tk.Label(buscar_frame, text="ID Usuario").grid(row=0, column=0, padx=5)
        self.entry_id = tk.Entry(buscar_frame, width=20)
        self.entry_id.grid(row=0, column=1, padx=5)

        tk.Button(
            buscar_frame,
            text="Buscar",
            command=self.buscar_usuario,
            bg=color_morado,
            fg="white",
            width=10
        ).grid(row=0, column=2, padx=5)

        datos_frame = tk.Frame(root, bg=color_lila, bd=2, relief=tk.GROOVE)
        datos_frame.pack(pady=10, fill=tk.X, padx=20)

        self.lbl_nombre = tk.Label(datos_frame, text="Nombre: -", bg=color_lila)
        self.lbl_nombre.pack(anchor="w", padx=10, pady=2)

        self.lbl_apellido = tk.Label(datos_frame, text="Apellido: -", bg=color_lila)
        self.lbl_apellido.pack(anchor="w", padx=10, pady=2)

        self.lbl_puntaje = tk.Label(
            datos_frame,
            text="Puntaje: -",
            bg=color_lila,
            font=("Arial", 10, "bold")
        )
        self.lbl_puntaje.pack(anchor="w", padx=10, pady=2)

        rewards_frame = tk.Frame(root)
        rewards_frame.pack(pady=15)

        tk.Label(
            rewards_frame,
            text="Canjear Recompensas",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        tk.Button(
            rewards_frame,
            text="Boletín Cafetería EPN (100 pts)",
            command=lambda: self.comprar(100, recompensa1),
            width=35
        ).pack(pady=3)

        tk.Button(
            rewards_frame,
            text="Peluche de Búho (200 pts)",
            command=lambda: self.comprar(200, recompensa2),
            width=35
        ).pack(pady=3)

        tk.Button(
            rewards_frame,
            text="Llavero EPN (150 pts)",
            command=lambda: self.comprar(150, recompensa3),
            width=35
        ).pack(pady=3)

        self.preview_frame = tk.Frame(root)
        self.preview_frame.pack(pady=15)

        self.lbl_preview = tk.Label(self.preview_frame)
        self.lbl_preview.pack()

        self.lbl_msg = tk.Label(
            self.preview_frame,
            text="",
            font=("Arial", 11, "bold"),
            fg="green"
        )
        self.lbl_msg.pack()

        tk.Button(
            root,
            text="Salir",
            command=root.destroy,
            bg=color_morado,
            fg="white",
            width=12
        ).pack(pady=10)

    def buscar_usuario(self):
        uid = self.entry_id.get().strip()

        if uid == "":
            messagebox.showwarning("Advertencia", "Ingrese un ID.")
            return

        if not os.path.exists(archivo):
            messagebox.showerror("Error", "Archivo no encontrado.")
            return

        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                datos = [d.strip() for d in linea.split("|")]
                if datos[0] == uid:
                    self.usuario = datos
                    self.id_usuario = uid
                    self.puntaje_actual = int(datos[7])

                    self.lbl_nombre.config(text=f"Nombre: {datos[1]}")
                    self.lbl_apellido.config(text=f"Apellido: {datos[2]}")
                    self.lbl_puntaje.config(text=f"Puntaje: {self.puntaje_actual}")

                    self.limpiar_preview()
                    return

        messagebox.showerror("Error", "Usuario no encontrado.")

    def comprar(self, costo, img_path):
        if not self.usuario:
            messagebox.showwarning("Advertencia", "Busque un usuario primero.")
            return

        if self.puntaje_actual < costo:
            messagebox.showerror("Puntaje insuficiente", "No tiene puntos suficientes.")
            return

        self.puntaje_actual -= costo
        self.lbl_puntaje.config(text=f"Puntaje: {self.puntaje_actual}")

        self.actualizar_puntaje_archivo()

        try:
            img = Image.open(img_path)
            img = img.resize((220, 160), Image.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img)
            self.lbl_preview.config(image=self.img_tk)
        except:
            self.lbl_preview.config(image="")

        self.lbl_msg.config(text="¡Objeto adquirido!")

    def actualizar_puntaje_archivo(self):
        nuevas_lineas = []

        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                datos = [d.strip() for d in linea.split("|")]
                if datos[0] == self.id_usuario:
                    datos[7] = str(self.puntaje_actual)
                    nuevas_lineas.append(" | ".join(datos) + "\n")
                else:
                    nuevas_lineas.append(linea)

        with open(archivo, "w", encoding="utf-8") as f:
            f.writelines(nuevas_lineas)

    def limpiar_preview(self):
        self.lbl_preview.config(image="")
        self.lbl_msg.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    VentanaRecompensas(root)
    root.mainloop()