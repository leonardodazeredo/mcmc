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
    pprint(A)
    return A


def matrizPb(n):
    V1 = 1 / 2
    V2 = 1 / 4
    V3 = round(1 / 6, 5)
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

    pprint(A)
    #
    # for l in A:
    #     print(round(np.sum(l), 6))
    return A


def pi_direto(P, n):
    W = P[np.where(P > 0)].shape[1]
    # print(W)
    pi = []
    for l in P:
        g = l[np.where(l > 0)].shape[1]
        # print(l[np.where(l > 0)])
        pi.append((g - 1) / (W - n))
    return np.matrix(pi).transpose()


def DVT(piR, pi):
    valor = (np.sum(np.absolute(piR - pi.transpose()))) / 2
    return valor


def calcular_vetor_pi_iter(n, P):
    pi = pi_direto(P, n)

    piList = []

    pi0 = np.matrix(np.zeros(n))
    pi0[0, 0] = 1
    piList.append(pi0)

    piR = pi0 * P
    piList.append(piR)
    i = 0
    while i < 10**4:
        piR = piR * P
        piList.append(piR)
        # result = DVT(piR, pi)
        # print(result)
        # pprint(piR.transpose())
        i += 1
    # pprint(piR)
    # result = 1
    # while result > 10**-2:
    #     piR = piR * P
    #     piList.append(piR)
    #     result = DVT(piR, pi)
    #     print(result)
    #     # pprint(piR.transpose())
    #     i += 1
    return pi, piList


def grafico(api, apiList, bpi, bpiList):

    adata = [DVT(api, e) for e in apiList]
    bdata = [DVT(bpi, e) for e in bpiList]

    plt.loglog(adata)
    plt.loglog(bdata)
    plt.grid(True)
    plt.title('loglog value')

    plt.show()


if __name__ == '__main__':
    n = 1023
    # matriz = matrizPa
    #
    # pprint(matrizPa(n))

    # P = matrizPa(n)
    # print(pi_direto(P))
    # P = matrizPb(n)
    # print(P)
    # print(pi_direto(P))

    api, apiList = calcular_vetor_pi_iter(n, matrizPa(n))
    bpi, bpiList = calcular_vetor_pi_iter(n, matrizPb(n))

    grafico(api, apiList, bpi, bpiList)

    # pprint(pi)
    # print(np.sum(pi))
