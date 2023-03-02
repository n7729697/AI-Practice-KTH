Artificial Intelligence DD2380

Fishing derby: Hidden Markov Models
===
# Running on Ubuntu (Xuezhi)
```
python3 HMM0.py < test0.in
python3 HMM1.py < test1.in
python3 HMMx.py < testx.in
```
## Requirements
### GRADE LEVEL E AND D
Finish HMM0~3
The problem can be found on Kattis:

HMM0:https://kth.kattis.com/problems/kth.ai.hmm0

HMM1:https://kth.kattis.com/problems/kth.ai.hmm1

HMM2:https://kth.kattis.com/problems/kth.ai.hmm2

HMM3:https://kth.kattis.com/problems/kth.ai.hmm3

### GRADE LEVEL C
This part extends the HMM implementation by more empirical investigations. Given your complete
Baum-Welch algorithm, you are supposed to both investigate different properties of its performance
and to test different parameter settings. To this end, we provide you with an HMM model which can
be used for data generation. Thus, this assignment focuses on theoretical and empirical understand-
ing of HMMs.

Your task is to train an HMM on a varying number of these observations with the help of your
Baum-Welch implementation.

Q7: Does the algorithm converge? How many observations do you need for the algorithm to con-
verge? How can you define convergence?

1000 total observations
For 169 observations or more converges after 1000 iterations
10000 total observations
For 81 observation or more coverges after 532 iterations

Q8: Train an HMM with the same parameter dimensions as above, i.e. A is a 3x3 matrix
etc. The initialization is left up to you.
How close do you get to the parameters above, i.e. how close do you get to the generating
parameters in Eq. 3.1? What is the problem when it comes to estimating the distance between
these matrices? How can you solve these issues?

Q9: Train an HMM with different numbers of hidden states.
What happens if you use more or less than 3 hidden states? Why?
Are three hidden states and four observations the best choice? If not, why? How can you deter-
mine the optimal setting? How does this depend on the amount of data you have?

Q10: Initialize your Baum-Welch algorithm with a uniform distribution. How does this
affect the learning?
Initialize your Baum-Welch algorithm with a diagonal A matrix and π = [0, 0, 1]. How does this
affect the learning?
Initialize your Baum-Welch algorithm with a matrices that are close to the solution. How does
this affect the learning?


### GRADE LEVEL B AND A
In this part of the assignment you will implement an agent that can classify fish. The aim is to get a
deep understanding of Hidden Markov Models and for you to show that you can make use of them to
solve a less structured problem. You will practice identifying the number of states, observations, etc.
You will have to learn the HMM model and use it for classification.
In this part of fishing derby, you play a single-player game and observe the movement of different
fish swimming in the water. There are 7 fish species, and each species has its own swimming patterns
and behave differently, unknown to the player. You have to observe the swimming patterns of the fish
and identify their types.

This assignment requires a thorough understanding of HMMs. Therefore it is highly recommended
to have a look at the Stamp tutorial (A Revealing Introduction to Hidden Markov Models by Mark
Stamp)! It will give you more details about numerically stable computations and other important
factors for your implementation.

A basic code skeleton is provided for you in Python 3. The program is fully functional as it is provided,
but the program never makes any guesses. The code can be downloaded from the attachments on the
Kattis page of the game, or can be downloaded directly by the following link: https://kth.kattis.com/problems/kth.ai.hmm/file/statement/attachments/fishingderby_hmm.zip

You find valuable information regarding the dynamics of the game on Kattis: https://kth.kattis.com/problems/kth.ai.hmm

The fish and the environments provided for testing are different from the ones that are used in
Kattis.

You should modify the PlayerControllerHMM class in the file player.py. You may also create any
number of new classes and files. The files included in the skeleton may be modified locally, but keep
in mind that they will be overwritten on Kattis (except for player.py).
Your interface with the program environment is the PlayerControllerHMM class. Avoid using stdin
and stdout. (Instead, use stderr for debugging.)

The Kattis server uses Python 3 with PyPy compiler, which unfortunately is not supported by the
provided skeleton (due to the graphical user interface libraries). Although the numpy library is in-
cluded in this part of the assignment on Kattis, it would be important to keep in mind that code
written on python lists would actually run faster than a code that uses numpy.
For more details, check out the problem description on Kattis webpage.

You are required to have a Kattis score of at least 250. However, keep in mind that the goal of this
exercise is not to optimize your code toward Kattis, but instead that you get an understanding of the
theory behind HMMs. Therefore, you also have to be able to reason about your solution and answer
theoretical questions regarding HMMs for obtaining your grade.