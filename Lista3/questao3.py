import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from datetime import datetime


def checkUrl(url):
    import socket
    try:
        socket.gethostbyname(url.strip())
        return True
    except socket.gaierror:
        return False


letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def gerar_string(k):
    global letras
    ks = list(range(k, 0, -1))
    k = np.random.choice(ks, 1)
    s = np.random.choice(letras, k)
    return ''.join(s)


def gerar_url(k):
    return "www." + gerar_string(k) + ".ufrj.br"


def avaliar_indicadora(ss):
    inicio = datetime.now()
    print("Avaliando URLs.")
    import multiprocessing.dummy
    pool = multiprocessing.dummy.Pool(processes=100)
    i = pool.map(checkUrl, ss)
    pool.close()
    print("URLs avaliadas.", "Tempo:", (datetime.now() - inicio))
    return i


def estimar_e(indicadora_avaliada):
    abaixo = len([e for e in indicadora_avaliada if e])
    return estimar_diretamente(abaixo, len(indicadora_avaliada))


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


def estimar_multi(n_ini=1, n_fim=None, ia=None):
    if ia is None:
        raise ValueError('Ia none.')
    if n_fim is None:
        n_fim = len(ia)
    ns = contagem_cumulativa_da_indicadora_por_n(ia)
    ns = [estimar_diretamente(ns[n - 1], n) for n in range(n_ini, n_fim)]
    return ns


def card_D(k):
    c = 0
    for ki in range(k, 0, -1):
        c += len(letras)**ki
    print("Cardinalidade de Dk:", c)
    return c


def fazer_e_salvar_amostra(n_ex, k=4):
    n = 10**n_ex
    ps = [gerar_url(k) for i in range(0, n)]
    ia = avaliar_indicadora(ps)
    np.save(open(file_name(k, n_ex), "wb"), ia)


def file_name(k, n_ex):
    return "k_{}_n_ex_{}".format(k, n_ex)


def plot(n_ex=6, k=4):
    import os.path
    if not os.path.isfile(file_name(k, n_ex)):
        fazer_e_salvar_amostra(n_ex=n_ex, k=k)

    ia = np.load(open(file_name(k, n_ex), "rb"))

    es = estimar_multi(ia=ia)
    es = np.multiply(es, card_D(k=k))
    # pprint([e for e in es if e])
    # plt.yticks(np.arange(-50, 1500, 50))
    plt.semilogx(es)
    # plt.plot(es)
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        print("Incorrect use.")

    elif sys.argv[1] == '-save':
        k = int(sys.argv[2])
        ex = int(sys.argv[3])
        fazer_e_salvar_amostra(ex, k=k)

    elif sys.argv[1] == '-plot':
        k = int(sys.argv[2])
        ex = int(sys.argv[3])
        plot(n_ex=ex, k=k)

    else:
        print("Inexistent option.")
