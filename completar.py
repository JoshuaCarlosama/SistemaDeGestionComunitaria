import tkinter as tk
from tkinter import messagebox
import os

directorio = os.path.dirname(os.path.abspath(__file__))

archivo = os.path.join(directorio, "Datos", "usuarios.txt")

class Recompensas:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.withdraw()
        self.usuario_actual = None
        self.lineas = []

        self.login_admin()
        self.ventana.mainloop()

    def login_admin(self):
        login = tk.Toplevel()
        login.title("Acceso Administrador")
        login.geometry("300x200")
        login.resizable(False, False)
        login.grab_set()

        tk.Label(
            login,
            text="ADMINISTRADOR",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Label(login, text="Usuario").pack()
        entry_user = tk.Entry(login)
        entry_user.pack()

        tk.Label(login, text="Contraseña").pack()
        entry_pass = tk.Entry(login, show="*")
        entry_pass.pack()

        def verificar():
            if entry_user.get() == "Admin" and entry_pass.get() == "123":
                login.destroy()
                self.crear_interfaz()
            else:
                messagebox.showerror(
                    "Acceso denegado",
                    "Credenciales incorrectas"
                )

        tk.Button(login, text="Ingresar", command=verificar).pack(pady=10)
        tk.Button(login, text="Salir", command=self.ventana.destroy).pack()

    def crear_interfaz(self):
        self.ventana.deiconify()
        self.ventana.title("Completar Actividad")
        self.ventana.geometry("420x350")
        self.ventana.resizable(False, False)

        tk.Label(self.ventana,text="COMPLETAR ACTIVIDAD",font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Label(self.ventana, text="ID Usuario").pack()
        self.entry_id = tk.Entry(self.ventana)
        self.entry_id.pack(pady=5)

        tk.Button(self.ventana,text="Buscar",command=self.buscar_usuario
        ).pack(pady=5)

        self.lbl_nombre = tk.Label(self.ventana, text="Nombre: -")
        self.lbl_nombre.pack(pady=2)

        self.lbl_apellido = tk.Label(self.ventana, text="Apellido: -")
        self.lbl_apellido.pack(pady=2)

        self.lbl_actividad = tk.Label(self.ventana, text="Actividad: -")
        self.lbl_actividad.pack(pady=2)

        frame_btn = tk.Frame(self.ventana)
        frame_btn.pack(pady=20)

        tk.Button(frame_btn,text="Completado",width=12,command=self.marcar_completado
        ).grid(row=0, column=0, padx=5)

        tk.Button(frame_btn,text="Incompleto",width=12,command=self.marcar_incompleto
        ).grid(row=0, column=1, padx=5)

        tk.Button(frame_btn,text="Salir",width=12,command=self.ventana.destroy
        ).grid(row=0, column=2, padx=5)

    def buscar_usuario(self):
        uid = self.entry_id.get().strip()
        if uid == "":
            messagebox.showwarning("Advertencia", "Ingrese un ID.")
            return

        if not os.path.exists(archivo):
            messagebox.showerror("Error", "Archivo usuarios.txt no encontrado.")
            return

        self.usuario_actual = None
        self.lineas.clear()

        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                datos = [p.strip() for p in linea.split("|")]
                self.lineas.append(datos)

                if datos[0] == uid:
                    self.usuario_actual = datos

        if not self.usuario_actual:
            messagebox.showerror("Error", "ID no encontrado.")
            self.limpiar_labels()
            return

        self.lbl_nombre.config(text=f"Nombre: {self.usuario_actual[1]}")
        self.lbl_apellido.config(text=f"Apellido: {self.usuario_actual[2]}")
        self.lbl_actividad.config(text=f"Actividad: {self.usuario_actual[3]}")

    def marcar_completado(self):
        if not self.usuario_actual:
            messagebox.showwarning("Advertencia", "Busque un usuario primero.")
            return

        if self.usuario_actual[4] == "Completado":
            messagebox.showinfo(
                "Información",
                "La actividad ya fue completada.\nNo se suman más puntos."
            )
            return

        self.usuario_actual[4] = "Completado"

        if len(self.usuario_actual) < 8:
            self.usuario_actual.append("100")
        else:
            self.usuario_actual[7] = str(int(self.usuario_actual[7]) + 100)

        self.guardar()

        messagebox.showinfo(
            "Éxito",
            "Actividad completada.\n+100 puntos otorgados."
        )

    def marcar_incompleto(self):
        if not self.usuario_actual:
            messagebox.showwarning("Advertencia", "Busque un usuario primero.")
            return

        self.usuario_actual[4] = "Incompleto"
        self.guardar()

        messagebox.showinfo(
            "Éxito",
            "Actividad marcada como incompleta."
        )

    def guardar(self):
        with open(archivo, "w", encoding="utf-8") as f:
            for datos in self.lineas:
                f.write(" | ".join(datos) + "\n")

    def limpiar_labels(self):
        self.lbl_nombre.config(text="Nombre: -")
        self.lbl_apellido.config(text="Apellido: -")
        self.lbl_actividad.config(text="Actividad: -")

if __name__ == "__main__":
    Recompensas()
