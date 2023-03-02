import sys
import math
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

def print_matrix(matrix):
    output = ""
    # print size of matrix
    output += str(len(matrix)) + " " + str(len(matrix[0])) + " "
    # print matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            output += str(matrix[i][j]) + " "
    print(output)

def forward(O, A, B, pi):
    # forward algorithm
    # INPUT
    # O: observe sequence
    # A: transition matrix
    # B: emission matrix
    # pi: initial state probabilities
    # OUTPUT
    # fwd_probs: is the alpha matrix contains every alpha 
    # alpha_T: is the coefficient used to scale the alpha which is the sum of alpha
    #         aims to erase the super small floats

    forward_probs =[[0.0 for i in range(len(A[0]))] for j in range(len(O))]
    alpha_T = [0.0 for i in range(len(O))]
    for t in range(len(O)):
        alpha_t = 0.0
        alpha_ij = 0.0
        for i in range(len(A[0])):
            if t == 0:
                forward_probs[t][i] = pi[i] * B[i][O[t]]
                alpha_ij += pi[i] * B[i][O[t]]
                alpha_t = alpha_ij
            else:
                alpha_ij = 0.0
                for j in range(len(A[0])):
                    alpha_ij += forward_probs[t-1][j] * A[j][i] * B[i][O[t]]
                forward_probs[t][i] = alpha_ij
                alpha_t += alpha_ij 
        
        # alpha_T is the reciprocal of alpha_t (alpha at time t)
        alpha_T[t] = 1/alpha_t 

        for k in range(len(A[0])):
            forward_probs[t][k] = alpha_T[t] * forward_probs[t][k]
    
    return forward_probs, alpha_T

def backward(O, A, B, alpha_T):
    # backward algorithm
    # INPUT
    # O: observe sequence
    # A: transition matrix
    # B: emission matrix
    # alpha_T: the coefficient used to scale the alpha which is the sum of alpha
    #          aims to erase the super small floats
    O_reversed = O[::-1]
    alpha_T_rev = alpha_T[::-1]

    # beta values stored during backward possibilities
    backward_probs = [[0 for i in range(len(A[0]))] for j in range(len(O_reversed))] 
    for t in range(len(O_reversed)):
        beta_t = 0
        for i in range(len(A[0])):
            if t == 0:
                beta_t = alpha_T_rev[t]
                backward_probs[t][i] = beta_t
            else:
                beta_t = 0
                for j in range(len(A[0])):
                    beta_t += backward_probs[t-1][j] * A[i][j] * B[j][O_reversed[t-1]]
                backward_probs[t][i] = beta_t
    
        # not the end states
        if t > 0:
            for k in range(len(A[0])):
                backward_probs[t][k] = alpha_T_rev[t] * backward_probs[t][k] 
            
    return backward_probs[::-1]

def si_compute_gamma(O, A, B, alpha_list, beta_list):
    # di-gamma and gamma function
    # INPUT
    # O: observe sequence
    # A: transition matrix
    # B: emission matrix
    # alpha_list: list of all alpha
    # beta_list: list of all beta 
    # OUTPUT
    # gamma_list is the list of di-gamma function 
    # gamma_T is the list of gamma function

    si_probs = [[[0 for i in range(len(A[0]))] for j in range(len(A[0]))] for k in range(len(O)-1)]
    gamma_probs = [[0 for i in range(len(A[0]))] for j in range(len(O))]

    for t in range(len(O)-1):
        for i in range(len(A[0])):

            gamma_t = 0
            for j in range(len(A[0])):
                gamma_t += alpha_list[t][i] * A[i][j] * B[j][O[t+1]] * beta_list[t + 1][j]
                si_probs[t][i][j] = alpha_list[t][i] * A[i][j] * B[j][O[t+1]] * beta_list[t + 1][j]
            gamma_probs[t][i] = gamma_t

    for k in range(len(A[0])):
        gamma_probs[t+1][k] = alpha_list[t+1][k]

    return si_probs, gamma_probs

def re_estimate(O, A, B, si_list, gamma_list):
    # re-estimate the alpha and beta function
    # INPUT
    # O: observe sequence
    # A: transition matrix
    # B: emission matrix
    # si_list: list of all gamma_ij
    # gamma_list: list of all gamma_t 
    # OUTPUT
    # a_list is the list of new alpha
    # b_list is the list of new beta

    a=[[0 for i in range(len(A[0]))] for j in range(len(A[0]))]
    b=[[0 for i in range(len(B[0]))] for j in range(len(B))]
    # re-estimate matrix A 
    for i in range(len(A[0])):
        denom = 0
        for t in range(len(O)-1):
            denom += gamma_list[t][i]
        for j in range(len(A[0])):
            numer = 0
            for t in range(len(O)-1):
                numer += si_list[t][i][j]
            a[i][j] = numer / denom

    # re-estimate matrix B
    for i in range(len(A[0])):
        denom = 0
        for t in range(len(O)):
            denom += gamma_list[t][i]
        for j in range(len(B[0])):
            numer = 0
            for t in range(len(O)):
                if O[t] == j:
                    numer += gamma_list[t][i]
            b[i][j] = numer/denom
    
    return a,b

def compute_log_likelihood(O, alpha_T):
    # compute the log likelihood
    # INPUT
    # O: observe sequence
    # alpha_T: the coefficient used to scale the alpha which is the sum of alpha
    #          aims to erase the super small floats
    # OUTPUT
    # log_likelihood: the log likelihood of the observe sequence

    log_likelihood = 0
    for t in range(len(O)):
        log_likelihood += math.log(alpha_T[t])
    return -log_likelihood

def baum_welch(O, A, B, pi, max_iter):
    # baum-welch algorithm
    # INPUT
    # O: observe sequence
    # A: transition matrix
    # B: emission matrix
    # pi: initial state distribution
    # max_iter: maximum iteration
    # OUTPUT
    # A: new transition matrix
    # B: new emission matrix
    
    old_log_likelihood = float('-inf')
    iter = 0
    for i in range(max_iter):
        iter += 1
        alpha_list, alpha_T = forward(O, A, B, pi)
        beta_list = backward(O, A, B, alpha_T)
        si_list, gamma_list = si_compute_gamma(O, A, B, alpha_list, beta_list)
        A, B = re_estimate(O, A, B, si_list, gamma_list)

        log_likelihood = compute_log_likelihood(O, alpha_T)
        if log_likelihood <= old_log_likelihood:
            break
        old_log_likelihood = log_likelihood

    # Round and return
    A = [[round(x, 6) for x in row] for row in A]
    B = [[round(x, 6) for x in row] for row in B]
    return A, B, iter


def main():
    transition_matrix = read_matrix()
    emission_matrix = read_matrix()
    initial_state_prob_dist = read_matrix()
    observe_sequence = read_int()
    
    A, B = baum_welch(observe_sequence, transition_matrix, emission_matrix, initial_state_prob_dist[0], 10000)
    print_matrix(A)
    print_matrix(B)

    #alpha_list,alpha_T = forward(observe_sequence, transition_matrix, emission_matrix, initial_state_prob_dist[0])
    #beta_list = backward(observe_sequence, transition_matrix, emission_matrix, alpha_T)
    #gamma_list, gamma_T = si_compute_gamma(observe_sequence, transition_matrix, emission_matrix, alpha_list, beta_list)
    #print(gamma_list)

if __name__ == "__main__":
    main()