"""5. Resolutor de Sudoku
Utiliza la biblioteca pygame (consulta las instrucciones de instalación de pip) para
implementar una interfaz gráfica (GUI) que resuelve automáticamente los rompecabezas de
Sudoku.
Para resolver un rompecabezas de Sudoku, puedes crear un programa que utilice un algoritmo
de retroceso (backtracking) que verifica incrementalmente soluciones, adoptando o
abandonando la solución actual si no es viable.
Este paso de abandonar una solución es la característica definitoria de un enfoque de
retroceso, ya que el programa retrocede para probar una nueva solución hasta que encuentra
una válida. Este proceso se lleva a cabo de manera incremental hasta que todo el tablero se
haya completado correctamente"""

import pygame  # Importa el módulo pygame para manejar la interfaz gráfica
import sys  # Importa el módulo sys para manejar la salida del programa

# Inicializar Pygame
pygame.init()  # Inicializa el motor de Pygame

# Constantes de la ventana
CELL_SIZE = 60  # Tamaño de cada celda del tablero
LINE_WIDTH = 2  # Ancho de las líneas que dibujan el tablero
THICK_LINE_WIDTH = 4  # Ancho de las líneas gruesas que dividen las regiones del tablero
WINDOW_PADDING = 50  # Espaciado entre el borde de la ventana y el tablero
FONT_SIZE = 30  # Tamaño de la fuente para los números en las celdas
WHITE = (255, 255, 255)  # Color blanco
BLACK = (0, 0, 0)  # Color negro
RED = (255, 0, 0)  # Color rojo (se usa para resaltar la celda seleccionada)

# Función para crear un tablero de Sudoku vacío
def create_empty_board(rows, cols):
    """Crea un tablero de Sudoku vacío con el número de filas y columnas especificado."""
    return [[0 for _ in range(cols)] for _ in range(rows)]

# Función para dibujar el tablero de Sudoku
def draw_board(board, window, selected_cell):
    """Dibuja el tablero de Sudoku en la ventana especificada."""
    window.fill(WHITE)  # Rellena la ventana con color blanco
    rows = len(board)  # Obtiene el número de filas en el tablero
    cols = len(board[0])  # Obtiene el número de columnas en el tablero
    for i in range(rows):
        for j in range(cols):
            # Dibuja las líneas horizontales y verticales que forman el tablero
            if i % 3 == 0 and j % 3 == 0:
                pygame.draw.rect(window, BLACK, (j*CELL_SIZE+WINDOW_PADDING, i*CELL_SIZE+WINDOW_PADDING, 3*CELL_SIZE, 3*CELL_SIZE), THICK_LINE_WIDTH)
            else:
                pygame.draw.rect(window, BLACK, (j*CELL_SIZE+WINDOW_PADDING, i*CELL_SIZE+WINDOW_PADDING, CELL_SIZE, CELL_SIZE), LINE_WIDTH)
            # Dibuja los números en las celdas no vacías del tablero
            if board[i][j] != 0:
                font = pygame.font.SysFont(None, FONT_SIZE)
                number = font.render(str(board[i][j]), True, BLACK)
                window.blit(number, (j*CELL_SIZE+WINDOW_PADDING+20, i*CELL_SIZE+WINDOW_PADDING+10))
    # Resalta la celda seleccionada con un borde rojo
    if selected_cell:
        row, col = selected_cell
        pygame.draw.rect(window, RED, (col*CELL_SIZE+WINDOW_PADDING, row*CELL_SIZE+WINDOW_PADDING, CELL_SIZE, CELL_SIZE), 3)

# Función para resolver el Sudoku utilizando backtracking
def solve_sudoku(board):
    """Resuelve el Sudoku utilizando el algoritmo de backtracking."""
    empty_cell = find_empty_cell(board)  # Encuentra una celda vacía en el tablero
    if not empty_cell:
        return True

    row, col = empty_cell  # Obtiene la posición de la celda vacía

    for num in range(1, 10):
        if is_valid_move(board, num, row, col):  # Verifica si el número es válido para colocar en la celda
            board[row][col] = num  # Coloca el número en la celda

            if solve_sudoku(board):  # Intenta resolver el Sudoku recursivamente
                return True

            board[row][col] = 0  # Si no se puede resolver, retrocede y prueba otro número

    return False

# Función para encontrar una celda vacía
def find_empty_cell(board):
    """Encuentra una celda vacía en el tablero."""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

# Función para verificar si un movimiento es válido
def is_valid_move(board, num, row, col):
    """Verifica si un movimiento es válido en la posición especificada."""
    # Verificar fila y columna
    for i in range(len(board)):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Verificar caja 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

# Función para detectar la celda seleccionada
def get_selected_cell(mouse_pos):
    """Devuelve la fila y columna de la celda seleccionada."""
    col = (mouse_pos[0] - WINDOW_PADDING) // CELL_SIZE
    row = (mouse_pos[1] - WINDOW_PADDING) // CELL_SIZE
    return row, col

# Función principal
def main():
    """Función principal del juego."""

    rows = 9
    cols = 9
       
    board = create_empty_board(rows, cols)  # Crea un tablero de Sudoku vacío con las dimensiones especificadas

    window_width = cols * CELL_SIZE + 2 * WINDOW_PADDING  # Calcula el ancho de la ventana
    window_height = rows * CELL_SIZE + 2 * WINDOW_PADDING  # Calcula la altura de la ventana
    window = pygame.display.set_mode((window_width, window_height))  # Crea una ventana con el tamaño calculado
    pygame.display.set_caption("Sudoku Solver")  # Establece el título de la ventana

    selected_cell = None  # Inicializa la celda seleccionada como vacía
    solve_button_rect = pygame.Rect(50, 20, 100, 40)  # Define un rectángulo para el botón de resolver

    # Ciclo principal del juego
    while True:
        for event in pygame.event.get():  # Itera sobre los eventos pygame
            if event.type == pygame.QUIT:  # Si se cierra la ventana, sale del juego
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Si se presiona el botón del ratón
                mouse_pos = pygame.mouse.get_pos()  # Obtiene la posición del ratón
                if solve_button_rect.collidepoint(mouse_pos):  # Si se hace clic en el botón de resolver
                    solve_sudoku(board)  # Resuelve el Sudoku

                selected_cell = get_selected_cell(mouse_pos)  # Obtiene la celda seleccionada con el ratón

            if event.type == pygame.KEYDOWN:  # Si se presiona una tecla del teclado
                mods = pygame.key.get_mods()  # Obtiene los modificadores de teclado
                if selected_cell and not mods & pygame.KMOD_SHIFT:  # Si hay una celda seleccionada y no se presiona la tecla Shift
                    row, col = selected_cell  # Obtiene la fila y columna de la celda seleccionada
                    if pygame.K_KP1 <= event.key <= pygame.K_KP9:  # Si se presiona una tecla numérica en el teclado numérico
                        num = event.key - pygame.K_KP1 + 1  # Obtiene el número correspondiente
                        board[row][col] = num  # Coloca el número en la celda seleccionada
                    elif pygame.K_1 <= event.key <= pygame.K_9:  # Si se presiona una tecla numérica en la fila superior del teclado
                        num = event.key - pygame.K_1 + 1  # Obtiene el número correspondiente
                        board[row][col] = num  # Coloca el número en la celda seleccionada

        draw_board(board, window, selected_cell)  # Dibuja el tablero en la ventana

        # Dibujar botón de resolver
        pygame.draw.rect(window, BLACK, solve_button_rect)  # Dibuja el botón de resolver
        font = pygame.font.SysFont(None, FONT_SIZE)  # Crea una fuente para el texto del botón
        solve_text = font.render("Solve", True, WHITE)  # Renderiza el texto del botón
        window.blit(solve_text, (solve_button_rect.x + 25, solve_button_rect.y + 10))  # Coloca el texto en el botón

        pygame.display.update()  # Actualiza la ventana con los cambios realizados

# Ejecutar el programa
if __name__ == "__main__":
    main()  # Llama a la función principal del juego