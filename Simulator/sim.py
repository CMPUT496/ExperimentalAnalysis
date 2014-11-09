# Alg selects C_t
# Sim selects S_t at random
# Compute d(S_t, C_t)
# Compute P(S_t, C_t)
# Sample Rt ~ Bernoulli(P(S_t, C_t))
#
# C = <C_1 , ... , C_n >
# S = <C_1 , ... , C_n >
# D(s,c) = distance

import numpy
import random

class LineConfig():
    def __init__():
        ticks = random.randint(0,2)
        fractions = random.randint(0,5)
        hints = random.randint(0,1)
        target_rep = random.randint(0,1)
        label_rep = random.randint(0,1)  

    def getTicks():
        return this.ticks

    def getFractions():
        return this.fractions

    def getHints():
        return this.hints

    def getTarget():
        return this.target_rep

    def getLabel():
        return this.label_rep

def distance(config, student):
    # calculate distance
    return distance

def probability(distance):
    # calculate probability of success based on distance
    # this is the distribution function
    probability = e^(-distance)
    return probability

def getStudent():
    # randomly returns a student config vector
    return student

def log_results(student, question, attempt):
    return

def simulate(config):
    student = getStudent()
    dist = distance(config, student)
    prob = probability(distance)
    reward = rewardBasedOnProb(prob)
    log_results(student, question, attempt)
    return reward
 


