import cv2 as cv
import numpy as np
import Homografy
global lista_destino
lista_destino = []
global lista_origem
lista_origem = []


def click_event1(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        global lista_destino
        lista_destino.append((y, x))
        cv.circle(image, (x, y), 1, (0, 0, 255), 2)


def click_event2(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        global lista_origem
        lista_origem.append((y, x))
        cv.circle(image, (x, y), 1, (0, 255, 255), 2)


image = cv.imread("img.jpeg", 1)
dimensions = image.shape
image2 = image.copy()

while len(lista_destino) < 4:
    cv.imshow("tela", image)
    cv.setMouseCallback('tela', click_event1)
    cv.waitKey(1)
while len(lista_origem) < 4:
    cv.imshow("tela", image)
    cv.setMouseCallback('tela', click_event2)
    cv.waitKey(1)
cv.imshow("tela", image)
cv.waitKey(1000)

H = Homografy.homografy(lista_destino, lista_origem)

for i in range(dimensions[0]):
    for j in range(dimensions[1]):
        pixel_alvo = np.matmul(H, np.array([[i], [j], [1]]))
        pixel_alvo = np.divide(pixel_alvo, pixel_alvo[2][0])
        x = round(pixel_alvo[0][0])
        y = round(pixel_alvo[1][0])
        if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]:
            image[i, j] = image2[x, y]
        else:
            image[i, j] = [255, 255, 255]

cv.imshow("tela", image)
cv.waitKey(0)