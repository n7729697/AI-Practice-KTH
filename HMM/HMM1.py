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

def forward(O, A, B, alpha):
    # forward algorithm
    # O: observe sequence
    # A: transition matrix
    # B: emission matrix
    
    if len(O) == 0:
        print(sum(alpha))
        return 0
    
    first_sum = [sum(element_multiplication(alpha, get_column(A, i))) for i in range(len(A[0]))]
    current_alpha = element_multiplication(first_sum, get_column(B, O[0]))
    forward(O[1:], A, B, current_alpha)


transition_matrix = read_matrix()
emission_matrix = read_matrix()
initial_state_prob_dist = read_matrix()
observe_sequence = read_int()

first_alpha = element_multiplication(initial_state_prob_dist[0], get_column(emission_matrix, observe_sequence[0]))
forward(observe_sequence[1:], transition_matrix, emission_matrix, first_alpha)