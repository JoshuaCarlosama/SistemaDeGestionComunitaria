import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import os

def validar_texto(nuevo_texto):
    if len(nuevo_texto) > 20:
        return False
    return re.match("^[A-Za-z0-9]*$", nuevo_texto) is not None

def iniciar_sesion():
    usuario = entry_nombre.get()
    contrasena = entry_pass.get()
    
    if not usuario or not contrasena:
        messagebox.showwarning(
            "Campos vacíos",
            "Por favor, complete todos los campos."
        )
        return

    if usuario == "Admin" and contrasena == "123":
        messagebox.showinfo(
            "Acceso concedido",
            "Bienvenido Administrador"
        )
        app.destroy()
        os.system("python main.py")
    else:
        messagebox.showerror(
            "Acceso denegado",
            "Usuario o contraseña incorrectos."
        )

app = tk.Tk()

color_lila_claro = "#D1A8E1"
color_morado_fuerte = "#A546B6"
color_verde_fuerte = "#00674F"
color_fondo = "#F0F0F0"

ancho = 900
alto = 500

pantalla_ancho = app.winfo_screenwidth()
pantalla_alto = app.winfo_screenheight()

x = (pantalla_ancho // 2) - (ancho // 2)
y = (pantalla_alto // 2) - (alto // 2)

app.geometry(f"{ancho}x{alto}+{x}+{y}")
app.title("Login")
app.config(bg=color_fondo)

titulo = tk.Label(app,text="INICIO DE SESIÓN",font=("Arial", 22, "bold"),bg=color_morado_fuerte,fg="white",bd=5,relief=tk.GROOVE)
titulo.pack(fill=tk.X, pady=(10, 20))

contenedor = tk.Frame(app, bg=color_fondo)
contenedor.pack(pady=10)

img = Image.open("Recursos/PoliLogo.png")
img = img.resize((380, 200), Image.LANCZOS)
Logo = ImageTk.PhotoImage(img)

lbl_imagen = tk.Label(contenedor, image=Logo, bg=color_fondo)
lbl_imagen.image = Logo
lbl_imagen.pack(pady=(5, 10))

form = tk.Frame(contenedor, bg=color_fondo)
form.pack(pady=5)

vcmd = app.register(validar_texto)

tk.Label(form,text="Ingrese Usuario:",bg=color_lila_claro,fg="black",font=("Arial", 10, "bold"),width=20,anchor="w"
).grid(row=0, column=0, padx=10, pady=5)

entry_nombre = tk.Entry(form,width=30,validate="key",validatecommand=(vcmd, "%P"))
entry_nombre.grid(row=0, column=1, pady=5)

tk.Label(form,text="Ingrese Contraseña:",bg=color_lila_claro,fg="black",font=("Arial", 10, "bold"),width=20,anchor="w"
).grid(row=1, column=0, padx=10, pady=5)

entry_pass = tk.Entry(form,width=30,show="*",validate="key",validatecommand=(vcmd, "%P"))
entry_pass.grid(row=1, column=1, pady=5)

botones = tk.Frame(contenedor, bg=color_fondo)
botones.pack(pady=20)

tk.Button(botones,text="Ingresar",width=14,bg=color_verde_fuerte,fg="white",font=("Arial", 10, "bold"),command=iniciar_sesion
).grid(row=0, column=0, padx=15)

tk.Button(botones,text="Salir",width=14,bg=color_morado_fuerte,fg="white",font=("Arial", 10, "bold"),command=app.destroy
).grid(row=0, column=1, padx=15)

app.mainloop()