from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import random

from bbdd import BBDD


class Juego:
    def __init__(self, root, bbdd):

        self.root = root
        self.root.title("Juego del Ahorcado")
        self.root.config(bg="lightblue")

        self.bbdd = bbdd

        # Solicitamos el nombre del jugador
        self.nombre_jugador = self.pedir_nombre_jugador()
        if not self.nombre_jugador:
            return

        # Solicitamos  la  categoría de palabras
        self.categoria = self.pedir_categoria()

        # Cargamos las palabras con la categoría seleccionada
        if self.categoria == "Frutas":
            self.palabras = self.bbdd.obtener_palabras_frutas()
        elif self.categoria == "Informática":
            self.palabras = self.bbdd.obtener_palabras_informatica()
        elif self.categoria == "Nombres":
            self.palabras = self.bbdd.obtener_palabras_nombres()

        # Verificamos si se cargaron las palabras
        if not self.palabras:
            messagebox.showerror("Error", "No se pudieron cargar las palabras desde la base de datos.")
            self.root.quit()
            return

        # Registramos al jugador en la base de datos
        self.jugador_id = self.bbdd.registrar_jugador(self.nombre_jugador)


        self.intentos = 6
        self.palabra_secreta = random.choice(self.palabras)
        self.letras_adivinadas = []
        self.palabra_mostrada = ["_"] * len(self.palabra_secreta)

        # Partidas ganadas y perdidas
        self.partidas_ganadas = 0
        self.partidas_perdidas = 0


        self.label_palabra = tk.Label(self.root, text=" ".join(self.palabra_mostrada), font=("Courier", 24, "bold"),
                                      bg="lightblue")
        self.label_palabra.pack(pady=20)
        self.label_estadisticas = tk.Label(self.root, text=f"Ganadas: {self.partidas_ganadas} - Perdidas: {self.partidas_perdidas}",
                                           font=("Courier", 14, "bold"), bg="lightblue")
        self.label_estadisticas.pack(pady=10)

        self.canvas_width = 400
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="lightblue")
        self.canvas.pack(pady=10)

        self.imagenes = [
            ImageTk.PhotoImage(Image.open(f"ahorcado{i}.png").resize((300, 300))) for i in range(7)
        ]


        self.imagen_actual_id = None
        self.mostrar_imagen_centrada(self.imagenes[0])

        # Entrada de texto para que el jugador ingrese una letra
        self.entry_letra = tk.Entry(self.root, font=("Courier", 16, "bold"))
        self.entry_letra.pack(pady=10)

        #Boton de Adivinar
        self.boton_adivinar = tk.Button(self.root, text="Adivinar", font=("Courier", 16, "bold"), command=self.adivinar,
                                        bg="lightgreen")
        self.boton_adivinar.pack(pady=10)

        # Botón para reiniciar el juego
        self.boton_reset = tk.Button(self.root, text="Reiniciar", font=("Courier", 16, "bold"), command=self.reiniciar,
                                     state=tk.DISABLED, bg="lightcoral")
        self.boton_reset.pack(pady=10)


        self.root.mainloop()

    #Función para pedirle el nombre al jugador
    def pedir_nombre_jugador(self):
        def on_submit():
            nombre = entry.get().strip()
            if nombre:
                self.root.quit()
            else:
                messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre.")
        nombre_ventana = tk.Toplevel(self.root)
        nombre_ventana.title("Ingreso de Nombre")
        nombre_ventana.config(bg="lightblue")

        label = tk.Label(nombre_ventana, text="Ingresa tu nombre:", font=("Courier", 14, "bold"), bg="lightblue")
        label.pack(pady=10)

        entry = tk.Entry(nombre_ventana, font=("Courier", 14), bg="lightgreen")
        entry.pack(pady=10)

        submit_btn = tk.Button(nombre_ventana, text="Aceptar", font=("Courier", 14, "bold"), command=on_submit, bg="lightcoral")
        submit_btn.pack(pady=10)
        nombre_ventana.mainloop()
        return entry.get().strip()


    #Función para pedir la categoría
    def pedir_categoria(self):
        def on_submit():
            categoria = selected_category.get()
            if categoria:
                self.root.quit()
            else:
                messagebox.showwarning("Advertencia", "Por favor, seleccione una categoría.")


        categoria_ventana = tk.Toplevel(self.root)
        categoria_ventana.title("Seleccionar Categoría")
        categoria_ventana.config(bg="lightblue")

        label = tk.Label(categoria_ventana, text="Selecciona una categoría:", font=("Courier", 14, "bold"), bg="lightblue")
        label.pack(pady=10)
        selected_category = tk.StringVar()
        selected_category.set(None)

        # Categorías disponibles
        categorias = ["Frutas", "Informática", "Nombres"]
        for categoria in categorias:
            radio_btn = tk.Radiobutton(categoria_ventana, text=categoria, variable=selected_category, value=categoria,
                                       font=("Courier", 12), bg="lightblue")
            radio_btn.pack(pady=5)


        submit_btn = tk.Button(categoria_ventana, text="Aceptar", font=("Courier", 14, "bold"), command=on_submit, bg="lightcoral")
        submit_btn.pack(pady=10)


        categoria_ventana.mainloop()
        return selected_category.get()

    #Función para reiniciar y resetear los intentos
    def reiniciar(self):
        self.intentos = 6
        self.palabra_secreta = random.choice(self.palabras)
        self.letras_adivinadas = []
        self.palabra_mostrada = ["_"] * len(self.palabra_secreta)
        self.label_palabra.config(text=" ".join(self.palabra_mostrada))
        self.mostrar_imagen_centrada(self.imagenes[0])
        self.boton_reset.config(state=tk.DISABLED)

    #Nos muestra la imagen centrada y elimina la anterior
    def mostrar_imagen_centrada(self, imagen):
        if self.imagen_actual_id is not None:
            self.canvas.delete(self.imagen_actual_id)

        canvas_center_x = self.canvas_width // 2
        canvas_center_y = self.canvas_height // 2
        img_width = imagen.width()
        img_height = imagen.height()
        x_position = canvas_center_x - img_width // 2
        y_position = canvas_center_y - img_height // 2

        self.imagen_actual_id = self.canvas.create_image(x_position, y_position, anchor="nw", image=imagen)

    #Funcion adivinar
    def adivinar(self):
        letra = self.entry_letra.get().lower()
        self.entry_letra.delete(0, tk.END)

        # Verificamos que solo se ingrese una letra
        if len(letra) != 1 or not letra.isalpha():
            messagebox.showwarning("Advertencia", "Por favor ingrese solo una letra.")
            return

        # Verificamos si la letra ya fue adivinada
        if letra in self.letras_adivinadas:
            messagebox.showwarning("Advertencia", "Ya adivinaste esa letra.")
            return

        # Añadimos la letra a las letras adivinadas
        self.letras_adivinadas.append(letra)

        # Comprobamos si la letra está en la palabra secreta
        if letra in self.palabra_secreta:
            for i, letra_palabra in enumerate(self.palabra_secreta):
                if letra_palabra == letra:
                    self.palabra_mostrada[i] = letra

            self.label_palabra.config(text=" ".join(self.palabra_mostrada))

            # Comprobamos si el jugador ha ganado
            if "_" not in self.palabra_mostrada:
                self.partidas_ganadas += 1
                self.label_estadisticas.config(
                    text=f"Ganadas: {self.partidas_ganadas} - Perdidas: {self.partidas_perdidas}"
                )

                self.bbdd.actualizar_estadisticas(self.jugador_id, ganadas=1)

                messagebox.showinfo("¡Ganaste!", f"¡Felicidades {self.nombre_jugador}! Has adivinado la palabra.")
                self.boton_reset.config(state=tk.NORMAL)
        else:
            self.intentos -= 1
            self.mostrar_imagen_centrada(self.imagenes[6 - self.intentos])
            if self.intentos == 0:
                self.partidas_perdidas += 1
                self.label_estadisticas.config(
                    text=f"Ganadas: {self.partidas_ganadas} - Perdidas: {self.partidas_perdidas}"
                )
                self.bbdd.actualizar_estadisticas(self.jugador_id, perdidas=1)

                messagebox.showinfo("Perdiste", f"Perdiste, la palabra era: {self.palabra_secreta}")
                self.boton_reset.config(state=tk.NORMAL)



bbdd = BBDD(host="localhost", user="root", password="", database="JuegoAhorcado")


root = tk.Tk()
juego = Juego(root, bbdd)


bbdd.cerrar_conexion()
