from algorithms import sa
import tqdm


def gerar_parametros(tsp):
    T0s = [1, 5, 10]
    Ns = [1, 3, 10]
    alphas = [0.9, 0.99, 0.999]

    for T0 in T0s:
        for N in Ns:
            for alpha in alphas:
                yield dict(tsp=tsp, T0=T0, N=N, alpha=alpha, verbose=False)


def test(pram_grip):
    return sa(**pram_grip)


def testar_parametros_paralelo_por_combinacao(tsp):
    parametros_dict_list = list(gerar_parametros(tsp))
    import multiprocessing
    pool = multiprocessing.Pool()
    i = list()
    for r in tqdm.tqdm(pool.imap_unordered(test, parametros_dict_list), total=len(parametros_dict_list)):
        i.append(r)
        # print(r)
    pool.close()
    pool.join()
