import sys, pygame

size = width, height = 1000, 564

BLACK = (0,0,0)

def main():
  # instancias
  pygame.init()
  #Crear pantalla
  screen = pygame.display.set_mode(size)
  pygame.display.set_caption("JUEGO DE LA VIDA DE CONWAY'S")

  while 1:
    # eventos a comprobar
    for event in pygame.event.get(): 
      if event.type == pygame.QUIT:     #cuando se cierre la ventana
        print("End.")
        sys.exit()
    #reiniciar juego
    screen.fill(BLACK)             # Color de fondo
    pygame.display.flip()          # Refrescar pantalla

if __name__ == "__main__":
  main()
  