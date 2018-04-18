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
    pool = multiprocessing.dummy.Pool(processes=200)
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


def fazer_e_salvar_amostra(n_ex=5, k=4, sufixo=""):
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
    file_name = file_name_amostra(k, n_ex) + "_" + sufixo
    np.savez_compressed(file_name, amostra=ps)
    return k, n_ex, file_name


def avaliar_e_salvar_indicadora(file_name=None):
    if file_name is None:
        raise ValueError('File_name none.')
    ps = np.load(file_name)
    n, k = get_n(ps), get_k(file_name)
    print("n =", n)
    ia = avaliar_indicadora(ps['amostra'])
    n_ex = str(n).count('0')
    file_name = file_name_indicadora(file_name_amostra=file_name)
    np.savez_compressed(file_name, amostra_eval=ia)
    return k, n_ex, file_name


def file_name_amostra(k, n_ex):
    return "k_{}_n_ex_{}".format(k, n_ex)


def file_name_indicadora(k=None, n_ex=None, file_name_amostra=None):
    if file_name_amostra is None:
        return "k_{}_n_ex_{}_eval".format(k, n_ex)
    else:
        return file_name_amostra.replace(".npz", "_eval")


def get_n(arrs):
    return len(arrs['amostra'])


def get_k(file_name):
    return int(file_name[file_name.index("k_") + 2])


def plot(file_name=None):
    import os
    if file_name is None:
        raise ValueError('File_name none.')
    if not os.path.isfile(file_name):
        raise ValueError('File não existe.')
    if not os.path.isfile(file_name_indicadora(file_name_amostra=file_name) + ".npz"):
        avaliar_e_salvar_indicadora(file_name)

    ps = np.load(file_name)
    n, k = get_n(ps), get_k(file_name)
    del ps

    ia = np.load(file_name_indicadora(file_name_amostra=file_name) + ".npz")
    pprint((n, k))

    es = estimar_multi(ia=ia['amostra_eval'])
    es = np.multiply(es, card_D(k=k))
    plt.semilogx(es)
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        print("Incorrect use.")

    elif sys.argv[1] == '-amostrar':
        k = int(sys.argv[2])
        ex = int(sys.argv[3])
        su = sys.argv[4]
        fazer_e_salvar_amostra(n_ex=ex, k=k, sufixo=su)

    elif sys.argv[1] == '-avaliar':
        avaliar_e_salvar_indicadora(file_name=sys.argv[2])

    elif sys.argv[1] == '-plotar':
        plot(file_name=sys.argv[2])

    else:
        print("Inexistent option.")
