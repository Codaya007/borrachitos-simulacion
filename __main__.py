import matplotlib
import matplotlib.pyplot as plt
import random
import time
import tkinter as tk
from tkinter import ttk

MAX_PUNTOS_POR_CUADRICULA = 8 * 8

MAX_LIMITE_BORRACHITOS = round(MAX_PUNTOS_POR_CUADRICULA/2)


def generarCoordenadaNoRepetida(valoresNoRepetir):
    coordenadas = generate_random_cordinate()

    intentos = 12
    while (punto_repetido(valoresNoRepetir, coordenadas) and intentos > 0):
        coordenadas = generate_random_cordinate()
        intentos += 1

    return coordenadas


def generar_color_hexadecimal():
    """
    Genera un color hexadecimal aleatorio.

    Returns:
        str: Código hexadecimal del color generado.
    """
    # Generar valores aleatorios para los componentes RGB
    r = random.randint(5, 255)
    g = random.randint(5, 255)
    b = random.randint(5, 255)

    # Formar el código hexadecimal del color
    color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return color_hex


def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)


def generar_movimiento(currentX, currentY):
    # Generar un movimiento aleatorio en x o y (1 unidad a la vez)

    eje = random.choice(['x', 'y'])
    direccion = 1
    # Una vez generado el eje, debo determinar la dirección
    # Si el eje es x y el punto actual es 1, solo puede aumentar
    # Si el eje es x y el punto actual es 9, solo puede disminuir
    # Si no es ninguno, puede aumentar o disminuir
    # Lo mismo para 'y'
    if ((eje == "x" and currentX == 1) or (eje == "y" and currentY == 1)):
        direccion = 1
    elif ((eje == "x" and currentX == 9) or (eje == "y" and currentY == 9)):
        direccion = -1
    else:
        direccion = random.choice([1, -1])

    # determino los movimientos que puede dar el punto, puede moverse 1 paso tanto vertical como horizontalmente
    mov_random = 1 * direccion

    if eje == 'x':
        return mov_random, 0
    else:
        y = 1 * direccion
        return 0, mov_random


def punto_repetido(coordenadas, nuevo_punto):
    # Verificar si el nuevo punto ya existe en las coordenadas
    return nuevo_punto in coordenadas


def generar_movimiento_no_repetido(currentX, currentY, valoresANoRepetir):
    x, y = generar_movimiento(currentX, currentY)

    intentos = 5
    while (punto_repetido(valoresANoRepetir, [currentX, currentY]) and intentos > 0):
        x, y = generar_movimiento(currentX, currentY)
        intentos -= 1

    return x, y


def crear_matriz_vacia(filas):
    return [[] for _ in range(filas)]


def generate_random_cordinate():
    x = random.randint(1, 9)
    y = random.randint(1, 9)

    return [x, y]


def mostrar_ventana_ejecucion_borrachos(informacion_borrachitos):
    ventana = tk.Tk()
    ventana.title("Resumen de ejecución")

    # Ajustar el tamaño de la ventana y centrarla
    ancho_ventana = 800
    altura_ventana = 400
    x_pos = (ventana.winfo_screenwidth() - ancho_ventana) // 2
    y_pos = (ventana.winfo_screenheight() - altura_ventana) // 2
    ventana.geometry(f"{ancho_ventana}x{altura_ventana}+{x_pos}+{y_pos}")

    # Crear un Treeview para mostrar la tabla v2
    tabla = ttk.Treeview(ventana, columns=(
        "Borrachito", "Veces que comió", "Pasos dados", "Pasos restantes", "Estado"), show="headings")
    tabla.heading("Borrachito", text="Borrachito")
    tabla.heading("Veces que comió", text="Veces que comió")
    tabla.heading("Pasos dados", text="Pasos dados")
    tabla.heading("Pasos restantes", text="Pasos restantes")
    tabla.heading("Estado", text="Estado")

    # Insertar filas en la tabla
    for resultado in informacion_borrachitos:
        estado_texto = "Vivo" if resultado['tiempoVida'] > 0 else "Muerto"
        tabla.insert("", "end", values=(
            resultado['i'], resultado['vecesComio'], resultado['pasosTotales'], resultado['tiempoVida'], estado_texto))

    # Ajustar el tamaño de las columnas
    for columna in ("Borrachito", "Veces que comió", "Pasos dados", "Pasos restantes", "Estado"):
        tabla.column(columna, width=150, anchor="center")

    # Empaquetar la tabla en la ventana
    tabla.pack(padx=20, pady=10)

    # Iniciar el bucle de la interfaz gráfica
    ventana.mainloop()


def validar_coordenadas(xComida, yComida,
                        # xLlegada, yLlegada
                        ):
    # Desempaquetar las coordenadas
    coordenadas = generate_random_cordinate()
    [x, y] = coordenadas

    # Validar que las coordenadas no coincidan con el punto de comida ni el de llegada
    while (x == xComida and y == yComida):
        # or (x == xLlegada and y == yLlegada):
        # Generar nuevas coordenadas
        coordenadas = generate_random_cordinate()
        x, y = coordenadas

    return coordenadas


def isValidInput(inputMessage, min, max, minReason='', maxReason=''):
    inputValue = None
    try:
        inputValue = int(input(inputMessage))

        if (inputValue < min):
            print(
                f"El valor ingresado debe ser mayor a igual a {min} {minReason}")
            return False, inputValue

        if (inputValue > max):
            print(
                f"El valor ingresado debe ser menor a igual a {max} {maxReason}")
            return False, inputValue

        return True, inputValue
    except ValueError:
        print("El valor ingresado debe ser un número entero positivo")
        return False, inputValue


def menuIngresoDatos():
    print("============================ INGRESO DE DATOS ============================")
    limite_pasos = None
    n_borrachitos = None
    cantidad_comida = None
    tiempo_vida_inicial = None
    ejecuciones = None

    validLP = False
    while (not validLP):
        validLP, limite_pasos = isValidInput(
            "Ingrese el límite de pasos de la ejecución: ", 1, 100)

    validNB = False
    while not validNB:
        validNB, n_borrachitos = isValidInput(
            "Numero de borrachitos: ", 1, MAX_LIMITE_BORRACHITOS, "", " para que hayan suficientes puntos de comida y no se solapen")

    validCC = False
    while not validCC:
        validCC, cantidad_comida = isValidInput(
            "Ingrese la cantidad de puntos de comida: ", n_borrachitos + 1, MAX_PUNTOS_POR_CUADRICULA - n_borrachitos, " para que haya suficiente comida para los borrachitos", " para que hayan suficientes puntos libres para los borrachitos")

    validTVI = False
    while not validTVI:
        validTVI, tiempo_vida_inicial = isValidInput(
            "Ingrese el tiempo de vida por borrachito: ", 1, 100)

    validE = False
    while not validE:
        validE, ejecuciones = isValidInput(
            "Veces que desea ejecutar: ", 1, 500)

    return limite_pasos, n_borrachitos, cantidad_comida, tiempo_vida_inicial, ejecuciones


def convertir_a_lista_de_listas_por_nombre(lista_de_diccionarios, nombre_campo):
    return [diccionario[nombre_campo] for diccionario in lista_de_diccionarios if nombre_campo in diccionario]


try:
    limite_pasos, n_borrachitos, cantidad_comida, tiempo_vida_inicial, ejecuciones = menuIngresoDatos()

    TIEMPO_VIDA_INICIAL = 5
    PUNTOS_NO_REPETIR = 3
    resultados = crear_matriz_vacia(n_borrachitos)
    ESPACIO_POR_BORRACHO = 9/n_borrachitos + 0.5

    for ejecucion in range(ejecuciones):
        #! Inicialización variables importantes
        informacion_borrachitos = []  # Aquí van todos los detalles de los borrachitos
        # llegaron = 0
        murieron = 0
        # xComida = 3
        # yComida = 4
        # xLlegada = 5
        # yLlegada = 4

        #! Inicialización de la gráfica de ejecución actual
        plt.ion()  # Habilitar el modo interactivo

        # Crear la figura y los ejes
        fig, ax = plt.subplots()

        move_figure(fig, 600, 500)

        # Establecer el tamaño del gráfico en 6x6 pulgadas
        fig.set_size_inches(6, 6)

        # Establecer los límites de los ejes
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

        # Especificar los ticks de los ejes de 1 en 1
        ax.set_xticks(range(11))
        ax.set_yticks(range(11))

        # Añadir cuadrícula
        ax.grid(True)

        # Añadir título al gráfico completo
        plt.suptitle('SIMULACIÓN DE BORRACHITOS')

        plt.title(f'EJECUCIÓN {ejecucion + 1}')
        print(f"EJECUCIÓN {ejecucion + 1}")

        #! Puntos de comida en verde
        puntosComidaData = []

        for i in range(cantidad_comida):
            coordenadas = generarCoordenadaNoRepetida(convertir_a_lista_de_listas_por_nombre(
                puntosComidaData, "coordenadas"))

            [xComida, yComida] = coordenadas

            puntoComida = ax.scatter(x=[xComida], y=[yComida], color='green')

            textoComida = ax.text(xComida + 0.5, yComida - 0.5, "C" + str(i + 1), ha='center',
                                  va='center', fontsize=7, bbox=dict(facecolor='white', alpha=0.7))

            puntosComidaData.append(
                {"puntoComida": puntoComida, "textoComida": textoComida, "coordenadas": coordenadas})

        coordenadasComida = convertir_a_lista_de_listas_por_nombre(
            puntosComidaData, "coordenadas")

        #! Inicializo los borrachos
        for i in range(n_borrachitos):
            # ? Valida que la coordenada de inicio no pueda ser el punto de comida
            [x, y] = generarCoordenadaNoRepetida(
                coordenadasComida + convertir_a_lista_de_listas_por_nombre(informacion_borrachitos, "posicionActual"))

            # ? Punto punto inicial de borrachito i en rojo
            ax.scatter(x=[x], y=[y], color='red')
            ax.text(x + 0.5, y + 0.5, "B" + str(i + 1), ha='center',
                    va='center', fontsize=8, bbox=dict(facecolor='green', alpha=0.7))

            color = generar_color_hexadecimal()

            # ? Añado toda la información del estado del borracho
            informacion_borrachitos.append({
                "i": i + 1,
                'posicionActual': [x, y],
                'tiempoVida': tiempo_vida_inicial,
                'coordenadas': [[x, y]],
                'vecesComio': 0,
                'pasosTotales': 0,
                'color': color
            })

        pasos_dados = 0
        #! Mientras todos los borrachos no estén muertos o se hayan dado los pasos totales, sigo generando puntos
        while ((murieron != n_borrachitos) and (pasos_dados < limite_pasos)):
            # Esperar 0.5 segundo
            time.sleep(0.5)

            for i in range(n_borrachitos):
                # ? Validacion: Si el borrachito actual ya llegó o ya se murió, lo ignoro
                if (informacion_borrachitos[i]['tiempoVida'] <= 0):
                    continue

                # ? El punto anterior ahora es el punto inicial
                [x0, y0] = informacion_borrachitos[i]["posicionActual"]

                # Genero nuevo movimiento
                dx, dy = generar_movimiento_no_repetido(
                    x0, y0, informacion_borrachitos[i]['coordenadas'])

                # Actualizo las nuevas coordenadas
                x1 = x0 + dx
                y1 = y0 + dy

                informacion_borrachitos[i]["posicionActual"][0] = x1
                informacion_borrachitos[i]["posicionActual"][1] = y1

                # Terminando el bucle, significa que se generó un nuevo paso válido en posicionActual
                [x1, y1] = informacion_borrachitos[i]["posicionActual"]

                # Pasos totales aumentan
                informacion_borrachitos[i]["pasosTotales"] += 1

                # Tiempo de vida disminuye
                informacion_borrachitos[i]["tiempoVida"] -= 1

                # Se añaden las nuevas coordenadas al registro para que no se repitan los puntos
                informacion_borrachitos[i]["coordenadas"].append([x1, y1])
                informacion_borrachitos[i]["coordenadas"] = informacion_borrachitos[i]["coordenadas"][-PUNTOS_NO_REPETIR:]

                # Dibujo la línea entre los puntos
                ax.plot([x0, x1], [y0, y1],
                        informacion_borrachitos[i]['color'])

                #! Si el nuevo punto es un punto de comida, lo elimino. Solo se puede comer una vez, luego de eso la comida desaparece
                for obj in puntosComidaData:
                    if (obj["coordenadas"] == [x1, y1]):
                        print(
                            f"BORRACHITO {str(i+1)} PASÓ POR PUNTO DE COMIDA: {obj['coordenadas']}\n")

                        informacion_borrachitos[i]["tiempoVida"] += tiempo_vida_inicial
                        informacion_borrachitos[i]["vecesComio"] += 1

                        obj["coordenadas"] = [None, None]

                        obj["puntoComida"].remove()
                        obj["textoComida"].remove()

                # Si ya no le quedan movimientos al borracho actual muestro un texto informativo de q murió
                if (informacion_borrachitos[i]["tiempoVida"] <= 0):
                    murieron += 1
                    # ax.text((i * ESPACIO_POR_BORRACHO), 9.5, "B" + str(i+1) + " murió",
                    #         ha='center', va='center', fontsize=8, bbox=dict(facecolor='white', alpha=0.7))

            # Actualizar la figura
            fig.canvas.draw_idle()

            plt.pause(2)

            # print(informacion_borrachitos)
            pasos_dados += 1

        print(f"TERMINA EJECUCIÓN {ejecucion + 1}")

        if (murieron < n_borrachitos):
            msg = ""
            for i in range(n_borrachitos):
                tiempoVida = informacion_borrachitos[i]["tiempoVida"]

                if (tiempoVida > 0):
                    msg += "borrachito " + str(i+1)

            ax.text(4.5, 9.5, msg + " llegaron a la meta",
                    ha='center', va='center', fontsize=10, bbox=dict(facecolor='green', alpha=0.7))
        else:
            ax.text(2, 9.5, "Nadie ganó",
                    ha='center', va='center', fontsize=10, bbox=dict(facecolor='red', alpha=0.7))

        for i in range(n_borrachitos):
            resultados[i].append(informacion_borrachitos[i])

        plt.pause(1200)

        # Cerrar la figura al finalizar
        plt.ioff()  # Deshabilitar el modo interactivo

        # Cerrar el gráfico
        plt.close()

        mostrar_ventana_ejecucion_borrachos(informacion_borrachitos)

        print(resultados)
except KeyboardInterrupt:
    print('\n\nPROGRAMA CERRADO')
