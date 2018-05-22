from pprint import pprint
import numpy as np
from copy import deepcopy


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


# def matrizPr(n):
#     A = np.matrix(np.zeros([n, n]))
#     i = 0
#     while i < n:
#         g = int((2 * (i + 1)))
#         if g <= n - 1:
#             A[i, g - 1] = A[i, g] = A[i + 1, int(i / 2)] = round(1 / 6, 4)
#         elif i < n - 1:
#             A[i + 1, int(i / 2)] = round(1 / 2, 4)
#         # A[i, i] = round(1 / 2, 4)
#         i += 1
#     return A


def calcular_vetor_pi_iter(n):
    P = matrizPa(n)
    pi0 = np.matrix(np.zeros(n))
    pi0[0, 0] = 1

    print(P)

    # pprint(pi0)

    R = pi0 * P

    # pprint(R.transpose())

    i = 0
    result = 100
    while result > 10**-6:
        Rn = R * P
        result = (np.sum(np.absolute(R - Rn))) / 2
        R = Rn
        # pprint(R.transpose())
        # print(np.sum(R))
        i += 1
    return R.transpose()


if __name__ == '__main__':
    pi = calcular_vetor_pi_iter(15)
    #
    pprint(pi)
    print(np.sum(pi))
