#!/usr/bin/env python3
from argparser import parser
from tspparse import read_tsp_file
from algorithms import calc_nearest_neighbor_tour, calc_in_order_tour, calc_furthest_neighbor_tour, sa

from glob import iglob
from os.path import isfile, isdir, join, exists
from pprint import pprint

import sys
sys.setrecursionlimit(10000)


def glean_tsp_files(path_arg_list):
    for path_arg in path_arg_list:

        if isdir(path_arg):
            for filepath in iglob(join(path_arg, "*.tsp")):
                yield filepath

        elif isfile(path_arg) & str(path_arg).endswith(".tsp"):
            yield path_arg

        elif isfile(path_arg) & (not path_arg.endswith(".tsp")):
            print("Can't open file ``{0}'': not a .tsp file".format(path_arg))

        elif exists(path_arg):
            print("Path {0} is neither a file nor a directory".format(path_arg))

        else:
            print("Path {0} does not exist".format(path_arg))


def process_from_tsp_path(call_args, tsp_path):
    tsp = read_tsp_file(tsp_path)
    print("TSP Problem:              {}".format(tsp["NAME"]))
    print("PATH:                     {}".format(tsp_path))
    print("DIMENSION:                {} points".format(tsp["DIMENSION"]))

    if call_args.call_all:
        from experiments import testar_parametros_paralelo_por_combinacao

        testar_parametros_paralelo_por_combinacao(tsp)

    else:
        if call_args.need_in_order:
            print("IN-ORDER TOUR LENGTH:     {}".format(calc_in_order_tour(tsp)))

        if call_args.need_nearest_neighbor:
            print("NEAREST NEIGHBOR LENGTH:  {}".format(calc_nearest_neighbor_tour(tsp)))

        if call_args.need_furthest_neighbor:
            print("FURTHEST NEIGHBOR LENGTH: {}".format(calc_furthest_neighbor_tour(tsp)))

        if call_args.call_sa:
            best_tour, current_tour = sa(tsp)
            print("SA LENGTH:                {}".format(best_tour[1]))

    print("")
    del(tsp)


def main():
    call_args = parser.parse_args()

    if call_args.experiment:
        import pickle
        from experiments import testar_parametros_paralelo_por_arquivo
        print(call_args.tsp_queue)
        r = testar_parametros_paralelo_por_arquivo(list(glean_tsp_files(call_args.tsp_queue)))
        binary_file = open(call_args.tsp_queue[0] + '/my_pickled_results.bin', mode='wb')
        pickle.dump(r, binary_file)
        binary_file.close()
        import os
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.1, 440))
        # r = pickle.loads(open('my_pickled_results.bin', mode='rb').read())
        # pprint(r)
    else:
        for tsp_path in glean_tsp_files(call_args.tsp_queue):
            process_from_tsp_path(call_args, tsp_path)


if __name__ == "__main__":
    main()
