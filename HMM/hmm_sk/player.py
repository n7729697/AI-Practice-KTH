#!/usr/bin/env python3

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random
import sys
import math
import numpy as np

epsilon = sys.float_info.epsilon

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
    pi = pi[0]
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
        #print("t: ", t)
        #print("alpha_t: ", alpha_t)
        alpha_T[t] = 1/(alpha_t + epsilon)

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

    for i in range(len(A[0])):
        gamma_probs[len(O)- 1][i] = alpha_list[len(O)-1][i]

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

    a = [[0 for i in range(len(A[0]))] for j in range(len(A[0]))]
    b = [[0 for i in range(len(B[0]))] for j in range(len(B))]
    pi = [0 for i in range(len(A[0]))]

    for i in range(len(A[0])):
        pi[i] = gamma_list[0][i]

    # re-estimate matrix A 
    for i in range(len(A[0])):
        denom = 0
        if len(O) == 1:
            denom += gamma_list[0][i]
        for t in range(len(O)-1):
            denom += gamma_list[t][i]
        for j in range(len(A[0])):
            numer = 0
            for t in range(len(O)-1):
                numer += si_list[t][i][j]
            a[i][j] = numer / (denom+epsilon)

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
            b[i][j] = numer/(denom+epsilon)
    
    return a,b,[pi]

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
        log_likelihood -= math.log(alpha_T[t])
    return log_likelihood

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
    # pi: new initial probabilities
    
    old_log_likelihood = float('-inf')
    convergence = False

    for i in range(max_iter):
        alpha_list, alpha_T = forward(O, A, B, pi)
        beta_list = backward(O, A, B, alpha_T)
        si_list, gamma_list = si_compute_gamma(O, A, B, alpha_list, beta_list)
        A, B, pi = re_estimate(O, A, B, si_list, gamma_list)

        log_likelihood = compute_log_likelihood(O, alpha_T)
        if log_likelihood <= old_log_likelihood:
            convergence = True
            break
        old_log_likelihood = log_likelihood


    return A, B, pi, convergence

def transpose(M):
    # transpose the B col to real col
    return [list(i) for i in zip(*M)]

def matrix_multiplication(A, B):
    return [[sum(a * b for a, b in zip(a_row, b_col)) for b_col in zip(*B)] for a_row in A]
def dot_prod(matrix_a, matrix_b):
    return [[a * b for a, b in zip(matrix_a[0], matrix_b)]] 

def  most_prob_next(model, obs):
    A=model.A
    # print("model.B", model.B)
    B=transpose(model.B)
    # print("A", A[0])
    pi=model.PI
    
    alpha = dot_prod(pi, B[obs[0]])

    for e in obs[1:]:
        alpha = matrix_multiplication(alpha, A)
        alpha = dot_prod(alpha, B[e])

    return sum(alpha[0])

def generate_row_stochastic(size):
    M = [(1 / size) + np.random.rand() / 1000 for _ in range(size)]
    s = sum(M)
    return [m / s for m in M]

class HMModel:
    def __init__(self, species, emissions):
        self.PI = [generate_row_stochastic(species)]
        self.A = [generate_row_stochastic(species) for _ in range(species)]
        self.B = [generate_row_stochastic(emissions) for _ in range(species)]

    def set_A(self, A):
        self.A = A

    def set_B(self, B):
        self.B = B

    def set_PI(self, PI):
        self.PI = PI

class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        self.models = [HMModel(1, N_EMISSIONS) for _ in range(N_SPECIES)]
        self.fishes_obs = [(i,[]) for i in range(N_FISH)]
        self.obs_now = []

    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """

        # print(step)

        # Update the observations of each fish
        for i in range(len(self.fishes_obs)):
            if observations[i] is not None:
                self.fishes_obs[i][1].append(observations[i])
                
        # Viterbi algorithm
        if step < 10:
            # No wasting chance
            return None
        else:
            # Guess the most likely fish
            fish_id, obs = self.fishes_obs.pop()
            fish_type = 0
            max = 0
            for model, idx in zip(self.models, range(N_SPECIES)):
                m = most_prob_next(model, obs)
                if m>max:
                    max = m
                    fish_type = idx
            self.obs_now = obs
            
            return fish_id, fish_type

    def reveal(self, correct, fish_id, true_type):
        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """

        # print("Guess was correct: {}".format(correct))
        # print("Fish id: {}".format(fish_id))
        # print("True type: {}".format(true_type))
        
        if not correct:
            A, B, PI, _ = baum_welch(self.obs_now, self.models[true_type].A, self.models[true_type].B, self.models[true_type].PI, 10)
            self.models[true_type].set_A(A)
            self.models[true_type].set_B(B)
            self.models[true_type].set_PI(PI)