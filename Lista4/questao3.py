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
    i = 0
    while i < n:
        g = int((2 * (i + 1)))
        if g <= n - 1:
            A[i, g - 1] = A[i, g] = A[i + 1, int(i / 2)] = round(1 / 6, 4)
        elif i < n - 1:
            A[i + 1, int(i / 2)] = round(1 / 2, 4)
        A[i, i] = round(1 / 2, 4)
        i += 1
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
#         A[i, i] = round(1 / 2, 4)
#         i += 1
#     return A

def roundM(A, n=6):
    ml = []
    for l in A:
        ml.append(list(map((lambda x: round(x, n)), l)))
    return ml


def calcular_vetor_pi_iter(p0, p1, p2):
    P = matrizP(p0, p1, p2)
    P = np.matrix(P)

    pi0 = np.matrix([0, 0, 0, 0, 1, 0, 0, 0, 0])

    R = pi0 * P
    i = 0
    result = 100
    while result > 10**-10:
        Rn = R * P
        result = (np.sum(np.absolute(R - Rn))) / 2
        R = Rn
        i += 1
    return R.transpose()


if __name__ == '__main__':
    pprint(matrizPb(15))
