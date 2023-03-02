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

def backward(O_rev, A, B, end_alpha):
    # backward algorithm
    # O: reversed observe sequence
    # A: transition matrix
    # B: emission matrix
    # pi: initial state probabilities
    
    # alpha values stored during forward possibilities
    back_probs = [[0 for i in range(len(A[0])+1)] for j in range(len(O_rev))] 
    for t in range(len(A[0])):
        beta_temp_list = []
        for i in range(len(A[0])):     
            if t == 0:
                beta = end_alpha[t]
                beta_temp_list.append(beta)
            else:
                sum_term = 0
                for j in range(len(A[0])):     # from state
                    sum_term += back_probs[t-1][j] * A[i][j] * B[j][O_rev[t-1]]
                beta_temp_list.append(sum_term)
        
        back_probs.append(beta_temp_list)
    return back_probs

transition_matrix = read_matrix()
emission_matrix = read_matrix()
initial_state_prob_dist = read_matrix()
observe_sequence = read_int()

first_delta = element_multiplication(initial_state_prob_dist[0], get_column(emission_matrix, observe_sequence[0]))
max_id_initial = [[None] * len(transition_matrix[0])]

backward(observe_sequence[::-1], transition_matrix, emission_matrix, first_delta, max_id_initial)