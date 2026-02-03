import tkinter as tk
from tkinter import ttk, messagebox
import os

class SistemaComunitario:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Actividades Comunitarias")
        self.root.geometry("900x700")
        self.archivo = "usuarios.txt"

        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        self.telefono = tk.StringVar()
        self.vive_en = tk.StringVar()
        self.actividad = tk.StringVar()


        color_lila_claro = "#D1A8E1"
        color_morado_fuerte = "#A546B6"
        color_verde_fuerte = "#00674F"

        tk.Label(root, text="El Lienzo de Grafite", font=("Arial", 20, "bold"), 
                 bg=color_morado_fuerte, fg="white", bd=5, relief=tk.GROOVE).pack(side=tk.TOP, fill=tk.X, pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        campos = [("Nombre:", self.nombre), ("Apellido:", self.apellido), 
                  ("Teléfono:", self.telefono), ("Ciudad:", self.vive_en)]

        for i, (texto, var) in enumerate(campos):
            tk.Label(frame, text=f" Ingrese {texto} ", bg=color_lila_claro, fg="black", font=("Arial", 10, "bold"), width=20, anchor="w").grid(row=i, column=0, padx=5, pady=5)
            tk.Entry(frame, textvariable=var, font=("Arial", 10), width=30).grid(row=i, column=1, padx=5, pady=5)

        tk.Label(frame, text=" Actividades: ", bg=color_lila_claro, fg="black", font=("Arial", 10, "bold"), width=20, anchor="w").grid(row=4, column=0, padx=5, pady=5)
        opciones = ["Reciclaje", "Reforestación", "Adopción de animales", "Cuidado de vía pública", "Ayuda a personas mayores"]
        self.combo = ttk.Combobox(frame, textvariable=self.actividad, values=opciones, state="readonly", width=28)
        self.combo.grid(row=4, column=1, padx=5, pady=5)
        self.combo.current(0)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Registrar", command=self.registrar, bg=color_verde_fuerte, fg="white", font=("Arial", 10, "bold"), width=12).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar, bg=color_morado_fuerte, fg="white", font=("Arial", 10, "bold"), width=12).grid(row=0, column=1, padx=10)

        tf = tk.Frame(root, bd=2, relief=tk.RIDGE)
        tf.place(x=50, y=350, width=800, height=250)
        self.tabla = ttk.Treeview(tf, columns=("id", "n", "a", "act", "est", "t", "l"))
        encabezados = ["ID Usuario", "Nombre", "Apellido", "Actividad", "Estado", "Teléfono", "Ciudad"]
        for col, h in zip(self.tabla["columns"], encabezados):
            self.tabla.heading(col, text=h)
            self.tabla.column(col, width=110, anchor="center")
        self.tabla['show'] = 'headings'
        self.tabla.pack(fill=tk.BOTH, expand=1)

        self.cargar_datos()
        tk.Button(root, text="Salir", command=root.quit, bg=color_morado_fuerte, fg="white", font=("Arial", 12, "bold"), width=10).pack(side=tk.BOTTOM, pady=20)

    def registrar(self):
        
        nom = self.nombre.get().strip()
        ape = self.apellido.get().strip()
        tel = self.telefono.get().strip()
        ciu = self.vive_en.get().strip()

        if nom == "" or ape == "" or tel == "" or ciu == "":
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

   
        if any(char.isdigit() for char in nom):
            messagebox.showerror("Error en Nombre", "El nombre no puede contener números.")
            return
        
        if any(char.isdigit() for char in ape):
            messagebox.showerror("Error en Apellido", "El apellido no puede contener números.")
            return

        if any(char.isdigit() for char in ciu):
            messagebox.showerror("Error en Ciudad", "La ciudad no dee contener números.")
            return

     
        if not tel.isdigit():
            messagebox.showerror("Error en Teléfono", "El teléfono solo debe contener números.")
            return

        
        count = 1
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                count = len(f.readlines()) + 1
        
        nuevo_id = f"User{count:03d}"
        datos = [nuevo_id, nom, ape, self.actividad.get(), "Disponible", tel, ciu]
        linea = " | ".join(datos) + "\n"
        
        with open(self.archivo, "a") as f:
            f.write(linea)
            
        messagebox.showinfo("Éxito", f"Usuario {nuevo_id} registrado correctamente")
        self.cargar_datos()
        self.limpiar()

    def cargar_datos(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                for l in f:
                    valores = [p.strip() for p in l.split("|")]
                    if len(valores) == 7:
                        self.tabla.insert('', tk.END, values=valores)

    def limpiar(self):
        self.nombre.set(""); self.apellido.set(""); self.telefono.set(""); self.vive_en.set("")
        self.combo.current(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaComunitario(root)
    root.mainloop()