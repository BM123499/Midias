import cv2 as cv
import numpy as np
import Homografy

# Cria as listas de Xi' e Xi
global lista_destino
lista_destino = []
global lista_origem
lista_origem = []


def click_event(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        global lista_destino
        # Guarda o ponto Xi' na lista de destinos
        lista_destino.append((y, x))
        # Desenha um circulo em cima do pixel selecionado
        cv.circle(image, (x, y), 1, (0, 0, 255), 2)

# Lê a imagem de calibração
image_origem = cv.imread("img2.png", 1)

# Gera lista com (x, y, cor) de cada pixel
lista_cores = [(x, y, image_origem[x, y]) for x in range(image_origem.shape[0])
                       for y in range(image_origem.shape[1])
                       if image_origem[x, y, 0] != 255 or image_origem[x, y, 1] != 255 or image_origem[x, y, 2] != 255]

# Itera pela matriz de calibração a fim de encontrar os pontos de origem (quinas)
for i in range(4):
    for cores in lista_cores:
        if i == 0 and not any(cores[2]):
            lista_origem.append((cores[0], cores[1]))
        if i == 1 and cores[2][0] == 255:
            lista_origem.append((cores[0], cores[1]))
        if i == 2 and cores[2][1] == 255:
            lista_origem.append((cores[0], cores[1]))
        if i == 3 and cores[2][2] == 255:
            lista_origem.append((cores[0], cores[1]))


# Lê a imagem distorcida
image = cv.imread("img.png", 1)

# Guarda as dimensões da imagem
dimensions = image.shape

# Copia a imagem distoricida
image2 = image.copy()

# Mostra a tela pós seleção de cada ponto Xi'
while len(lista_destino) < 4:
    cv.imshow("tela", image)
    cv.setMouseCallback('tela', click_event)
    cv.waitKey(1)
cv.imshow("tela", image)
cv.waitKey(1000)

# Cria a matriz da homografia 2d (Xi' -> Xi)
H = Homografy.homografy(lista_destino, lista_origem)

# Cria a Homografia inversa (Xi -> Xi')
H2 = Homografy.homografy(lista_origem, lista_destino)

# Calculando a bounding box
min_x = 1281
min_y = 1281
max_x = 0
max_y = 0
for i in range(4):
    # Para cada quina da imagem original
    p = lista_origem[i]
    # descobre o correspondente na imagem final
    pixel_alvo = np.matmul(H2, np.array([[p[0]], [p[1]], [1]]))
    pixel_alvo = np.divide(pixel_alvo, pixel_alvo[2][0])

    # Armazena o (x,y)  do ponto correspondente
    x = round(pixel_alvo[0][0])
    y = round(pixel_alvo[1][0])

    # Atualiza a bounding box
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    max_x = max(max_x, x)
    max_y = max(max_y, y)

# Deixa a tela branca
image[:, :] = [255, 255, 255]
# Para cada pixel dentro da bounding box
for i in range(min_x, max_x+1):
    for j in range(min_y, max_y+1):
        # Encontra ponto na imagem original
        pixel_alvo = np.matmul(H, np.array([[i], [j], [1]]))
        pixel_alvo = np.divide(pixel_alvo, pixel_alvo[2][0])
        # Armazena o (x,y)
        x = round(pixel_alvo[0][0])
        y = round(pixel_alvo[1][0])
        # Verifica se está na imagem
        if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]:
            image[i, j] = image2[x, y]

# Mostra o resultado
cv.imshow("tela", image)
cv.waitKey(0)
