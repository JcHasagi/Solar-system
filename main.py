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

    play_img = pygame.image.load("play.png")
    pause_img = pygame.image.load("pause.png")
    save_img = pygame.image.load("save.png")
    load_img = pygame.image.load("load.png")
    clear_img = pygame.image.load("clear.png")

    button_size = 50
    button_spacing = 20
    total_width = 5 * button_size + 4 * button_spacing
    start_x = (width - total_width) // 2
    y_pos = height - button_size - 10

    button_rects = {
        "play": pygame.Rect(start_x + 0 * (button_size + button_spacing), y_pos, button_size, button_size),
        "pause": pygame.Rect(start_x + 1 * (button_size + button_spacing), y_pos, button_size, button_size),
        "save": pygame.Rect(start_x + 2 * (button_size + button_spacing), y_pos, button_size, button_size),
        "load": pygame.Rect(start_x + 3 * (button_size + button_spacing), y_pos, button_size, button_size),
        "clear": pygame.Rect(start_x + 4 * (button_size + button_spacing), y_pos, button_size, button_size),
    }

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Simulación de Polvo Estelar y Planeta")

    clock = pygame.time.Clock()
    paused = True
    world = PolvoEstelar()
    iterations = 0

    font = pygame.font.SysFont('Consolas', 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("End.")
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if button_rects["play"].collidepoint(mx, my):
                    paused = False
                elif button_rects["pause"].collidepoint(mx, my):
                    paused = True
                elif button_rects["save"].collidepoint(mx, my):
                    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
                    if file_path:
                        with open(file_path, 'w') as f:
                            for row in world.grid:
                                f.write(' '.join(str(cell) for cell in row) + '\n')
                elif button_rects["load"].collidepoint(mx, my):
                    file_path = filedialog.askopenfilename()
                    if file_path:
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                            for i, line in enumerate(lines):
                                row = list(map(int, line.strip().split()))
                                world.grid[i] = row
                elif button_rects["clear"].collidepoint(mx, my):
                    world.reset()
                else:
                    mouse_click(world, mx, my)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    paused = True
                    world.reset()
                    iterations = 0

        if not paused:
            world.update()
            iterations += 1

        screen.fill(black)
        world.draw(screen)

        status = "CORRIENDO" if not paused else "PAUSA - Editando"
        status_text = font.render(f"Estado: {status}", True, white)
        screen.blit(status_text, (10, 10))

        iterations_text = font.render(f"Iteraciones: {iterations}", True, white)
        screen.blit(iterations_text, (10, 40))

        screen.blit(play_img, button_rects["play"].topleft)
        screen.blit(pause_img, button_rects["pause"].topleft)
        screen.blit(save_img, button_rects["save"].topleft)
        screen.blit(load_img, button_rects["load"].topleft)
        screen.blit(clear_img, button_rects["clear"].topleft)

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()
