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
    return A


def matrizPb(n):
    A = np.matrix(np.zeros([n, n]))
    A[0, 0] = 1 / 2
    A[0, 1] = A[0, 2] = 1 / 4
    A[1, 0] = 1 / 6
    i = 1
    while i < n:
        g = int((2 * (i + 1)))
        if g <= n - 1:
            A[i, g - 1] = A[i, g] = A[i + 1, int(i / 2)] = 1 / 6
        elif i < n - 1:
            A[i + 1, int(i / 2)] = 1 / 2
        if g == n - 1:
            A[i + 1, int(i / 2)] = 1 / 2
        A[i, i] = 1 / 2
        i += 1
    for l in A:
        print(round(np.sum(l), 6))
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
    return (np.sum(np.absolute(piR - pi))) / 2


def calcular_vetor_pi_iter(n, P):
    pi = pi_direto(P)

    piList = []

    pi0 = np.matrix(np.zeros(n))
    pi0[0, 0] = 1
    piList.append(pi0)

    piR = pi0 * P
    piList.append(piR)
    i = 0
    result = 1
    while result > 10**-2:
        piR = piR * P
        piList.append(piR)
        result = DVT(piR, pi)
        # print(result)
        # pprint(piR.transpose())
        # piRn = piR * P
        # result = (np.sum(np.absolute(piR - piRn))) / 2
        # piR = piRn
        i += 1
    return pi, piList


def grafico(api, apiList, bpi, bpiList):

    adata = [DVT(api, e) for e in apiList]
    # bdata = [DVT(bpi, e) for e in bpiList]

    plt.loglog(adata)
    # plt.loglog(bdata)
    plt.grid(True)
    plt.title('loglog value')

    plt.show()


if __name__ == '__main__':
    n = 15
    # matriz = matrizPa
    #
    # pprint(matrizPa(n))

    P = matrizPa(n)
    print(pi_direto(P))
    P = matrizPb(n)
    print(pi_direto(P))

    api, apiList = calcular_vetor_pi_iter(n, matrizPa(n))
    bpi, bpiList = 0,0#calcular_vetor_pi_iter(n, matrizPb(n))

    grafico(api, apiList, bpi, bpiList)

    # pprint(pi)
    # print(np.sum(pi))
