from pprint import pprint
import numpy as np


def roundM(A):
    ml = []
    for l in A:
        ml.append(list(map((lambda x: round(x, 4)), l)))
    return ml


def calcular_vetor_pi(p0=0.5, p1=0.3, p2=0.1):
    A = [
        [(1 - p0**2 - 1), 0, 0, 0, p0**2, 0, 0, 0, 0],
        [p1 * (1 - p0), (1 - p1 - 1), 0, 0, 0, p1 * p0, 0, 0, 0],
        [p2 * (1 - p0), 0, (1 - p2 - 1), 0, 0, p2 * p0, 0, 0, 0],
        [p1 * (1 - p0), 0, 0, (1 - p1 - 1), 0, 0, 0, p1 * p0, 0],
        [0, (p1 - p1**2), 0, (p1 - p1**2), (1 - p1)**2 - 1, 0, 0, 0, p1**2],
        [0, 0, p1 * (1 - p2), p2 * (1 - p1), 0, (1 - p1 - p2 + p1 * p2 - 1), 0, 0, p2 * p1],
        [p2 * (1 - p0), 0, 0, 0, 0, 0, (1 - p2 - 1), p2 * p0, 0],
        [0, p2 * (1 - p1), 0, 0, 0, 0, p1 * (1 - p2), (1 - p1 - p2 + p1 * p2 - 1), p2 * p1],
        [0, 0, (p2 - p2**2), 0, 0, 0, (p2 - p2**2), 0, (2 * (p2**2) - 2 * p2 + 1 - 1)],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    A = np.matrix(roundM(A))
    B = np.matrix([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

    pi = A.I * B.transpose()
    return pi


if __name__ == '__main__':
    # ps = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
    ps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for p0 in ps:
        for p1 in ps:
            for p2 in ps:
                pi = calcular_vetor_pi(p0, p1, p2)
                print("\n", p0, p1, p2)
                pprint(pi)
