from pprint import pprint
import numpy as np
from copy import deepcopy


def matrizP(p0, p1, p2):
    P = [
        [(1 - p0**2), 0, 0, 0, p0**2, 0, 0, 0, 0],
        [p1 * (1 - p0), (1 - p1), 0, 0, 0, p1 * p0, 0, 0, 0],
        [p2 * (1 - p0), 0, (1 - p2), 0, 0, p2 * p0, 0, 0, 0],
        [p1 * (1 - p0), 0, 0, (1 - p1), 0, 0, 0, p1 * p0, 0],
        [0, (p1 - p1**2), 0, (p1 - p1**2), (1 - p1)**2, 0, 0, 0, p1**2],
        [0, 0, p1 * (1 - p2), p2 * (1 - p1), 0, (1 - p1 - p2 + p1 * p2), 0, 0, p2 * p1],
        [p2 * (1 - p0), 0, 0, 0, 0, 0, (1 - p2), p2 * p0, 0],
        [0, p2 * (1 - p1), 0, 0, 0, 0, p1 * (1 - p2), (1 - p1 - p2 + p1 * p2), p2 * p1],
        [0, 0, (p2 - p2**2), 0, 0, 0, (p2 - p2**2), 0, (2 * (p2**2) - 2 * p2 + 1)]
    ]
    return roundM(P)


def matrizA(p0, p1, p2):
    P = matrizP(p0, p1, p2)
    A = deepcopy(P)
    for i, l in enumerate(A):
        l[i] -= 1

    A = roundM(A)
    A = np.matrix(A).transpose()
    A = np.vstack([A, [1, 1, 1, 1, 1, 1, 1, 1, 1]])
    return A


def roundM(A, n=6):
    ml = []
    for l in A:
        ml.append(list(map((lambda x: round(x, n)), l)))
    return ml


def calcular_vetor_pi(p0, p1, p2):
    A = matrizA(p0, p1, p2)

    pprint(A)
    B = np.matrix([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

    pi = A.I * B.transpose()
    return pi


def calcular_vetor_pi_iter(p0, p1, p2):
    P = matrizP(p0, p1, p2)
    P = np.matrix(P)

    pi0 = np.matrix([0, 0, 0, 0, 1, 0, 0, 0, 0])

    R = pi0 * P
    i = 0
    result = 100
    while result > 10**-6:
        Rn = R * P
        result = (np.sum(np.absolute(R - Rn))) / 2
        R = Rn
        i += 1
    return R.transpose()


if __name__ == '__main__':
    # _pi = calcular_vetor_pi(0.5, 0.3, 0.1)
    # print(_pi)
    # _pi = calcular_vetor_pi_iter(0.5, 0.3, 0.1)
    # print(_pi)
    # pprint(matrizP())
    # for l in P:
    #     print(round(sum(l), 6))

    melhor = (0, 0)
    # ps = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    ps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    i = 1
    for p0 in ps:
        for p1 in ps:
            for p2 in ps:
                if p0 > p1 > p2:
                    pi = calcular_vetor_pi(p0, p1, p2)
                    v = pi[0, 0] + pi[1, 0] + pi[2, 0] + pi[3, 0] + pi[6, 0]
                    if melhor[0] < v:
                        melhor = v, pi
                    print("\n########################################################")
                    print("\n{}:".format(i), p0, p1, p2)
                    # pprint(matrizP(p0, p1, p2))
                    # pprint(melhor)
                    i += 1
                    # if not np.equal(_pi, pi).all():
                    #     pprint(matrizP(p0, p1, p2))
                    #     pprint(pi)

    pprint(melhor)
