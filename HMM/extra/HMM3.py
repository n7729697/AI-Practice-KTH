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

def forward_prob(O, states, initial_prob, trans_prob, emm_prob, end_st):
    forward = []
    for i, observation_i in enumerate(O):
        f_current = [0.0 for i in range(len(trans_prob))]
        for s in states:
            if i == 0:
                # base case for the forward part
                prev_f_sum = initial_prob[s]
            else:
                prev_f_sum = sum(f_prev[k] * trans_prob[k][s] for k in states)
           
            f_current[s] = emm_prob[s][observation_i] * prev_f_sum
            #print(f_current[s])
        forward.append(f_current)
        f_prev = f_current

    p_forward = sum(f_current[k] * trans_prob[k][end_st] for k in states)
    return forward, p_forward


def backward_prob(O, states, initial_prob, trans_prob, emm_prob, end_st):
    # Backward part of the algorithm
    backward = []
    for i, observation_i_plus in enumerate(reversed(O[1:] + [None,])):
        b_current = [0.0 for i in range(len(trans_prob))]
        for s in states:
            if i == 0:
                # base case for backward part
                b_current[s] = trans_prob[s][end_st]
            else:
                b_current[s] = sum(trans_prob[s][l] * emm_prob[l][observation_i_plus] * b_prev[l] for l in states)
        backward.insert(0,b_current)
        b_prev = b_current

    p_backward = sum(initial_prob[l] * emm_prob[l][O[0]] * b_current[l] for l in states)

    return backward, p_backward


# si probability
def si_prob(O, states, trans_prob, emm_prob, forward, backward, f_sum):

    si_probs = [[[0 for k in range(len(states))] for j in range(len(O) - 1)] for i in range(len(states))]

    for t in range(len(O) - 1):
        for i in range(len(states)):
            for j in range(len(states)):
                #alpha_list[t][i] * A[i][j] * B[j][O[t+1]] * beta_list[t + 1][j]
                si_probs[t,i,j] = ( forward[t,i] * backward[t+1,j] * trans_prob[i,j] * emm_prob[j,O[t+1]] ) / f_sum

    return si_probs


# Gamma probabilities
def gamma_prob(O, states, forward, backward, f_sum):

    gamma_probs = [[0 for j in range(len(0))] for i in range(len(states))]

    for i in range(len(O)):
        for j in range(len(states)):
            gamma_probs[j,i] = ( forward[j,i] * backward[j,i] ) / f_sum

transition_matrix = read_matrix()
emission_matrix = read_matrix()
initial_state_prob_dist = read_matrix()
observe_sequence = read_int()
states = [i for i in range(len(transition_matrix))]

forward, f_sum = forward_prob(observe_sequence, states, initial_state_prob_dist[0], transition_matrix, emission_matrix, len(transition_matrix)-1)
backward, b_sum = backward_prob(observe_sequence, states, initial_state_prob_dist[0], transition_matrix, emission_matrix, len(transition_matrix)-1)

sig = si_prob(observe_sequence, states, transition_matrix, emission_matrix, forward, backward, f_sum)
gamma = gamma_prob(observe_sequence, states, forward, backward, f_sum)
print(gamma)

