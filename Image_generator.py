import cv2 as cv
import numpy as np
import Homografy

# Gerador de deformação

# Criando lsita de pontos Xi'
global lista_destino
lista_destino = []


# Detectar click
def click_event(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        global lista_destino
        # Guarda o ponto Xi' na lista de destinos
        lista_destino.append((y, x))
        # Desenha um circulo em cima do pixel selecionado
        cv.circle(image, (x, y), 1, (255, 0, 0), 2)


# Cria imagem 1280X720 branca
image = np.zeros((720, 1280, 3), np.uint8)
image[:, :, 0] = 255
image[:, :, 1] = 255
image[:, :, 2] = 255
# Cria copia da imagem
image2 = image.copy()

# Cria a tela
cv.namedWindow("tela", 0)

# Mostra a tela pós seleção de cada ponto Xi'
while len(lista_destino) < 4:
    cv.imshow("tela", image)
    cv.setMouseCallback('tela', click_event)
    cv.waitKey(1)
cv.imshow("tela", image)
cv.waitKey(1000)

# Lê a imagem a ser distorcida
xi = cv.imread("teste_IF-760.jpeg", 1)

# Guarda as dimensões da imagem
dimensions = xi.shape

# Guarda os pontos Xi (As quinas da imagem)
lista_origem = [[0, 0], [0, dimensions[1] - 1], [dimensions[0] - 1, dimensions[1] - 1], [dimensions[0] - 1, 0]]


# Calculamos para cada ponto na iamgem final o seu correpondente na imagem inicial
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

    # Gera a imagem de calibração (Imagem branca com as quinas coloridas)
    if i == 0:
        image2[x, y, :] = 0
    if i == 1:
        image2[x, y] = [255, 0, 0]
    if i == 2:
        image2[x, y] = [0, 255, 0]
    if i == 3:
        image2[x, y] = [0, 0, 255]

    # Apagando os pontos de referencia para o usuario
    cv.circle(image, (y, x), 1, (255, 255, 255), 2)

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
            image[i, j] = xi[x, y]

# Mostra resultado da distorção e salva as imagens (resultado e calibração)
cv.imshow("tela", image)
cv.waitKey(0)
cv.imwrite("img.png", image)
cv.imwrite("img2.png", image2)