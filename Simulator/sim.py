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
    def __init__(self):
        self.ticks = random.randint(0,2)
        self.fractions = random.randint(0,5)
        self.hints = random.randint(0,1)
        self.target_rep = random.randint(0,1)
        self.label_rep = random.randint(0,1)  

    def getTicks(self):
        return self.ticks

    def getFractions(self):
        return self.fractions

    def getHints(self):
        return self.hints

    def getTarget(self):
        return self.target_rep

    def getLabel(self):
        return self.label_rep

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
    student = LineConfig()
    print student.getTicks() 
    print student.getFractions() 
    print student.getHints() 
    print student.getLabel() 
    print student.getTarget()
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
 
getStudent()


