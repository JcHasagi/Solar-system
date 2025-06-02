import sys
import pygame
import tkinter as tk
from tkinter import filedialog
import random

root = tk.Tk()
root.withdraw()

# Constantes
size = width, height = 1000, 564
black = (0, 0, 0)
white = (255, 255, 255)
planet_color = (200, 120, 50, 255)

class PolvoEstelar:
    def __init__(self):
        self.cols = width // 10
        self.rows = height // 10
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.next_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = 0

    def count_neighbors(self, row, col):
        count = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                r = (row + i) % self.rows
                c = (col + j) % self.cols
                count += 1 if self.grid[r][c] != 0 else 0
        return count

    def update(self):
        for i in range(self.rows):
            for j in range(self.cols):
                state = self.grid[i][j]
                neighbors = self.count_neighbors(i, j)

                if state == 1 and neighbors >= 5:
                    self.next_grid[i][j] = 2  # Se forma planeta

                elif state == 2:
                    if neighbors < 4:
                        self.next_grid[i][j] = 1
                    else:
                        self.next_grid[i][j] = 2

                elif state == 1:
                    if neighbors == 2 or neighbors == 3:
                        self.next_grid[i][j] = 1 if random.random() > 0.02 else 0
                    else:
                        self.next_grid[i][j] = 0
                else:
                    if neighbors == 3:
                        self.next_grid[i][j] = 1
                    else:
                        self.next_grid[i][j] = 1 if random.random() < 0.001 else 0

        self.grid, self.next_grid = self.next_grid, self.grid

    def draw(self, screen):
        for i in range(self.rows):
            for j in range(self.cols):
                state = self.grid[i][j]
                if state == 1:
                    neighbors = self.count_neighbors(i,j)
                    alpha = min(255, int((0.1 + neighbors*0.15)*255))
                    r = min(255, 180 + neighbors*10)
                    g = max(0, 180 - neighbors*60)
                    b = min(255, 220 + neighbors*15)
                    color = (r, g, b, alpha)
                    s = pygame.Surface((10,10), pygame.SRCALPHA)
                    s.fill(color)
                    screen.blit(s, (j*10, i*10))
                elif state == 2:
                    s = pygame.Surface((10,10), pygame.SRCALPHA)
                    s.fill(planet_color)
                    screen.blit(s, (j*10, i*10))

def mouse_click(world: PolvoEstelar, mouse_x: int, mouse_y: int) -> None:
    x = int(mouse_x / 10)
    y = int(mouse_y / 10)
    if 0 <= x < world.cols and 0 <= y < world.rows:
        if world.grid[y][x] == 1 or world.grid[y][x] == 2:
            world.grid[y][x] = 0
        else:
            world.grid[y][x] = 1

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Simulación de Polvo Estelar y Planeta")

    clock = pygame.time.Clock()
    running = False
    world = PolvoEstelar()
    iterations = 0

    font = pygame.font.SysFont('Consolas', 24)
    info_text = font.render("Click para poner/quitar polvo. ESPACIO iniciar/pausar. R reiniciar.", True, white)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("End.")
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not running:
                x, y = pygame.mouse.get_pos()
                mouse_click(world, x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                elif event.key == pygame.K_r:
                    running = False
                    world.reset()
                    iterations = 0

        if running:
            world.update()
            iterations += 1

        screen.fill(black)
        world.draw(screen)
        screen.blit(info_text, (10, height - 30))

        status = "CORRIENDO" if running else "PAUSA - Editando"
        status_text = font.render(f"Estado: {status}", True, white)
        screen.blit(status_text, (width - 260, height - 30))

        iterations_text = font.render(f"Iteraciones: {iterations}", True, white)
        screen.blit(iterations_text, (width - 220, 10))

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()
