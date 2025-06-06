import sys
import pygame
import tkinter as tk
from tkinter import filedialog
import random

root = tk.Tk()
root.withdraw()

width, height = 1920, 1080
size = (width, height)

black = (0, 0, 0)
white = (255, 255, 255)

planet_color = (200, 120, 50, 255)
star_color_base = (255, 255, 100, 255)
comet_color = (255, 255, 255, 200)

VACIO = 0
POLVO = 1
PLANETA = 2
ESTRELLA = 3
COMETA = 4

cell_size = 10
cols = width // cell_size
rows = height // cell_size

class Universo:
    def __init__(self):
        self.grid = [[VACIO for _ in range(cols)] for _ in range(rows)]
        self.next_grid = [[VACIO for _ in range(cols)] for _ in range(rows)]
        self.cometas = []

    def reset(self):
        self.grid = [[VACIO for _ in range(cols)] for _ in range(rows)]
        self.cometas = []

    def count_neighbors(self, row, col, tipo=None):
        count = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                r = (row + i) % rows
                c = (col + j) % cols
                if tipo is None:
                    if self.grid[r][c] != VACIO:
                        count += 1
                else:
                    if self.grid[r][c] == tipo:
                        count += 1
        return count

    def update(self):
        for i in range(rows):
            for j in range(cols):
                estado = self.grid[i][j]
                vecinos_totales = self.count_neighbors(i, j)
                vecinos_polvo = self.count_neighbors(i, j, POLVO)
                vecinos_planeta = self.count_neighbors(i, j, PLANETA)
                vecinos_estrella = self.count_neighbors(i, j, ESTRELLA)

                if estado == POLVO:
                    if vecinos_polvo >= 5 and random.random() < 0.08:
                        self.next_grid[i][j] = PLANETA
                    elif vecinos_totales == 2 or vecinos_totales == 3:
                        self.next_grid[i][j] = POLVO if random.random() > 0.01 else VACIO
                    else:
                        self.next_grid[i][j] = VACIO

                elif estado == PLANETA:
                    if vecinos_planeta >= 4:
                        self.next_grid[i][j] = ESTRELLA
                    elif vecinos_planeta >= 2 or vecinos_polvo >= 3:
                        self.next_grid[i][j] = PLANETA
                    elif random.random() < 0.03:
                        self.next_grid[i][j] = POLVO
                    else:
                        self.next_grid[i][j] = VACIO

                elif estado == ESTRELLA:
                    if vecinos_totales >= 2:
                        self.next_grid[i][j] = ESTRELLA
                    else:
                        self.next_grid[i][j] = PLANETA

                elif estado == COMETA:
                    self.next_grid[i][j] = VACIO

                else:
                    if vecinos_totales == 3:
                        self.next_grid[i][j] = POLVO
                    else:
                        self.next_grid[i][j] = POLVO if random.random() < 0.001 else VACIO

        self.grid, self.next_grid = self.next_grid, self.grid
        self.mover_cometas()

    def mover_cometas(self):
        nuevos_cometas = []
        for x, y in self.cometas:
            self.grid[y][x] = VACIO
            if y > 0:
                y -= 1
            x = (x + 1) % cols
            if self.grid[y][x] != ESTRELLA:
                self.grid[y][x] = COMETA
                nuevos_cometas.append((x, y))
        self.cometas = nuevos_cometas

    def crear_cometa(self, x, y):
        if 0 <= x < cols and 0 <= y < rows:
            self.grid[y][x] = COMETA
            self.cometas.append((x, y))

    def toggle_cell(self, x, y, modo='polvo'):
        if 0 <= x < cols and 0 <= y < rows:
            if modo == 'estrella':
                self.grid[y][x] = ESTRELLA
            elif modo == 'cometa':
                self.crear_cometa(x, y)
            elif modo == 'planeta':
                self.grid[y][x] = PLANETA
            else:
                actual = self.grid[y][x]
                self.grid[y][x] = VACIO if actual == POLVO else POLVO

    def draw(self, screen):
        for i in range(rows):
            for j in range(cols):
                estado = self.grid[i][j]
                if estado == POLVO:
                    vecinos = self.count_neighbors(i, j)
                    alpha = min(255, int((0.1 + vecinos*0.15)*255))
                    r = min(255, 180 + vecinos*10)
                    g = max(0, 180 - vecinos*60)
                    b = min(255, 220 + vecinos*15)
                    flicker = random.randint(-20, 20)
                    r = max(0, min(255, r + flicker))
                    g = max(0, min(255, g + flicker))
                    b = max(0, min(255, b + flicker))
                    color = (r, g, b, alpha)
                    s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    s.fill(color)
                    screen.blit(s, (j*cell_size, i*cell_size))

                elif estado == PLANETA:
                    s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    s.fill(planet_color)
                    screen.blit(s, (j*cell_size, i*cell_size))

                elif estado == ESTRELLA:
                    flicker = random.randint(-20, 20)
                    r = min(255, max(200, 255 + flicker))
                    g = min(255, max(200, 255 + flicker))
                    b = min(255, max(150, 200 + flicker))
                    s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    s.fill((r, g, b, 255))
                    screen.blit(s, (j*cell_size, i*cell_size))

                elif estado == COMETA:
                    s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    s.fill(comet_color)
                    screen.blit(s, (j*cell_size, i*cell_size))

def mouse_click(universo: Universo, mouse_x: int, mouse_y: int, modo: str) -> None:
    x = int(mouse_x / cell_size)
    y = int(mouse_y / cell_size)
    universo.toggle_cell(x, y, modo)

def main():
    pygame.init()
    pygame.font.init()

    play_img = pygame.image.load("play.png")
    pause_img = pygame.image.load("pause.png")
    save_img = pygame.image.load("save.png")
    load_img = pygame.image.load("load.png")
    clear_img = pygame.image.load("clear.png")
    star_img = pygame.image.load("star.png")
    comet_img = pygame.image.load("comet.png")
    polvo_img = pygame.image.load("dust.png")
    planeta_img = pygame.image.load("planet.png")

    button_size = 50
    button_spacing = 15
    buttons = ["play", "pause", "save", "load", "clear", "polvo", "estrella", "cometa", "planeta"]
    total_width = len(buttons) * button_size + (len(buttons) - 1) * button_spacing
    start_x = (width - total_width) // 2
    y_pos = height - button_size - 10

    button_rects = {}
    for i, b in enumerate(buttons):
        button_rects[b] = pygame.Rect(start_x + i*(button_size + button_spacing), y_pos, button_size, button_size)

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption("Simulación de Sistemas Solares - Polvo, Planetas, Estrellas y Cometas")

    clock = pygame.time.Clock()
    paused = True
    universo = Universo()
    iterations = 0
    modo_actual = 'polvo'

    font = pygame.font.SysFont('Consolas', 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("End.")
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                clicked_on_button = False
                for key, rect in button_rects.items():
                    if rect.collidepoint(mx, my):
                        clicked_on_button = True
                        if key == "play":
                            paused = False
                        elif key == "pause":
                            paused = True
                        elif key == "save":
                            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
                            if file_path:
                                with open(file_path, 'w') as f:
                                    for row in universo.grid:
                                        f.write(' '.join(str(cell) for cell in row) + '\n')
                        elif key == "load":
                            file_path = filedialog.askopenfilename()
                            if file_path:
                                with open(file_path, 'r') as f:
                                    lines = f.readlines()
                                    for i, line in enumerate(lines):
                                        row = list(map(int, line.strip().split()))
                                        if i < rows:
                                            universo.grid[i] = row
                        elif key == "clear":
                            universo.reset()
                            iterations = 0
                        elif key == "polvo":
                            modo_actual = 'polvo'
                        elif key == "estrella":
                            modo_actual = 'estrella'
                        elif key == "cometa":
                            modo_actual = 'cometa'
                        elif key == "planeta":
                            modo_actual = 'planeta'
                        break

                if not clicked_on_button:
                    mouse_click(universo, mx, my, modo_actual)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    paused = True
                    universo.reset()
                    iterations = 0
                elif event.key == pygame.K_1:
                    modo_actual = 'polvo'
                elif event.key == pygame.K_2:
                    modo_actual = 'estrella'
                elif event.key == pygame.K_3:
                    modo_actual = 'cometa'
                elif event.key == pygame.K_4:
                    modo_actual = 'planeta'

        if not paused:
            universo.update()
            iterations += 1

        screen.fill(black)
        universo.draw(screen)

        status = "CORRIENDO" if not paused else "PAUSA - Editando"
        status_text = font.render(f"Estado: {status}", True, white)
        screen.blit(status_text, (10, 10))

        iterations_text = font.render(f"Iteraciones: {iterations}", True, white)
        screen.blit(iterations_text, (10, 40))

        modo_text = font.render(f"Modo actual: {modo_actual.upper()} (1-polvo, 2-estrella, 3-cometa, 4-planeta)", True, white)
        screen.blit(modo_text, (10, 70))

        screen.blit(play_img, button_rects["play"].topleft)
        screen.blit(pause_img, button_rects["pause"].topleft)
        screen.blit(save_img, button_rects["save"].topleft)
        screen.blit(load_img, button_rects["load"].topleft)
        screen.blit(clear_img, button_rects["clear"].topleft)
        screen.blit(polvo_img, button_rects["polvo"].topleft)
        screen.blit(star_img, button_rects["estrella"].topleft)
        screen.blit(comet_img, button_rects["cometa"].topleft)
        screen.blit(planeta_img, button_rects["planeta"].topleft)

        pygame.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    main()
