import numpy as np
import math
from pprint import pprint
import matplotlib.pyplot as plt

LIMITE = 5


def gerar_amostra(n):
    xs = np.random.normal(size=n)
    # pprint(xs)
    return xs


def avaliar_indicadora(amostra):
    i = [(True if x >= LIMITE else False) for x in amostra]
    return i


def estimar(n_fim):
    ps = gerar_amostra(n_fim)
    ia = avaliar_indicadora(ps)
    abaixo = len([e for e in ia if e])
    return estimar_diretamente(abaixo, len(ia))


def estimar_diretamente(abaixo, total):
    r = np.divide(abaixo, total)
    return r


def contagem_cumulativa_da_indicadora_por_n(l):
    l2 = list()
    k = 0
    for e in l:
        if e:
            k = k + 1
        l2.append(k)
    return l2


def estimar_multi(n_ini, n_fim):
    ps = gerar_amostra(n_fim)
    ia = avaliar_indicadora(ps)
    ns = contagem_cumulativa_da_indicadora_por_n(ia)
    ns = [estimar_diretamente(ns[n - 1], n) for n in range(n_ini, n_fim)]
    return ns


def plot(n):
    es = estimar_multi(1, n)

    plt.semilogx(es)
    plt.grid(True)
    plt.title('loglog value')

    plt.show()


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        ex = int(sys.argv[1])
        n = 10**ex
        plot(n)
        # print(estimar(n))

    else:
        print("Inexistent option.")
