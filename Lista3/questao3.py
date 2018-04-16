import httplib2
import urllib.parse as urlparse
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


def checkUrl(url):
    p = urlparse.urlparse(url)
    try:
        conn = httplib2.HTTPConnectionWithTimeout(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        # print('O')
        return resp.status < 400

    except Exception:
        # print('X')
        return False


a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def gerar_string(k):
    global a
    ks = list(range(k, 0, -1))
    k = np.random.choice(ks, 1)
    s = np.random.choice(a, k)
    return ''.join(s)


def gerar_url(k):
    return "http://www." + gerar_string(k) + ".ufrj.br/"


def avaliar_indicadora(ss):
    print("Avaliando URLs.")
    import multiprocessing.dummy
    pool = multiprocessing.dummy.Pool(processes=5000)
    i = pool.map(checkUrl, ss)
    pool.close()
    print("URLs avaliadas.")
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


def estimar_multi(n_ini, n_fim, k):
    ps = [gerar_url(k) for i in range(n_ini, n_fim)]
    # pprint(ps)
    ia = avaliar_indicadora(ps)
    # pprint([e for e in ia if e])
    ns = contagem_cumulativa_da_indicadora_por_n(ia)
    ns = [estimar_diretamente(ns[n - 1], n) for n in range(n_ini, n_fim)]
    return ns


def card_D(k):
    c = 0
    for ki in range(k, 0, -1):
        c += 26**ki
    print("Cardinalidade de Dk:", c)
    return c


def plot(n, k=4):
    es = estimar_multi(1, n, k=k)
    es = np.multiply(es, card_D(k=k))
    # pprint([e for e in es if e])
    plt.plot(es)
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    plot(10**4)
