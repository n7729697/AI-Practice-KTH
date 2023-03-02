# Reinforcement Learning
## 1

Random agent

## 2
### 2.2
What do you observe? Is your agent capable of achieving the maximum score of 11 (if not,
please explain why)
The agent rarly gets 11 points. We dont run any type of exploring for this, and sole choose the option that has been the best in previous runs.

## 3
We use anneling to randomly do random moves, this hopefully improves the overall score, but not 100% to do so.
With the use of an interval we can do a lot of exploring in the begining and then switch over to exploitation

## 4
Never catching any Fish, including the King Fish: plus for steps minus for rest
Taking the shortest path to catch the King Fish: (Depends on the meaning of this) plus for king crab and minus for rest (Thought 0 for jelly would work, didnt)

## 5
alpha = low, to give learning
gamma = mid to high, to give more long term rewards