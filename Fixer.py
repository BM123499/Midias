import cv2 as cv
import numpy as np
import Homografy
global lista_destino
lista_destino = []
global lista_origem
lista_origem = []


def click_event(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        global lista_destino
        lista_destino.append((y, x))
        cv.circle(image, (x, y), 1, (0, 0, 255), 2)

image_origem = cv.imread("img2.png", 0)
lista_origem = [(x, y) for x in range(image_origem.shape[0])
                       for y in range(image_origem.shape[1])
                       if image_origem[x, y] == 0]

global ponto_medio
ponto_medio = [0, 0]
for p in lista_origem:
    ponto_medio[0] += p[0]
    ponto_medio[1] += p[1]

ponto_medio[0] /= len(lista_origem)
ponto_medio[1] /= len(lista_origem)

print(ponto_medio)
print(len(lista_origem))
print(lista_origem)

image = cv.imread("img.png", 1)
dimensions = image.shape
image2 = image.copy()

while len(lista_destino) < 4:
    cv.imshow("tela", image)
    cv.setMouseCallback('tela', click_event)
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
