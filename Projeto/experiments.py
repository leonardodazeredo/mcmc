from algorithms import sa
import tqdm
from pprint import pprint


def gerar_parametros(tsp):
    T0s = [1, 5, 10]
    Ns = [1, 3, 10]
    alphas = [0.9, 0.99, 0.999]

    for T0 in T0s:
        for N in Ns:
            for alpha in alphas:
                yield dict(tsp=tsp, T0=T0, N=N, alpha=alpha, verbose=False)


def run_sa(pram_grip):
    return sa(**pram_grip)


def testar_parametros_paralelo_por_combinacao(tsp):
    parametros_dict_list = list(gerar_parametros(tsp))
    import multiprocessing
    pool = multiprocessing.Pool()
    i = list()
    for r in tqdm.tqdm(pool.imap_unordered(run_sa, parametros_dict_list), total=len(parametros_dict_list)):
        i.append(r)
        # print(r)
    pool.close()
    pool.join()
    return i


def testar_parametros_paralelo_por_arquivo(tsp_path_list):
    from tspparse import read_tsp_file
    pram_grid_list = []
    for tsp_path in tsp_path_list:
        tsp = read_tsp_file(tsp_path)
        pram_grid_list += list(gerar_parametros(tsp))

    import multiprocessing
    pool = multiprocessing.Pool()
    i = list()
    for r in tqdm.tqdm(pool.imap_unordered(run_sa, pram_grid_list), total=len(pram_grid_list)):
        i.append(r)
        # pprint(r)
    pool.close()
    pool.join()
    return i


aux_dict = {}


def process_results(results_list):
    results_list.sort(key=lambda tup: tup[0][1])
    for r in results_list:
        r = list(r)
        # pprint(r[2])
        name_key = r[2]["tsp"]["NAME"]
        if name_key not in aux_dict:
            aux_dict[name_key] = []
        r[2]["tsp"] = name_key
        r[0] = r[0][1]
        aux_dict[name_key].append(r)

    for k, v in aux_dict.items():
        pprint(v[0])
