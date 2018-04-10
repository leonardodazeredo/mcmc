import numpy as np
import math
from pprint import pprint
import matplotlib.pyplot as plt


def gerar_pontos(n):
    xs = np.random.uniform(1, 2, n)
    ys = np.random.uniform(0, 1, n)
    p = zip(xs, ys)
    return list(p)


def avaliar_indicadora(pontos):
    i = [(True if x**(-1) >= y else False) for x, y in pontos]
    return i


def estimar_e(indicadora_avaliada):
    abaixo = len([e for e in indicadora_avaliada if e])
    return estimar_e_diretamente(abaixo, len(indicadora_avaliada))


def estimar_e_diretamente(abaixo, total):
    if abaixo == 0:
        abaixo = 0.01
    r = abaixo / total
    e = 2**(1 / r)
    return e


def f(l):
    l2 = list()
    k = 0
    for e in l:
        if e:
            k = k + 1
        l2.append(k)
    return l2


def estimar_e_multi(n_ini, n_fim):
    ps = gerar_pontos(n_fim)
    ia = avaliar_indicadora(ps)

    ns = f(ia)

    ns = [estimar_e_diretamente(ns[n - 1], n) for n in range(n_ini, n_fim)]

    return ns


if __name__ == '__main__':
    n = 10**6
    # ps = gerar_pontos(n)
    # ia = avaliar_indicadora(ps)
    # a = estimar_e(ia)
    es = estimar_e_multi(1, n)

    es = [math.fabs(e - math.e) / math.e for e in es]

    se = [1 / math.sqrt(i) for i in range(1, n)]

    plt.loglog(es, basex=2, basey=2)
    plt.loglog(se, basex=2, basey=2)
    plt.show()
