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

def element_wise_product(A, B):
    C = []
    for i in range(len(A)):
        C.append(A[i] * B[i])
    return C

def scalar_vector_product(scalar, vector):
    C = []
    for i in range(len(vector)):
        C.append(0)
        C[i] = scalar * vector[i]
    return C
           
def get_column(matrix, column):
    C = []
    for i in range(len(matrix)):
        C.append(matrix[i][column])
    return C


# Read 3 matrices from stdin
transition_matrix = read_matrix()
emission_matrix = read_matrix()
initial_state_prob_dist = read_matrix()
input = sys.stdin.readline().split()
sequence_of_emissions = [int(i) for i in input[1:int(input[0]) + 2]]

# calculate probability of the given sequence as a single scalar
a = element_wise_product(initial_state_prob_dist[0], get_column(emission_matrix, sequence_of_emissions[0]))

for e in sequence_of_emissions[1:]:
    new_a = [0]*len(a)
    for i, s in enumerate(a):
        for j in range(len(new_a)):
            new_a[j] += scalar_vector_product(s, transition_matrix[:][i])[j]

    new_a = element_wise_product(new_a, get_column(emission_matrix, e))
    a = new_a
print(sum(a))
