"""
=====================================================================
 PROYECTO DE ARREGLOS - RESISTENCIA ELÉCTRICA
 Estructuras de Datos - Anáhuac Mayab
=====================================================================
Objetivo:
  1. Determinar los colores de una resistencia a partir de su valor
     en ohmios (Primera banda, Segunda banda, Multiplicador).
  2. Calcular el valor total de 'n' resistencias en serie y en
     paralelo, generadas con valores aleatorios entre 10 y
     1,000,000,000.

Restricción técnica:
  El almacenamiento, recorrido y suma de las 'n' resistencias
  aleatorias se realiza EXCLUSIVAMENTE con una Lista Enlazada
  (NodoLista / Lista) provista por el profesor. No se usan listas
  nativas de Python para ese propósito.

Estructura del archivo:
  1) LÓGICA DE ESTRUCTURA DE DATOS -> NodoLista, Lista
  2) LÓGICA DE NEGOCIO            -> Resistencia, GeneradorResistencias
  3) INTERFAZ GRÁFICA (tkinter)   -> AplicacionResistencia
=====================================================================
"""

import random
import tkinter as tk
from tkinter import ttk, messagebox


# =====================================================================
# 1) LÓGICA DE ESTRUCTURA DE DATOS: NODO Y LISTA ENLAZADA
# =====================================================================
# Esta es la implementación base proporcionada en clase. Se conserva
# la lógica original de los nodos y se agregan métodos a la clase
# Lista para poder recorrerla y calcular las sumas requeridas, sin
# alterar el funcionamiento interno de NodoLista.
# =====================================================================

class NodoLista:
    """Representa un nodo individual de la lista enlazada."""

    def __init__(self, objeto, nodo=None):
        self.datos = objeto            # Dato almacenado (valor de la resistencia)
        self.siguienteNodo = nodo      # Referencia al siguiente nodo

    def obtenerObject(self):
        return self.datos

    def obtenerSiguiente(self):
        return self.siguienteNodo


class Lista:
    """Lista enlazada simple utilizada para almacenar los valores
    de resistencia generados aleatoriamente."""

    def __init__(self, nombreLista="lista"):
        self.nombre = nombreLista
        self.primerNodo = None
        self.ultimoNodo = None

    def insertarAlFrente(self, elementoInsertar):
        if self.estaVacia():
            self.primerNodo = self.ultimoNodo = NodoLista(elementoInsertar)
        else:
            self.primerNodo = NodoLista(elementoInsertar, self.primerNodo)

    def insertarAlFinal(self, elementoInsertar):
        if self.estaVacia():
            self.primerNodo = self.ultimoNodo = NodoLista(elementoInsertar)
        else:
            self.ultimoNodo.siguienteNodo = NodoLista(elementoInsertar)
            self.ultimoNodo = self.ultimoNodo.siguienteNodo

    def estaVacia(self):
        return self.primerNodo is None

    # ---------------------------------------------------------------
    # Métodos agregados para cubrir las necesidades del proyecto.
    # No modifican la lógica de NodoLista, solo recorren la lista
    # usando obtenerSiguiente()/obtenerObject() ya existentes.
    # ---------------------------------------------------------------

    def obtenerValores(self):
        """Recorre la lista enlazada y regresa los valores como una
        tupla (se usa tupla, no lista nativa, solo para poder
        entregarlos a la interfaz; el almacenamiento y cálculo real
        siempre se hace recorriendo los nodos)."""
        valores = ()
        nodoActual = self.primerNodo
        while nodoActual is not None:
            valores += (nodoActual.obtenerObject(),)
            nodoActual = nodoActual.obtenerSiguiente()
        return valores

    def calcularSumaSerie(self):
        """Rts = R1 + R2 + R3 + ... + RN, recorriendo los nodos."""
        suma = 0
        nodoActual = self.primerNodo
        while nodoActual is not None:
            suma += nodoActual.obtenerObject()
            nodoActual = nodoActual.obtenerSiguiente()
        return suma

    def calcularInversoParalelo(self):
        """Devuelve 1/R1 + 1/R2 + ... + 1/RN (el inverso de la suma
        de inversos), recorriendo los nodos."""
        sumaInversos = 0.0
        nodoActual = self.primerNodo
        while nodoActual is not None:
            valor = nodoActual.obtenerObject()
            if valor != 0:
                sumaInversos += 1 / valor
            nodoActual = nodoActual.obtenerSiguiente()
        return sumaInversos

    def cantidadNodos(self):
        contador = 0
        nodoActual = self.primerNodo
        while nodoActual is not None:
            contador += 1
            nodoActual = nodoActual.obtenerSiguiente()
        return contador


# =====================================================================
# 2) LÓGICA DE NEGOCIO
# =====================================================================

class Resistencia:
    """Representa una resistencia eléctrica y calcula sus bandas de
    color a partir de su valor en ohmios."""

    # Tabla estándar: color -> (dígito, color hexadecimal para el dibujo)
    TABLA_COLORES = {
        0: ("Negro",    "#000000"),
        1: ("Marrón",   "#8B4513"),
        2: ("Rojo",     "#FF0000"),
        3: ("Naranja",  "#FFA500"),
        4: ("Amarillo", "#FFD700"),
        5: ("Verde",    "#008000"),
        6: ("Azul",     "#0000FF"),
        7: ("Violeta",  "#8A2BE2"),
        8: ("Gris",     "#808080"),
        9: ("Blanco",   "#FFFFFF"),
    }

    def __init__(self, valorOhmios):
        if valorOhmios < 0:
            raise ValueError("El valor de la resistencia no puede ser negativo.")
        self.valorOhmios = int(valorOhmios)

    def obtenerBandasDeColor(self):
        """Calcula la 1a banda, 2a banda y multiplicador a partir del
        valor en ohmios, usando la tabla de dígitos 0-9.

        Ejemplo: 160 -> primer dígito 1 (Marrón), segundo dígito 6
        (Azul), y el resto (10^1) corresponde al multiplicador
        Marrón (10). Resultado: Marrón, Azul, Marrón.
        """
        valorTexto = str(self.valorOhmios)

        if len(valorTexto) < 2:
            # Si el valor tiene un solo dígito, se completa con un 0
            # para poder obtener dos dígitos significativos.
            valorTexto = "0" + valorTexto

        primerDigito = int(valorTexto[0])
        segundoDigito = int(valorTexto[1])
        # El multiplicador es la potencia de 10 necesaria para
        # reconstruir el valor original a partir de los dos primeros
        # dígitos significativos.
        exponente = len(valorTexto) - 2

        nombrePrimero, hexPrimero = self.TABLA_COLORES[primerDigito]
        nombreSegundo, hexSegundo = self.TABLA_COLORES[segundoDigito]
        nombreMultiplicador, hexMultiplicador = self.TABLA_COLORES[exponente % 10] \
            if exponente in self.TABLA_COLORES else (f"10^{exponente}", "#CCCCCC")

        return {
            "primera_banda": (nombrePrimero, hexPrimero),
            "segunda_banda": (nombreSegundo, hexSegundo),
            "multiplicador": (nombreMultiplicador, hexMultiplicador),
        }

    def __str__(self):
        return f"Resistencia({self.valorOhmios} Ω)"


class GeneradorResistencias:
    """Genera 'n' resistencias con valores aleatorios y las almacena
    en una Lista enlazada. Calcula los totales en serie y paralelo
    apoyándose en los métodos de la clase Lista."""

    VALOR_MINIMO = 10
    VALOR_MAXIMO = 1_000_000_000

    def __init__(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad de resistencias (n) debe ser mayor a 0.")
        self.cantidad = cantidad
        self.lista = Lista("resistencias_generadas")
        self._generarValores()

    def _generarValores(self):
        """Genera 'n' valores aleatorios y los inserta al final de
        la lista enlazada, uno por uno."""
        for _ in range(self.cantidad):
            valorAleatorio = random.randint(self.VALOR_MINIMO, self.VALOR_MAXIMO)
            self.lista.insertarAlFinal(valorAleatorio)

    def obtenerValoresGenerados(self):
        return self.lista.obtenerValores()

    def calcularTotalSerie(self):
        """Rts = R1 + R2 + ... + RN"""
        return self.lista.calcularSumaSerie()

    def calcularTotalParalelo(self):
        """Rtp = 1 / (1/R1 + 1/R2 + ... + 1/RN)"""
        inversoTotal = self.lista.calcularInversoParalelo()
        if inversoTotal == 0:
            return 0
        return 1 / inversoTotal


# =====================================================================
# 3) INTERFAZ GRÁFICA (tkinter)
# =====================================================================

class AplicacionResistencia:
    """Ventana principal de la aplicación. Contiene dos pestañas:
    una para el cálculo de bandas de color y otra para el cálculo
    de resistencias en serie/paralelo."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Proyecto de Arreglos - Resistencia Eléctrica")
        self.raiz.geometry("640x520")
        self.raiz.resizable(False, False)

        self._crearNotebook()

    # -----------------------------------------------------------
    # Construcción general de pestañas
    # -----------------------------------------------------------
    def _crearNotebook(self):
        notebook = ttk.Notebook(self.raiz)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        pestañaColores = ttk.Frame(notebook)
        pestañaSeriesParalelo = ttk.Frame(notebook)

        notebook.add(pestañaColores, text="Colores de Resistencia")
        notebook.add(pestañaSeriesParalelo, text="Serie y Paralelo")

        self._construirPestañaColores(pestañaColores)
        self._construirPestañaSeriesParalelo(pestañaSeriesParalelo)

    # -----------------------------------------------------------
    # PESTAÑA 1: Colores de la resistencia
    # -----------------------------------------------------------
    def _construirPestañaColores(self, contenedor):
        tk.Label(
            contenedor, text="Ingresa el valor de la resistencia (Ω):",
            font=("Segoe UI", 11)
        ).pack(pady=(20, 5))

        self.entradaValorResistencia = tk.Entry(contenedor, font=("Segoe UI", 11), width=20)
        self.entradaValorResistencia.pack(pady=5)

        tk.Button(
            contenedor, text="Calcular colores",
            command=self._calcularColores, bg="#FF7A00", fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=10)

        # Lienzo donde se dibuja la resistencia con sus bandas
        self.canvasResistencia = tk.Canvas(contenedor, width=560, height=160, bg="white",
                                            highlightthickness=1, highlightbackground="#CCCCCC")
        self.canvasResistencia.pack(pady=10)

        self.etiquetaResultadoColores = tk.Label(
            contenedor, text="", font=("Segoe UI", 11), justify="left"
        )
        self.etiquetaResultadoColores.pack(pady=10)

        self._dibujarResistenciaBase()  # Dibuja el cuerpo sin bandas al iniciar

    def _dibujarResistenciaBase(self, bandas=None):
        """Dibuja el cuerpo de la resistencia y, si se le pasa un
        diccionario de bandas, pinta las franjas de color
        correspondientes (primera banda, segunda banda,
        multiplicador)."""
        canvas = self.canvasResistencia
        canvas.delete("all")

        # Terminales (patitas) de la resistencia
        canvas.create_line(20, 80, 130, 80, width=4, fill="#888888")
        canvas.create_line(430, 80, 540, 80, width=4, fill="#888888")

        # Cuerpo color beige de la resistencia
        canvas.create_rectangle(130, 40, 430, 120, fill="#E8C79A", outline="#A67C52", width=2)

        if bandas:
            posiciones = [190, 250, 310]
            claves = ["primera_banda", "segunda_banda", "multiplicador"]
            for x, clave in zip(posiciones, claves):
                nombreColor, colorHex = bandas[clave]
                canvas.create_rectangle(x, 40, x + 20, 120, fill=colorHex, outline="")
                canvas.create_text(
                    x + 10, 135, text=nombreColor, font=("Segoe UI", 8), angle=0
                )

    def _calcularColores(self):
        textoValor = self.entradaValorResistencia.get().strip()
        if not textoValor.isdigit():
            messagebox.showerror("Valor inválido", "Ingresa un número entero positivo en ohmios.")
            return

        try:
            resistencia = Resistencia(int(textoValor))
            bandas = resistencia.obtenerBandasDeColor()
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return

        self._dibujarResistenciaBase(bandas)

        texto = (
            f"Primera banda:   {bandas['primera_banda'][0]}\n"
            f"Segunda banda:   {bandas['segunda_banda'][0]}\n"
            f"Multiplicador:   {bandas['multiplicador'][0]}"
        )
        self.etiquetaResultadoColores.config(text=texto)

    # -----------------------------------------------------------
    # PESTAÑA 2: Resistencias en serie y en paralelo
    # -----------------------------------------------------------
    def _construirPestañaSeriesParalelo(self, contenedor):
        tk.Label(
            contenedor, text="Cantidad de resistencias a generar (n):",
            font=("Segoe UI", 11)
        ).pack(pady=(20, 5))

        self.entradaCantidad = tk.Entry(contenedor, font=("Segoe UI", 11), width=20)
        self.entradaCantidad.pack(pady=5)

        tk.Button(
            contenedor, text="Generar y calcular",
            command=self._generarYCalcular, bg="#FF7A00", fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=10)

        # Lista visual (Listbox) donde se muestran los valores generados,
        # los cuales se obtienen recorriendo la lista enlazada.
        marcoLista = tk.Frame(contenedor)
        marcoLista.pack(pady=5, fill="both", expand=False)

        tk.Label(marcoLista, text="Resistencias generadas (nodos de la lista enlazada):",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")

        scrollbar = tk.Scrollbar(marcoLista)
        scrollbar.pack(side="right", fill="y")

        self.listboxValores = tk.Listbox(marcoLista, width=60, height=8,
                                          yscrollcommand=scrollbar.set)
        self.listboxValores.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listboxValores.yview)

        self.etiquetaResultadoSerieParalelo = tk.Label(
            contenedor, text="", font=("Segoe UI", 11, "bold"), justify="left"
        )
        self.etiquetaResultadoSerieParalelo.pack(pady=15)

    def _generarYCalcular(self):
        textoCantidad = self.entradaCantidad.get().strip()
        if not textoCantidad.isdigit() or int(textoCantidad) <= 0:
            messagebox.showerror("Valor inválido", "Ingresa un número entero positivo para n.")
            return

        n = int(textoCantidad)

        try:
            generador = GeneradorResistencias(n)
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return

        # Se recorre la lista enlazada para mostrar los valores generados
        self.listboxValores.delete(0, tk.END)
        for indice, valor in enumerate(generador.obtenerValoresGenerados(), start=1):
            self.listboxValores.insert(tk.END, f"R{indice} = {valor} Ω")

        totalSerie = generador.calcularTotalSerie()
        totalParalelo = generador.calcularTotalParalelo()

        texto = (
            f"Rts (Serie)    = {totalSerie:,} Ω\n"
            f"Rtp (Paralelo) = {totalParalelo:,.4f} Ω"
        )
        self.etiquetaResultadoSerieParalelo.config(text=texto)


# =====================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =====================================================================

def main():
    raiz = tk.Tk()
    AplicacionResistencia(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
