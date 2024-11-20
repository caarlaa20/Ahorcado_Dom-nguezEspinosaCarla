import mysql.connector

# Establece la conexión con la base de datos usando los parámetros proporcionados.
class BBDD:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port="3306",
                database="JuegoAhorcado"
            )
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos exitosa.")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            self.conn = None
            self.cursor = None  #

   # Método que vamos a utilizar para imprimir las palabras de la tabla fruta
    def obtener_palabras_frutas(self):

        if self.conn:
            try:
                self.cursor.execute("SELECT nombre FROM Fruta")
                palabras = [row[0] for row in self.cursor.fetchall()]
                return palabras
            except mysql.connector.Error as err:

                print(f"Error al obtener palabras de frutas: {err}")
                return []
        else:
            print("No se pudo conectar a la base de datos.")
            return []



    # Método que vamos a utilizar para imprimir las palabras de la tabla informatica
    def obtener_palabras_informatica(self):

        if self.conn:
            try:
                self.cursor.execute("SELECT nombre FROM Informatica")
                palabras = [row[0] for row in self.cursor.fetchall()]
                return palabras
            except mysql.connector.Error as err:
                print(f"Error al obtener palabras de informática: {err}")
                return []
        else:
            print("No se pudo conectar a la base de datos.")
            return []


    # Método que vamos a utilizar para imprimir las palabras de la tabla nombres
    def obtener_palabras_nombres(self):

        if self.conn:
            try:
                self.cursor.execute("SELECT nombre FROM Nombres")
                palabras = [row[0] for row in self.cursor.fetchall()]
                return palabras
            except mysql.connector.Error as err:
                print(f"Error al obtener palabras de nombres: {err}")
                return []
        else:
            print("No se pudo conectar a la base de datos.")
            return []

    #Este es el método que vamos usar para registrar al usuario en cada partida
    def registrar_jugador(self, nombre):

        if self.conn:
            try:
                self.cursor.execute("SELECT id FROM jugadores WHERE nombre = %s", (nombre,))
                resultado = self.cursor.fetchone()

                if resultado:
                    print(f"Jugador '{nombre}' ya registrado con ID: {resultado[0]}")
                    return resultado[0]
                else:
                    self.cursor.execute("INSERT INTO jugadores (nombre) VALUES (%s)", (nombre,))
                    self.conn.commit()
                    jugador_id = self.cursor.lastrowid
                    print(f"Jugador '{nombre}' registrado con ID: {jugador_id}")
                    return jugador_id
            except mysql.connector.Error as err:
                print(f"Error al registrar jugador: {err}")
                return None
        else:
            print("No se pudo conectar a la base de datos.")
            return None

    #Utilizaremos este método para ver las partidas ganadas y las partidas perdidas de cada jugador y guardarla
    # en nuestra base de datos
    def actualizar_estadisticas(self, jugador_id, ganadas=0, perdidas=0):
        if self.conn:
            try:
                self.cursor.execute("""
                    UPDATE jugadores
                    SET partidas_ganadas = partidas_ganadas + %s,
                        partidas_perdidas = partidas_perdidas + %s
                    WHERE id = %s
                """, (ganadas, perdidas, jugador_id))
                self.conn.commit()  #
                print(f"Estadísticas actualizadas para jugador ID {jugador_id}.")
            except mysql.connector.Error as err:
                print(f"Error al actualizar estadísticas: {err}")
        else:
            print("No se pudo conectar a la base de datos.")

    #Este método lo utilizamos para cerrar la conexion con la base de datos cuendo terminemo de ejecutar el programa
    def cerrar_conexion(self):

        if self.conn:
            self.conn.close()
            print("Conexión cerrada.")
