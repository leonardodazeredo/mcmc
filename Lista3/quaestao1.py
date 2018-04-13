import numpy as np
import math
from pprint import pprint
import matplotlib.pyplot as plt


def gerar_pontos_e(n):
    xs = np.random.uniform(1, 2, n)
    ys = np.random.uniform(0, 1, n)
    p = zip(xs, ys)
    return list(p)


def gerar_pontos_pi(n):
    xs = np.random.uniform(-1, 1, n)
    ys = np.random.uniform(-1, 1, n)
    p = zip(xs, ys)
    return list(p)


def avaliar_indicadora_e(pontos):
    i = [(True if x**(-1) >= y else False) for x, y in pontos]
    return i


def avaliar_indicadora_pi(pontos):
    i = [(True if x**2 + y**2 <= 1 else False) for x, y in pontos]
    return i


def estimar_e(indicadora_avaliada):
    abaixo = len([e for e in indicadora_avaliada if e])
    return estimar_e_diretamente(abaixo, len(indicadora_avaliada))


def estimar_e_diretamente(abaixo, total):
    if abaixo == 0:
        abaixo = 0.01
    r = round(abaixo / total, 8)
    e = round(2**(1 / r), 8)
    return e


def estimar_pi_diretamente(dentro, total):
    if dentro == 0:
        dentro = 0.000001
    r = round(dentro / total, 8)
    pi = round(4 * r, 8)
    return pi


def f(l):
    l2 = list()
    k = 0
    for e in l:
        if e:
            k = k + 1
        l2.append(k)
    return l2


def estimar_e_multi(n_ini, n_fim):
    ps = gerar_pontos_e(n_fim)
    ia = avaliar_indicadora_e(ps)

    ns = f(ia)

    ns = [estimar_e_diretamente(ns[n - 1], n) for n in range(n_ini, n_fim)]

    return ns


def estimar_pi_multi(n_ini, n_fim):
    ps = gerar_pontos_pi(n_fim - n_ini)
    ia = avaliar_indicadora_pi(ps)

    ns = f(ia)

    ns = [estimar_pi_diretamente(ns[idx], n_ini + idx) for idx in range(0, len(ns))]

    return ns


def plot_e_error(n):
    es = estimar_e_multi(1, n)
    print(es[-1], " - ", round(math.fabs(es[-1] - math.e) / math.e, 8))
    es = [round(math.fabs(e - math.e) / math.e, 8) for e in es]
    se = [1 / math.sqrt(i) for i in range(1, n)]
    plt.loglog(es)  # , basex=2, basey=2)
    plt.loglog(se)  # , basex=2, basey=2)
    plt.show()


def plot_e(n):
    es = estimar_e_multi(1, n)
    print(es[-1], " - ", round(math.fabs(es[-1] - math.e) / math.e, 8))
    # es = [round(math.fabs(e - math.e) / math.e, 8) for e in es]
    se = [math.e for i in range(1, n)]
    plt.loglog(es)  # , basex=2, basey=2)
    plt.loglog(se)  # , basex=2, basey=2)
    plt.show()


def plot_pi_error(n):
    es = estimar_pi_multi(1, n)
    print(es[-1], " - ", round(math.fabs(es[-1] - math.pi) / math.pi, 8))
    es = [round(math.fabs(e - math.pi) / math.pi, 8) for e in es]
    se = [1 / math.sqrt(i) for i in range(1, n)]
    plt.loglog(es)  # , basex=2, basey=2)
    plt.loglog(se)  # , basex=2, basey=2)
    plt.show()


def plot_pi(n):
    es = estimar_pi_multi(1, n)
    print(es[-1], " - ", round(math.fabs(es[-1] - math.pi) / math.pi, 8))
    # es = [round(math.fabs(e - math.pi) / math.pi, 8) for e in es]
    se = [math.pi for i in range(1, n)]
    plt.loglog(es)  # , basex=2, basey=2)
    plt.loglog(se)  # , basex=2, basey=2)
    plt.show()


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        n = 10**6
        plot_e_error(n)

    elif sys.argv[2] == 'e':
        ex = int(sys.argv[3])
        n = 10**ex
        if sys.argv[1] == '-e':
            plot_e_error(n)
        elif sys.argv[1] == '-v':
            plot_e(n)
        else:
            print("Inexistent option.")

    elif sys.argv[2] == 'pi':
        ex = int(sys.argv[3])
        n = 10**ex
        if sys.argv[1] == '-e':
            plot_pi_error(n)
        elif sys.argv[1] == '-v':
            plot_pi(n)
        else:
            print("Inexistent option.")

    else:
        print("Inexistent option.")
