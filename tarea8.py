def verificarGanador(tabero, jugador):
    for i in range(3):

        if tabero[i][0] == tabero[i][1] == tabero[i][2] == jugador:
            return True
        # Comprobar las columnasumnas
        elif tabero[0][i] == tabero[1][i] == tabero[2][i] == jugador:
            return True
    # Comprobar las diagonales
    if tabero[0][0] == tabero[1][1] == tabero[2][2] == jugador:
        return True
    elif tabero[0][2] == tabero[1][1] == tabero[2][0] == jugador:
        return True
    return False

def obtenerMovimientosPosibles(tabero):
    movimientos = []
    for i in range(3):
        for j in range(3):
            if tabero[i][j] == "":
                movimientos.append((i, j))
    return movimientos

def hacerMovimiento(tabero, movimiento, jugador):
    # Realiza una jugada en el tablero dado
    # Devuelve el nuevo tablero después de la jugada
    nuevoTablero = [filas[:] for filas in tabero] # hacer una copia del tablero
    i, j = movimiento
    nuevoTablero[i][j] = jugador
    return nuevoTablero

def evaluate(tabero):
    # Evalúa el tablero y devuelve un valor numérico que representa la calidad de la posición
    if verificarGanador(tabero, "X"):
        return 1
    elif verificarGanador(tabero, "O"):
        return -1
    else:
        return 0

def minimax(tabero, alpha, beta, JugadorQueMaximiza):
    # Algoritmo Minimax con poda alfa-beta
    if verificarGanador(tabero, "X") or verificarGanador(tabero, "O"):
        return evaluate(tabero)

    if JugadorQueMaximiza:
        max_eval = float("-inf")
        for movimiento in obtenerMovimientosPosibles(tabero):
            nuevoTablero = hacerMovimiento(tabero, movimiento, "X")
            eval = minimax(nuevoTablero, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for movimiento in obtenerMovimientosPosibles(tabero):
            nuevoTablero = hacerMovimiento(tabero, movimiento, "O")
            eval = minimax(nuevoTablero, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def obtenerMejorMovimiento(tabero, JugadorQueMaximiza):
    # Devuelve la mejor jugada para un jugador dado un estado del tablero
    best_eval = float("-inf") if JugadorQueMaximiza else float("inf")
    mejorMovimiento = None
    for movimiento in obtenerMovimientosPosibles(tabero):
        nuevoTablero = hacerMovimiento(tabero, movimiento, "X" if JugadorQueMaximiza else "O")
        eval = minimax(nuevoTablero, float("-inf"), float("inf"), not JugadorQueMaximiza)
        if JugadorQueMaximiza and eval > best_eval:
            best_eval = eval
            mejorMovimiento = movimiento
        elif not JugadorQueMaximiza and eval < best_eval:
            best_eval = eval
            mejorMovimiento = movimiento
    return mejorMovimiento

# Ejemplo de uso:
tabero = [["", "", ""], ["", "", ""], ["", "", ""]]
turno = "X"

while True:
    # Mostrar el tablero
    print("Tablero:")
    for filas in tabero:
        print(filas)

    if verificarGanador(tabero, "X"):
        print("¡Has ganado!")
        break
    elif verificarGanador(tabero, "O"):
        print("¡Has perdido!")
        break
    elif len(obtenerMovimientosPosibles(tabero)) == 0:
        print("¡Empate!")
        break

    if turno == "X":
        # Jugador humano
        filas = int(input("Elige una fila (0, 1, 2): "))
        columnas = int(input("Elige una columnasumna (0, 1, 2): "))
        if tabero[filas][columnas] != "":
            print("Esa celda ya está ocupada. Inténtalo de nuevo.")
            continue
        tabero[filas][columnas] = "X"
    else:
        # Jugador IA
        print("turnoo de la IA...")
        movimiento = obtenerMejorMovimiento(tabero, False)
        tabero[movimiento[0]][movimiento[1]] = "O"

    turno = "X" if turno == "O" else "O"
