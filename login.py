import tkinter as tk
app = tk.Tk()

ancho = 600
alto = 350 

pantalla_ancho = app.winfo_screenwidth()
pantalla_alto = app.winfo_screenheight()

x = (pantalla_ancho // 2) - (ancho // 2)
y = (pantalla_alto // 2) - (alto // 2)

app.geometry(f"{ancho}x{alto}+{x}+{y}")
app.config(background="white")
tk.Wm.wm_title(app,"Login")

frame = tk.Frame(app,bg="black")
frame.pack(expand = True)

logo = tk.Label(
    frame,
    text="MI PROYECTO",
    fg="white",
    bg="black",
    font=("Arial", 22, "bold")
)
logo.pack(pady=15)

lbl_nombre = tk.Label(frame, text="Nombre", fg="white", bg="black")
lbl_nombre.pack(anchor="w", padx=60)

entry_nombre = tk.Entry(frame, width=30)
entry_nombre.pack(pady=5)

lbl_pass = tk.Label(frame, text="Contraseña", fg="white", bg="black")
lbl_pass.pack(anchor="w", padx=60)

entry_pass = tk.Entry(frame, width=30, show="*")
entry_pass.pack(pady=5)

frame_botones = tk.Frame(frame, bg="black")
frame_botones.pack(pady=20)

btn_ingresar = tk.Button(frame_botones, text="Ingresar", width=12)
btn_ingresar.pack(side="left", padx=10)

btn_salir = tk.Button(
    frame_botones,
    text="Salir",
    width=12,
    command=app.destroy
)
btn_salir.pack(side="left", padx=10)

app.mainloop()
