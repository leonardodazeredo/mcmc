from pprint import pprint
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt


def matrizPa(n):
    A = np.matrix(np.zeros([n, n]))
    i = 0
    while i < n:
        if (i != n - 1):
            A[i, i + 1] = 1 / 4
        else:
            A[i, 0] = 1 / 4
        A[i, i - 1] = 1 / 4
        A[i, i] = 1 / 2
        i += 1
    # pprint(A)
    return A


def matrizPb(n):
    V1 = 1 / 2
    V2 = 1 / 4
    V3 = 1 / 6
    A = np.matrix(np.zeros([n, n]))

    i = 0
    j = 1
    while j + 1 < n:
        A[i, j] = A[i, j + 1] = 1
        i += 1
        j += 2

    i = 1
    j = 0
    while i + 1 < n:
        A[i, j] = A[i + 1, j] = 1
        i += 2
        j += 1

    for l in A:
        x = l[np.where(l > 0)].shape[1]
        if x == 1:
            l[np.where(l > 0)] = V1
        elif x == 2:
            l[np.where(l > 0)] = V2
        elif x == 3:
            l[np.where(l > 0)] = V3

    for i in range(0, n):
        A[i, i] = V1

    # pprint(A)
    #
    # for l in A:
    #     print(round(np.sum(l), 6))
    return A


def pi_direto(P):
    W = P[np.where(P > 0)].shape[1]
    # print(W)
    pi = []
    for l in P:
        g = l[np.where(l > 0)].shape[1]
        # print(l[np.where(l > 0)])
        pi.append(g / W)
    return np.matrix(pi).transpose()


def DVT(piR, pi):
    valor = (np.sum(np.absolute(piR - pi.transpose()))) / 2
    # if valor > 1:
    #     pprint(piR)
    #     pprint(pi.transpose())
    # exit(0)
    return valor


def calcular_vetor_pi_iter(n, P):
    pi = pi_direto(P)

    piList = []

    pi0 = np.matrix(np.zeros(n))
    pi0[0, 0] = 1
    piList.append(pi0)

    piR = pi0 * P
    piList.append(piR)
    i = 0
    # pprint(piR)
    result = 1
    while result > 10**-6:
        piR = piR * P
        piList.append(piR)
        result = DVT(piR, pi)
        if result > 1:
            break
        # print(result)
        # pprint(piR.transpose())
        i += 1

    return pi, piList, i


def rodar_para_anel(ns):
    tempos_anel = []
    for n in ns:
        pi, piList, i = calcular_vetor_pi_iter(n, matrizPa(n))
        tempos_anel.append(i)
        # print(piList[-1])

    tempos_arvore = []
    for n in ns:
        pi, piList, i = calcular_vetor_pi_iter(n, matrizPb(n))
        tempos_arvore.append(i)
        # tempos_arvore.append(10000)
    # print(piList[-1])
    # data to plot
    n_groups = len(ns)

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    plt.bar(index, tempos_anel, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Anel')

    plt.bar(index + bar_width, tempos_arvore, bar_width,
                     alpha=opacity,
                     color='g',
                     label='Arvore')

    plt.xlabel('Grafo')
    plt.ylabel('Tempo')
    plt.xticks(index + bar_width, ns)
    plt.legend()

    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    # ns = [10, 50, 100]#, 300, 700, 1000, 3000, 5000, 10000]
    ns = [15, 31, 127, 511]#, 300, 700, 1000, 3000, 5000, 10000]
    rodar_para_anel(ns)
    # matriz = matrizPa
    #
    # pprint(matrizPa(n))

    # P = matrizPa(n)
    # print(pi_direto(P))
    # P = matrizPb(n)
    # print(P)
    # print(pi_direto(P))
    #
    # api, apiList = calcular_vetor_pi_iter(n, matrizPa(n))
    # bpi, bpiList = calcular_vetor_pi_iter(n, matrizPb(n))
    #
    # grafico(api, apiList, bpi, bpiList)

    # pprint(pi)
    # print(np.sum(pi))
