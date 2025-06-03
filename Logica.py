import pygame

class ConWay:
    width = 100     # ancho en celdas
    height = 50     # alto de las celdas 
    live = 1    # celda viva
    dead = 0    # celda muerta

    __world = []     #lista de los valores de las celdas
    __next = []     #lista de respaldo

    __born = []     #numero de celdas vecinas activas para que una celda se active     
    __alive = []     #numero de celdas vecinas activas para que una celda se mantenga activa    

    __iterations = 0     #contador de iteraciones

    #logica de 23/3

    def __init__(self, pattern:str = "23/3"):
        #Constructor
        self.reset()
        self.__alive = [int(v) for v in pattern.split("/") [0]]
        self.__born = [int(v) for v in pattern.split("/") [1]]

    @property
    def iterations(self) -> int:
        #Devuelve el numero de iteraciones
        return self.__iterations
    
    @property
    def livecells(self) -> int:
        #Devuelve el numero de celdas activas presentes
        return self.__world.count(1)

    def reset(self):
        #Reinicia por completo el programa
        self.__iterations = 0
        self.__world = [0] * (self.width * self.height)
        self.__next = [0] * (self.width * self.height)

    def read(self, x: int, y:int) -> int:
        #Devolver el estado de una celda segun sus cordenadas con una frontera "reflectora"
        #param x: coordenadas x
        #param y: coordenadas y
        #return: Valor de la celda (0) INACTIVA - (1) ACTIVA
        if x >= self.width:
            x -= self.width
        elif x < 0:
            x += self.width
        if y >= self.height:
            y -= self.height
        elif y < 0:
            y += self.height
        return self.__world[(y * self.width) + x]
    
    def write(self, x: int, y: int, value: int) -> None:
        #Establecer el valor de las celdas dadas sus coordenadas
        #param x: coordenadas x
        #param y: coordenadas y
        #return: Valor de la celda (0) INACTIVA - (1) ACTIVA
        self.__world[(y * self.width) + x] = value

    def update(self) -> None:

        #Actualizacion el estado del automata celular 

        self.__iterations += 1
        # Bucle de recorrido de todas las celdas
        for y in range(self.height):
            for x in range(self.width):
                near = [self.read(x + 1, y - 1),    # Obtencion de la lista con celdas vecinas.
                        self.read(x, y - 1),
                        self.read(x - 1, y - 1),
                        self.read(x + 1, y),
                        self.read(x - 1, y),
                        self.read(x - 1, y + 1),
                        self.read(x, y + 1),
                        self.read(x + 1, y + 1)]
                alive_count = near.count(self.live)     # Obtencion de celdas vivas vecinas.
                current = self.read(x, y)
                if current == self.live:                    # Para una celda viva
                    if alive_count not in self.__alive:     # Si el numero de celdas activas corresponde   
                        current = self.dead                 # celda se muere
                else:                                       # Para una celda inactiva
                    if alive_count in self.__born:          # Si el numero de celdas activas coincida
                        current = self.live                 # celda se activa

                self.__next[(y * self.width) + x] = current     #Actualizacion en espacio de respaldo

        for i in range(self.width * self.height) :
            self.__world[i] = self.__next[i]

    def draw(self, context: pygame.Surface) -> None:

        #Funcion de proyeccion del espacio con el estado de las celdas del automata celular
        #param context: contexto grafico de la pantalla
        
        for y in range(self.height) : 
            for x in range(self.width) :
                current = self.read(x, y)
                if current == self.live:
                    # Si la celda esta activa se muestra un cuadro relleno de color blanco
                    pygame.draw.rect(surface= context, color= (255,255,255), 
                                     rect= (x * 10, y * 10, 10, 10))
                else:
                    # Si la celda esta inactiva se muestra un recuadro sin relleno con bordes grises
                    pygame.draw.lines(surface= context, color= (64,64,64), closed = True, points=(
                        (x * 10, y * 10),
                        ((x + 1) * 10, y * 10),
                        ((x + 1) * 10, (y + 1) * 10),
                        (x * 10, (y + 1) * 10)), width=1)
                    
    def save(self, filename:str) -> None:
        with open(filename, mode="w", encoding="utf-8") as fp:
            fp.write(str(self.__world))


    def load(self, filename:str) -> None:
        with open(filename, mode="r", encoding="utf-8") as fp:
            data = fp.read()[1:-1]
            self.__world = [int(v) for v in data.split(",")]




        