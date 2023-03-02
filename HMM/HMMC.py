from HMM3 import baum_welch
from HMM3 import read_matrix
from HMM3 import read_int
from HMM3 import print_matrix

# 1000 total observations
# For 169 observations or more converges after 1000 iterations

# 10000 total observations
# For 81 observation or more coverges after 532 iterations



def main():
    transition_matrix = read_matrix()
    emission_matrix = read_matrix()
    initial_state_prob_dist = read_matrix()
    observe_sequence = read_int()

    A, B, iter = baum_welch(observe_sequence, transition_matrix, emission_matrix, initial_state_prob_dist[0], 10000)
    print("iterations: ", iter)
    print_matrix(A)
    print_matrix(B)

    """
    r = [i for i in range(160, 170, 1)]
    save = []
    for i in r:
        
        A, B, iter = baum_welch(observe_sequence[:i], transition_matrix, emission_matrix, initial_state_prob_dist[0], 1000)
        save.append((iter, i))
        print("Observations: ", i, "iter: ", iter)
    print(save)
    """
if __name__ == '__main__':
    main()