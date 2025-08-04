import pygame
import random

# Inicializa Pygame
pygame.init()

# Configura la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Configura la fuente para las letras
fuente = pygame.font.SysFont("Arial", 30)

# Configura la velocidad de las letras
velocidad_letras = 2

# Configura la probabilidad de que salga una letra
probabilidad_letra = 0.05

# Configura la lista de letras que pueden salir
letras_posibles = "abcdefghijklmnopqrstuvwxyz"

# Inicializa la lista de letras en pantalla
letras_en_pantalla = []

# Bucle principal
while True:
    # Maneja los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Agrega letras nuevas a la pantalla
    if random.random() < probabilidad_letra:
        letra = random.choice(letras_posibles)
        x = random.randint(0, pantalla.get_width() - 20)
        y = random.randint(0, pantalla.get_height() - 20)
        letras_en_pantalla.append((letra, x, y))

    # Mueve las letras en pantalla
    for i, (letra, x, y) in enumerate(letras_en_pantalla):
        y += velocidad_letras
        if y > pantalla.get_height():
            del letras_en_pantalla[i]
        else:
            letras_en_pantalla[i] = (letra, x, y)

    # Dibuja las letras en pantalla
    pantalla.fill((255, 255, 255))
    for letra, x, y in letras_en_pantalla:
        texto = fuente.render(letra, True, (0, 0, 0))
        pantalla.blit(texto, (x, y))

    # Actualiza la pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)