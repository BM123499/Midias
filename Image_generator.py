import cv2 as cv
import numpy as np
import Homografy
global lista_destino
lista_destino = []


def click_event(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        global lista_destino
        lista_destino.append((y, x))
        cv.circle(image, (x, y), 1, (255, 0, 0), 2)


image = np.zeros((720, 1280, 3), np.uint8)
image[:, :, 0] = 255
image[:, :, 1] = 255
image[:, :, 2] = 255
image2 = image.copy()

cv.namedWindow("tela", 0)

while len(lista_destino) < 4:
    cv.imshow("tela", image)
    cv.setMouseCallback('tela', click_event)
    cv.waitKey(1)
cv.imshow("tela", image)
cv.waitKey(1000)

xi = cv.imread("teste_IF-760.jpeg", 1)
dimensions = xi.shape
lista_origem = [[0, 0], [0, dimensions[1] - 1], [dimensions[0] - 1, dimensions[1] - 1], [dimensions[0] - 1, 0]]
H = Homografy.homografy(lista_destino, lista_origem)
H2 = Homografy.homografy(lista_origem, lista_destino)

min_x = 1281
min_y = 1281
max_x = 0
max_y = 0
for i in range(4):
    p = lista_origem[i]
    pixel_alvo = np.matmul(H2, np.array([[p[0]], [p[1]], [1]]))
    pixel_alvo = np.divide(pixel_alvo, pixel_alvo[2][0])
    x = round(pixel_alvo[0][0])
    y = round(pixel_alvo[1][0])
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    image2[x, y, :] = 0
    cv.circle(image, (y, x), 1, (255, 255, 255), 2)

for i in range(min_x, max_x+1):
    for j in range(min_y, max_y+1):
        pixel_alvo = np.matmul(H, np.array([[i], [j], [1]]))
        pixel_alvo = np.divide(pixel_alvo, pixel_alvo[2][0])
        x = round(pixel_alvo[0][0])
        y = round(pixel_alvo[1][0])
        if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]:
            image[i, j] = xi[x, y]

cv.imshow("tela", image)
cv.waitKey(0)
cv.imwrite("img.png", image)
cv.imwrite("img2.png", image2)