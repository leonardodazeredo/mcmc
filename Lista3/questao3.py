import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from datetime import datetime
import tqdm


def checkUrl(url):
    import socket
    try:
        socket.gethostbyname(url.strip())
        return True
    except socket.gaierror:
        return False


letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                                        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


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
    i = list()
    for r in tqdm.tqdm(pool.imap_unordered(checkUrl, ss), total=len(ss)):
        i.append(r)
    pool.close()
    pool.join()
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


def fazer_e_salvar_amostra(n_ex=5, k=4):
    n = 10**n_ex
    k_arr = [k for i in range(0, n)]
    inicio = datetime.now()
    print("Gerando URLs.")
    import multiprocessing
    pool = multiprocessing.Pool()
    ps = list()
    for r in tqdm.tqdm(pool.imap_unordered(gerar_url, k_arr), total=len(k_arr)):
        ps.append(r)
    pool.close()
    pool.join()
    print("URLs gerandas.", "Tempo:", (datetime.now() - inicio))
    np.savez_compressed(file_name(k), amostra=ps)


def avaliar_e_salvar_amostra(k=4):
    ps = np.load(file_name(k) + ".npz")
    print("n =", len(ps['amostra']))
    ia = avaliar_indicadora(ps['amostra'])
    np.savez_compressed(file_name(k) + "_eval", amostra_eval=ia)


def file_name(k):
    return "k_{}".format(k)


def plot(k=4):
    import os.path
    if not os.path.isfile(file_name(k) + "_eval.npz"):
        fazer_e_salvar_amostra(k=k)

    ia = np.load(file_name(k) + "_eval.npz")
    print("n =", len(ia['amostra_eval']))

    es = estimar_multi(ia=ia['amostra_eval'])
    es = np.multiply(es, card_D(k=k))
    plt.semilogx(es)
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        print("Incorrect use.")

    elif sys.argv[1] == '-save-amostra':
        k = int(sys.argv[2])
        ex = int(sys.argv[3])
        fazer_e_salvar_amostra(ex, k=k)

    elif sys.argv[1] == '-eval-amostra':
        k = int(sys.argv[2])
        avaliar_e_salvar_amostra(k=k)

    elif sys.argv[1] == '-plot':
        k = int(sys.argv[2])
        plot(k=k)

    else:
        print("Inexistent option.")
