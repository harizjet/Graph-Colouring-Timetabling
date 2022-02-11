from ConstructiveHeuristics.largest_degree import Constructive_Heuristics
from Utils import plotting


if __name__ == '__main__':

    nodes = [input().split(' ') for _ in range(int(input()))]
    edges = [input() for _ in range(int(input()))]

    roulette_ld = Constructive_Heuristics(nodes, edges, pick_random=False)
    random_ld = Constructive_Heuristics(nodes, edges, pick_random=True)

    res_roulette_ld = roulette_ld.sampling_result(n=3000)
    res_random_ld = random_ld.sampling_result(n=3000)

    best_roulette_ld = min(res_roulette_ld[4])
    avg_roulette_ld = sum(res_roulette_ld[4]) / len(res_roulette_ld[4])
    worst_roulette_ld = max(res_roulette_ld[4])

    best_random_ld = min(res_random_ld[4])
    avg_random_ld = sum(res_random_ld[4]) / len(res_random_ld[4])
    worst_random_ld = max(res_random_ld[4])
    
    plotting.plot_comparison_result(
        res_roulette_ld[4], "Roulette Largest Degree", best_roulette_ld, avg_roulette_ld, worst_roulette_ld,
        res_random_ld[4], "Random Largest Degree", best_random_ld, avg_random_ld, worst_random_ld
        )
    
    plotting.plot_table_result_stud_pan(res_roulette_ld[0], res_roulette_ld[1], res_roulette_ld[3])

    plotting.plot_table_result_pans_sv(res_roulette_ld[1], res_roulette_ld[2], res_roulette_ld[3])

    print(res_roulette_ld[0])
    print(avg_roulette_ld, avg_random_ld, sep='\n')
