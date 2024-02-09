import pygame
import pygame_gui
import sys
import random
import copy
import funciones as gen
import matplotlib.pyplot as plt

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)

def draw_grid(screen, grid_rect):
    for i in range(grid_rect.left, grid_rect.right, grid_rect.width // 9):
        pygame.draw.line(screen, BLACK, (i, grid_rect.top), (i, grid_rect.bottom), 2)
        pygame.draw.line(screen, BLACK, (grid_rect.left, i), (grid_rect.right, i), 2)


def draw_sudoku(screen, sudoku_board, grid_rect):
    font = pygame.font.Font(None, 36)
    for i, row in enumerate(sudoku_board):
        for j, value in enumerate(row):
            if value != 0:
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(
                    center=(
                        grid_rect.left
                        + j * (grid_rect.width // 9)
                        + (grid_rect.width // 9) // 2,
                        grid_rect.top
                        + i * (grid_rect.height // 9)
                        + (grid_rect.height // 9) // 2,
                    )
                )
                screen.blit(text, text_rect)

# Función para validar que la entrada sea un número decimal en el rango [0, 1]
def is_valid_input(input_text):
    try:
        value = float(input_text)
        return 0 <= value <= 1
    except ValueError:
        return False

def main_interfaz():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Solver")

    clock = pygame.time.Clock()

    sudoku_board = gen.generar_sudoku(0)  # Porcentaje según tu preferencia

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    
    # Definir rectángulos para secciones de la pantalla
    grid_rect = pygame.Rect(50, 50, 500, 500)
    menu_rect = pygame.Rect(580, 50, 200, 500)

    # Agregar botones y controles
    resolver_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((menu_rect.left + 25, menu_rect.bottom - 90), (150, 40)),
        text='Resolver', manager=manager
    )
    
    # Agregar cuadros de entrada para configuración
    pc1_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_rect.left + 25, menu_rect.top + 15), (150, 30)),
        text='PC1:', manager=manager,
    )

    pc1_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((menu_rect.left + 60, menu_rect.top + 40), (100, 30)),
        manager=manager,
    )
    
    # Agregar cuadros de entrada para configuración
    pc2_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_rect.left + 25, menu_rect.top + 65), (150, 30)),
        text='PC2:', manager=manager,
    )

    pc2_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((menu_rect.left + 60, menu_rect.top + 90), (100, 30)),
        manager=manager,
    )
    
    # Agregar cuadros de entrada para configuración
    pm1_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_rect.left + 25, menu_rect.top + 115), (150, 30)),
        text='PM1:', manager=manager,
    )

    pm1_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((menu_rect.left + 60, menu_rect.top + 140), (100, 30)),
        manager=manager,
    )
    
    # Agregar cuadros de entrada para configuración
    pm2_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_rect.left + 25, menu_rect.top + 165), (150, 30)),
        text='PM2:', manager=manager,
    )

    pm2_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((menu_rect.left + 60, menu_rect.top + 190), (100, 30)),
        manager=manager,
    )
    
    
    # Agregar cuadros de entrada para configuración
    poblacion_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_rect.left + 25, menu_rect.top + 215), (150, 30)),
        text='Población:', manager=manager,
    )

    poblacion_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((menu_rect.left + 60, menu_rect.top + 240), (100, 30)),
        manager=manager,
    )
    
    # Agregar cuadros de entrada para configuración
    generaciones_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_rect.left + 25, menu_rect.top + 265), (150, 30)),
        text='Generaciones:', manager=manager,
    )

    generaciones_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((menu_rect.left + 60, menu_rect.top + 290), (100, 30)),
        manager=manager,
    )

    # Establecer el valor predeterminado después de crear el cuadro de entrada
    pc1_input.set_text('0.2')  # Valor por defecto

    pc1_input.valid_input_characters = '0123456789.'  # Permitir números y punto decimal
    pc1_input.input_validator = is_valid_input
    
    pc2_input.set_text('0.1')  # Valor por defecto

    pc2_input.valid_input_characters = '0123456789.'  # Permitir números y punto decimal
    pc2_input.input_validator = is_valid_input
    
    pm1_input.set_text('0.3')  # Valor por defecto

    pm1_input.valid_input_characters = '0123456789.'  # Permitir números y punto decimal
    pm1_input.input_validator = is_valid_input
    
    pm2_input.set_text('0.05')  # Valor por defecto

    pm2_input.valid_input_characters = '0123456789.'  # Permitir números y punto decimal
    pm2_input.input_validator = is_valid_input

    poblacion_input.set_text('150')  # Valor por defecto

    poblacion_input.valid_input_characters = '0123456789'  # Permitir números y punto decimal
    
    generaciones_input.set_text('1000')  # Valor por defecto

    generaciones_input.valid_input_characters = '0123456789'  # Permitir números y punto decimal

    # Agregar botones para elegir la dificultad
    easy_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 10), (80, 30)),
        text='Fácil', manager=manager
    )

    normal_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((150, 10), (80, 30)),
        text='Normal', manager=manager
    )

    hard_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((250, 10), (80, 30)),
        text='Difícil', manager=manager
    )

    expert_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 10), (85, 30)),
        text='Experto', manager=manager
    )

    impossible_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((450, 10), (100, 30)),
        text='Imposible', manager=manager
    )

    while True:
        
        # Dentro de tu bucle principal
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == resolver_button:
                        # Obtener el valor del cuadro de entrada
                        pc1_value = float(pc1_input.get_text())
                        pc2_value = float(pc2_input.get_text())
                        pm1_value = float(pm1_input.get_text())
                        pm2_value = float(pm2_input.get_text())
                        poblacion_value = int(poblacion_input.get_text())
                        generaciones_value = int(generaciones_input.get_text())
                        
                        sudoku_original = sudoku_board
                        mejor = []
                        peor = []
                        i = 0
                        while True:
                            i += 1
    
                            if i == 0:
                                flag = 0
                            else:
                                flag = 1
                                

                            x, nobest = gen.main(pc1_value, pc2_value, pm1_value, pm2_value, poblacion_value, 1, sudoku_board, sudoku_original, flag)  # Ejecutar solo 1 generación
                            
                            # Limpiar el tablero antes de mostrar cada nuevo estado
                            screen.fill(WHITE)
                            pygame.draw.rect(screen, GRAY, menu_rect)
                            manager.draw_ui(screen)
                            draw_grid(screen, grid_rect)

                            if (i % 100 == 0 and i!= 0) or gen.fitness_function(x) == 0:  # Mostrar el estado del Sudoku cada 50 generaciones
                                print("Estado del Sudoku en generación", i)
                                gen.print_sudoku(x)
                                print(f"la aptitud es: {gen.fitness_function(x)}")
                                # Actualizar el estado del Sudoku en la interfaz
                                draw_sudoku(screen, sudoku_board, grid_rect)
                                pygame.display.flip()
                                pygame.time.wait(1000)  # Pausa de 1 segundo para visualizar el estado
                                
                                eje_x = list(range(1, len(mejor) + 1))
                            
                                # Graficar los dos arreglos
                                plt.plot(eje_x, mejor, label='mejor')
                                plt.plot(eje_x, peor, label='peor')
                                
                                # Agregar etiquetas y título
                                plt.xlabel('Posición')
                                plt.ylabel('Valor')
                                plt.title('Gráfico de dos arreglos')

                                # Agregar leyenda
                                plt.legend()

                                # Mostrar el gráfico
                                plt.show()

                            mejor.append(gen.fitness_function(x))
                            peor.append(gen.fitness_function(nobest))
                            
                            sudoku_board = x
                            
                    # Agregar lógica para cambiar el porcentaje según la dificultad
                    elif event.ui_element == easy_button:
                        sudoku_board = gen.generar_sudoku(80)  # Porcentaje para Fácil
                    elif event.ui_element == normal_button:
                        sudoku_board = gen.generar_sudoku(60)  # Porcentaje para Normal
                    elif event.ui_element == hard_button:
                        sudoku_board = gen.generar_sudoku(40)  # Porcentaje para Difícil
                    elif event.ui_element == expert_button:
                        sudoku_board = gen.generar_sudoku(20)  # Porcentaje para Experto
                    elif event.ui_element == impossible_button:
                        sudoku_board = gen.generar_sudoku(10)  # Porcentaje para Imposible

            manager.process_events(event)

        screen.fill(WHITE)
        draw_grid(screen, grid_rect)
        draw_sudoku(screen, sudoku_board, grid_rect)

        pygame.draw.rect(screen, GRAY, menu_rect)
        manager.update(30)
        manager.draw_ui(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main_interfaz()
