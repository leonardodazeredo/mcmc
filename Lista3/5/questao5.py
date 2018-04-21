import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import math
import sys
from decimal import Decimal


def G(i):
    return i * math.log(i, math.e)


def Z(i):
    # return math.pow(i, 1 / math.e)
    return i


def calc_C():
    C = 0
    for e in range(1, 1001):
        C += Z(e)
    return C


C = calc_C()


def H(i):
    global C
    return Z(i) / C


def G_SUM():
    S = 0
    for i in range(1, 1001):
        S += G(i)
    return S


valor_real = G_SUM()


def M2(H):
    M2 = 0
    for i in range(1, 1001):
        M2 += math.pow(G(i), 2) / H(i)
    print('%.2E' % Decimal(M2))


def gerar_i(n):
    # arr = [(Z(i), i) for i in range(1, 1001)]
    # iarr = list()
    # for v, i in arr:
    #     for _ in range(0, v):
    #         iarr.append(i)
    # return np.random.choice(iarr, n)
    arr = [i for i in range(1, 1001)]
    iarr = [H(i) for i in arr]
    return np.random.choice(arr, n, p=iarr)


def Mn(amostra):
    Mn = 0
    for i in amostra:
        Mn += G(i) / H(i)
    return Mn / len(amostra)


def Mn_arr(amostra):
    arr = list()
    Mn = 0
    for c, i in enumerate(amostra):
        Mn += G(i) / H(i)
        arr.append(Mn / (c + 1))
    return arr


def estimar_multi(n):
    ps = gerar_i(n)
    arr = Mn_arr(ps)
    return arr


def plot(n):
    global valor_real

    es = estimar_multi(n)
    # pprint(es)
    print(es[-1], " - ", round(math.fabs(es[-1] - valor_real) / valor_real, 8))
    er = [math.fabs(e - valor_real) / valor_real for e in es]

    plt.subplot(211)
    plt.loglog(er)
    plt.loglog([1 / math.sqrt(i) for i in range(1, n)])
    plt.grid(True)
    plt.title('G relative error')

    plt.subplot(212)
    plt.semilogx(es)
    plt.semilogx([valor_real for i in range(1, n)])
    plt.grid(True)
    plt.title('G value')

    plt.show()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        M2(H)
        # print(valor_real)
        plot(10**int(sys.argv[1]))

    else:
        print("Inexistent option.")
