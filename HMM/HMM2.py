import sys

def read_matrix():
    # Read the matrix from stdin
    matrix = []
    # Read the first line and split it by spaces
    line = sys.stdin.readline().split()
    n, m = int(line[0]), int(line[1])
    for i in range(n):
        # Read the next line and split it by spaces
        matrix.append([])
        for j in range(m):
            matrix[i].append(float(line[2 + i * m + j]))
    return matrix

def read_int():    
    # Read the first line and split it by spaces
    line = sys.stdin.readline().split()
    result = [int(i) for i in line]
    return result[1:]

def get_column(matrix, col):
    return [row[col] for row in matrix]


def element_multiplication(A, B):
    # Multiply two matrices by elements    
    return [i*j for i,j in zip(A,B)]

def viterbi(O, A, B, delta, max_id):
    # viterbi algorithm
    # O: observe sequence
    # A: transition matrix
    # B: emission matrix
    # id: id list for tracking back the state
    
    if len(O) == 0:
        # track back the possible hidden states
        state_list = []
        last_state = delta.index(max(delta))
        state_list.append(last_state)
        for i in range(len(max_id) - 1, 0, -1):
            state_list.insert(0, max_id[i][last_state])
            last_state = max_id[i][last_state]
        print(' '.join([str(x) for x in state_list]))
        return 0
    
    all = [[delta[pre] * A[pre][curr] * B[curr][O[0]] for pre in range(len(A[0]))] for curr in range(len(A[0]))]
    possible_delta = [max(probabilities_curr_st) for probabilities_curr_st in all]
    print(possible_delta)
    max_id.append([max_idx.index(possible_delta[i]) for i, max_idx in enumerate(all)])
    viterbi(O[1:], A, B, possible_delta, max_id)


transition_matrix = read_matrix()
emission_matrix = read_matrix()
initial_state_prob_dist = read_matrix()
observe_sequence = read_int()

first_delta = element_multiplication(initial_state_prob_dist[0], get_column(emission_matrix, observe_sequence[0]))
max_id_initial = [[None] * len(transition_matrix[0])]

viterbi(observe_sequence[1:], transition_matrix, emission_matrix, first_delta, max_id_initial)