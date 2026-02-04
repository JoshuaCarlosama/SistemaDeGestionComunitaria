import tkinter as tk
from tkinter import ttk, messagebox
import os
import re

def texto_valido(texto, max_len):
    if texto.strip() == "":
        return False
    if len(texto) > max_len:
        return False
    return re.match("^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", texto) is not None


def validar_texto_30(nuevo):
    if len(nuevo) > 21:
        return False
    return re.match("^[A-Za-zÁÉÍÓÚáéíóúÑñ ]*$", nuevo) is not None


def validar_telefono(nuevo):
    if len(nuevo) > 10:
        return False
    return nuevo.isdigit() or nuevo == ""

def generar_nuevo_id(archivo):
    max_num = 0

    if not os.path.exists(archivo):
        return "User001"

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.split("|")
            if partes:
                uid = partes[0].strip()
                if uid.startswith("User"):
                    try:
                        num = int(uid.replace("User", ""))
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        pass

    return f"User{max_num + 1:03d}"

class SistemaComunitario:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Actividades Comunitarias")
        self.root.geometry("900x700")
        self.archivo = "Datos/usuarios.txt"

        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        self.telefono = tk.StringVar()
        self.vive_en = tk.StringVar()
        self.actividad = tk.StringVar()

        color_lila_claro = "#D1A8E1"
        color_morado_fuerte = "#A546B6"

        tk.Label(
            root,
            text="Sistema de Gestión de Actividades Comunitarias",
            font=("Arial", 20, "bold"),
            bg=color_morado_fuerte,
            fg="white",
            bd=5,
            relief=tk.GROOVE
        ).pack(side=tk.TOP, fill=tk.X, pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        vcmd_texto = root.register(validar_texto_30)
        vcmd_tel = root.register(validar_telefono)

        tk.Label(frame, text=" Ingrese Nombre: ", bg=color_lila_claro,
                 font=("Arial", 10, "bold"), width=20, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.nombre, width=30, font=("Arial", 10),
                 validate="key", validatecommand=(vcmd_texto, "%P")
                 ).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text=" Ingrese Apellido: ", bg=color_lila_claro,
                 font=("Arial", 10, "bold"), width=20, anchor="w").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.apellido, width=30, font=("Arial", 10),
                 validate="key", validatecommand=(vcmd_texto, "%P")
                 ).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text=" Ingrese Teléfono: ", bg=color_lila_claro,
                 font=("Arial", 10, "bold"), width=20, anchor="w").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.telefono, width=30, font=("Arial", 10),
                 validate="key", validatecommand=(vcmd_tel, "%P")
                 ).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text=" Ingrese Ciudad: ", bg=color_lila_claro,
                 font=("Arial", 10, "bold"), width=20, anchor="w").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.vive_en, width=30, font=("Arial", 10),
                 validate="key", validatecommand=(vcmd_texto, "%P")
                 ).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text=" Actividades: ", bg=color_lila_claro,
                 font=("Arial", 10, "bold"), width=20, anchor="w").grid(row=4, column=0, padx=5, pady=5)

        opciones = [
            "Reciclaje",
            "Reforestación",
            "Adopción de animales",
            "Cuidado de vía pública",
            "Ayuda a personas mayores"
        ]
        self.combo = ttk.Combobox(frame, textvariable=self.actividad,
                                  values=opciones, state="readonly", width=28)
        self.combo.grid(row=4, column=1, padx=5, pady=5)
        self.combo.current(0)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Registrar", command=self.registrar,
                  bg=color_morado_fuerte, fg="white",
                  font=("Arial", 10, "bold"), width=12).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar,
                  bg=color_morado_fuerte, fg="white",
                  font=("Arial", 10, "bold"), width=12).grid(row=0, column=1, padx=10)

        tf = tk.Frame(root, bd=2, relief=tk.RIDGE)
        tf.place(x=50, y=350, width=800, height=250)

        self.tabla = ttk.Treeview(tf, columns=("id", "n", "a", "act", "est", "t", "l"), show="headings")
        encabezados = ["ID Usuario", "Nombre", "Apellido", "Actividad", "Estado", "Teléfono", "Ciudad"]

        for col, h in zip(self.tabla["columns"], encabezados):
            self.tabla.heading(col, text=h)
            self.tabla.column(col, width=110, anchor="center")

        self.tabla.pack(fill=tk.BOTH, expand=1)
        self.cargar_datos()

        tk.Button(root, text="Salir", command=root.quit,
                  bg=color_morado_fuerte, fg="white",
                  font=("Arial", 12, "bold"), width=10).pack(side=tk.BOTTOM, pady=20)

    def registrar(self):
        nom = self.nombre.get().strip()
        ape = self.apellido.get().strip()
        tel = self.telefono.get().strip()
        ciu = self.vive_en.get().strip()

        if not nom or not ape or not tel or not ciu:
            messagebox.showwarning("Campos vacíos", "Complete todos los campos")
            return

        if not texto_valido(nom, 30) or not texto_valido(ape, 30) or not texto_valido(ciu, 30):
            messagebox.showerror("Error", "Texto inválido (máx 30 caracteres)")
            return

        if not tel.isdigit() or not (7 <= len(tel) <= 15):
            messagebox.showerror("Error Teléfono", "Solo números (7 a 15 dígitos)")
            return

        os.makedirs("Datos", exist_ok=True)

        with open(self.archivo, "r", encoding="utf-8") if os.path.exists(self.archivo) else open(self.archivo, "w", encoding="utf-8"):
            pass

        nuevo_id = generar_nuevo_id(self.archivo)

        with open(self.archivo, "a", encoding="utf-8") as f:
            f.write(f"{nuevo_id} | {nom} | {ape} | {self.actividad.get()} | Disponible | {tel} | {ciu}\n")

        messagebox.showinfo("Registro exitoso", f"Usuario {nuevo_id} registrado")
        self.cargar_datos()
        self.limpiar()

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                for l in f:
                    self.tabla.insert("", tk.END, values=[x.strip() for x in l.split("|")])

    def limpiar(self):
        self.nombre.set("")
        self.apellido.set("")
        self.telefono.set("")
        self.vive_en.set("")
        self.combo.current(0)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaComunitario(root)
    root.mainloop()