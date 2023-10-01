import numpy as np

def homografy(pontos_origem, pontos_destino):

    M = []
    # Para cada correspondecia
    for i in range(4):

        # Armazena Xi e Xi'
        po = pontos_origem[i]
        pd = pontos_destino[i]

        # Criando a matriz A (8x9)
        M.append([0, 0, 0, -1 * po[0], -1 * po[1], -1, pd[1] * po[0], pd[1] * po[1], pd[1]])
        M.append([po[0], po[1], 1, 0, 0, 0, -1 * pd[0] * po[0], -1 * pd[0] * po[1], -1*pd[0]])

    # A fim de impedir infinitas soluções isolamos a ultima variavel da matriz Ai e atualizando seu valor para 1
    A = [[X[i] for i in range(9) if i != 8] for X in M]
    B = [[-X[i] for i in range(9) if i == 8] for X in M]
    x = np.linalg.solve(np.array(A), np.array(B))
    return np.array([[x[0][0], x[1][0], x[2][0]],
                     [x[3][0], x[4][0], x[5][0]],
                     [x[6][0], x[7][0],      1]])
