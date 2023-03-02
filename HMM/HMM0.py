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



def print_matrix(matrix):
    output = ""
    # print size of matrix
    output += str(len(matrix)) + " " + str(len(matrix[0])) + " "
    # print matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            output += str(matrix[i][j]) + " "
    print(output)


def matrix_multiplication(A, B):
    # Multiply two matrices
    C = []
    for i in range(len(A)):
        C.append([])
        for j in range(len(B[0])):
            C[i].append(0)
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
    return C


# Read 3 matrices from stdin
transition_matrix = read_matrix()
emission_matrix = read_matrix()
initial_state_prob_dist = read_matrix()

emission_probability_distribution = matrix_multiplication(initial_state_prob_dist, matrix_multiplication(transition_matrix, emission_matrix))

print_matrix(emission_probability_distribution)

