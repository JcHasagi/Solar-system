import sys, pygame
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # oculta la ventana principal de Tkinter
# para mostrar los cuadros de dialogo de carga y guardado de archivo

from Logica import ConWay

#Constantes
size = width, height = 1000, 564  # Ancho y alto de la ventana
black = (0, 0, 0)  # Colores formato RGB (0 a 255, 0 a 225, 9 a 255)
white = (255, 255, 255)
gray = (92, 92, 92)


def mouse_click(world: ConWay, mouse_x: int, mouse_y: int) -> None:
    #funcion que captura el raton
    #param world: instancia del automata celular
    #param mouse_x: coordenadas X en pixeles del cursor del raton al hacer click
    #param mouse_y: coordenadas Y en pixeles del cursor del raton al hacer click

    x = int(mouse_x / 10)
    y = int(mouse_y / 10)
    if world.read(x, y) == world.live: # Si la celda esta activa
        world.write(x, y, world.dead)  # Se desactiva
    else: # Si la celda esta inactiva
        world.write(x, y, world.live) # Se activa

def main():
    # Instancias
    pygame.init()
    pygame.font.init()
    world = ConWay()
    # Creacion de ventana principal:

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("JUEGO DE LA VIDA DE CONWAY'S")
    
    # Control de velocidad de iteraciones
    clock = pygame.time.Clock()

    # Cargar imagenes PNG para iconos
    play = pygame.image.load("play.png")
    playrect = play.get_rect()
    playrect = playrect.move(404, 500)
    pause = pygame.image.load("pause.png")
    pauserect = pause.get_rect()
    pauserect = pauserect.move(468, 500)
    clear = pygame.image.load("clear.png")
    clearrect = clear.get_rect()
    clearrect = clearrect.move(532, 500)
    load = pygame.image.load("load.png")
    loadrect = load.get_rect()
    loadrect = loadrect.move(596, 500)
    save = pygame.image.load("save.png")
    saverect = save.get_rect()
    saverect = saverect.move(660, 500)
    # Carga de fuente para textos
    myfont = pygame.font.SysFont('Lucida Console', 30)

    # Estado del AC -> Parado
    running = False

    # Bucle principal
    while 1:
        # Captura de eventos.
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:                  # Evento de cierre de ventana
                print("End.")
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:       # Pulsaciones de raton
                x, y = pygame.mouse.get_pos()
                if y <= 500:
                    mouse_click(world, x,y)
                else:
                    if playrect.collidepoint(x,y):         # Pulsaciones de icono INICIO
                        running = True 
                    if pauserect.collidepoint(x,y):        # Pulsacion de icono PAUSA
                        running = False
                    if clearrect.collidepoint(x,y):        # Pulsacion de icono LIMPIAR
                        world.reset()
                    if loadrect.collidepoint(x, y):        # Pulsacion de icono CARGAR
                        file_path_string = filedialog.askopenfilename(filetypes=(
                            ("Conway Gol FIles", "*.cgl"),
                            ("All files", "*.*")
                        ))
                        if file_path_string != "":
                            world.load(file_path_string)
                    if saverect.collidepoint(x, y):         # Pulsacion de icono GUARDAR
                        file_path_string = filedialog.asksaveasfilename(
                            filetypes=(
                            ("Conway Gol Files", "*.cgl"),
                            ("All files", "*.*")
                            )
                        )
                        if file_path_string != "":
                            world.save(file_path_string)

        # Actualizacion del AC
        if running:
            world.update()

        # Refresco de pantalla
        screen.fill(black)
        world.draw(screen)      # Repintado celdas del AC
        screen.blit(play, playrect)     # Repitando iconos de control
        screen.blit(pause, pauserect)
        screen.blit(clear, clearrect)
        screen.blit(load, loadrect)
        screen.blit(save, saverect)

        textsurface = myfont.render("RUNNING" if running else "PAUSE", True, white)
        screen.blit(textsurface, (100,516))      # Texto de estado
        screen.blit(
            myfont.render(str(world.iterations), True, white), (750, 516))      # Texto de numero de iteraciones
        screen.blit(
            myfont.render(str(world.livecells), True, white), (850, 516))      # Texto de numero de celdas activas
        pygame.display.flip()   # Refresco de pantalla
        clock.tick(5)  # Limita a 5 FPS

if __name__ == "__main__": 
    main()