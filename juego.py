import pygame
import os
import random

# Inicialización
pygame.init()
pygame.mixer.init()

# Configuración de pantalla
TAM_CELDA = 48
FILAS, COLUMNAS = 16, 30  # 1920x1024
ANCHO, ALTO = COLUMNAS * TAM_CELDA, FILAS * TAM_CELDA
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🌿 CortaPastito")

# Fuente para mostrar texto
fuente = pygame.font.SysFont("consolas", 24)
tiempo_inicio = pygame.time.get_ticks()

# Música de fondo
pistas = ["musica/musica8bit.ogg", "musica/musica8bit_2.ogg"]
pista_actual = 0
pygame.mixer.music.load(pistas[pista_actual])
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Cargar sprites
def cargar_sprite(nombre):
    ruta = os.path.join("sprites", nombre)
    img = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(img, (TAM_CELDA, TAM_CELDA))

sprite_pasto_alto = cargar_sprite("pasto_alto.png")
sprite_pasto_cortado = cargar_sprite("pasto_cortado.png")
sprite_cortadora = cargar_sprite("cortadora.png")
sprite_piedra = cargar_sprite("piedra.png")

# Crear mapa
jardin = [[1 for _ in range(COLUMNAS)] for _ in range(FILAS)]
cortadora_x, cortadora_y = 0, 0

# Añadir rocas
for _ in range(25):
    while True:
        x, y = random.randint(0, COLUMNAS - 1), random.randint(0, FILAS - 1)
        if jardin[y][x] == 1 and (x, y) != (0, 0):
            jardin[y][x] = 2
            break

# Bucle principal
reloj = pygame.time.Clock()
jugando = True

while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                pista_actual = (pista_actual + 1) % len(pistas)
                pygame.mixer.music.load(pistas[pista_actual])
                pygame.mixer.music.play(-1)

    # Movimiento
    teclas = pygame.key.get_pressed()
    nueva_x, nueva_y = cortadora_x, cortadora_y
    if teclas[pygame.K_LEFT]: nueva_x -= 1
    if teclas[pygame.K_RIGHT]: nueva_x += 1
    if teclas[pygame.K_UP]: nueva_y -= 1
    if teclas[pygame.K_DOWN]: nueva_y += 1

    if 0 <= nueva_x < COLUMNAS and 0 <= nueva_y < FILAS:
        if jardin[nueva_y][nueva_x] != 2:
            cortadora_x, cortadora_y = nueva_x, nueva_y
            jardin[cortadora_y][cortadora_x] = 0

    # Dibujar
    pantalla.fill((30, 30, 30))
    for y in range(FILAS):
        for x in range(COLUMNAS):
            celda = jardin[y][x]
            if celda == 1:
                pantalla.blit(sprite_pasto_alto, (x*TAM_CELDA, y*TAM_CELDA))
            elif celda == 0:
                pantalla.blit(sprite_pasto_cortado, (x*TAM_CELDA, y*TAM_CELDA))
            elif celda == 2:
                pantalla.blit(sprite_piedra, (x*TAM_CELDA, y*TAM_CELDA))

    pantalla.blit(sprite_cortadora, (cortadora_x*TAM_CELDA, cortadora_y*TAM_CELDA))

    # Mostrar progreso y tiempo
    total_celdas = FILAS * COLUMNAS
    celdas_cortadas = sum(row.count(0) for row in jardin)
    porcentaje = int((celdas_cortadas / total_celdas) * 100)
    tiempo_actual = pygame.time.get_ticks()
    segundos = (tiempo_actual - tiempo_inicio) // 1000
    texto = f"Pasto cortado: {porcentaje}%   Tiempo: {segundos}s"
    superficie_texto = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(superficie_texto, (20, 10))

    pygame.display.flip()
    reloj.tick(10)

pygame.quit()
