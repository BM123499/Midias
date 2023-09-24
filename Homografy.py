import numpy as np

def homografy(pontos_origem, pontos_destino):

    A = []
    B = []
    for i in range(4):
        po = pontos_origem[i]
        pd = pontos_destino[i]
        A.append([0, 0, 0, -1 * po[0], -1 * po[1], -1, pd[1] * po[0], pd[1] * po[1]])
        A.append([po[0], po[1], 1, 0, 0, 0, -1 * pd[0] * po[0], -1 * pd[0] * po[1]])
        B.append([-1*pd[1]])
        B.append([pd[0]])

    x = np.linalg.solve(np.array(A), np.array(B))
    return np.array([[x[0][0], x[1][0], x[2][0]],
                     [x[3][0], x[4][0], x[5][0]],
                     [x[6][0], x[7][0],      1]])


# a = [[1, 1], [1, 2], [2, 2], [2, 1]]
# b = [[1, 1], [0.5, 0.5], [1, 0.5], [2, 1]]
# print(homografy(a, b))
