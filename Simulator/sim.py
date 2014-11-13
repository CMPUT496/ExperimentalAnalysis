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

logFile = open("LogFile.txt", "w")

class LineConfig():
    def __init__(self):
        self.ticks = random.randint(0,2)
        #self.fractions = random.randint(0,5)
        self.hints = random.randint(0,1)
        self.target_rep = random.randint(0,1)
        self.label_rep = random.randint(0,1)

    def get_ticks(self):
        return self.ticks

    # def getFraction(self):
    #     return self.fractions

    def get_hints(self):
        return self.hints

    def get_target(self):
        return self.target_rep

    def get_label(self):
        return self.label_rep

def distance(arm, student):
    # calculate distance
    dist = 0.0    # offset
    dist += 0.1 * (numpy.absolute(arm.getTicks() - student.getTicks()))
    # dist += 0.08 * (numpy.absolute(arm.getFraction() - student.getFraction()))
    dist += 0.05 * (numpy.absolute(arm.getHints() - student.getHints()))
    dist += 0.5 * (numpy.absolute(arm.getTarget() - student.getTarget()))
    dist += 0.5 * (numpy.absolute(arm.getLabel() - student.getLabel()))
    print "Distance: %f" %(dist)
    return dist

def probability(dist):
    # calculate probability of success based on distance
    # this is the distribution function
    prob = numpy.exp(0-dist)
    print "Probability: %f" %(prob)
    return prob

def reward(prob):
    if random.random() <= prob:
        return 1    # pass
    else:
        return 0    # fail

# def getStudent():
#     # randomly returns a student config vector
#     student = LineConfig()
#     print "Student: <%d, %d, %d, %d, %d>" %(student.getTicks(),
#             student.getFraction(), student.getHints(), student.getLabel(),
#             student.getTarget())
#     return student

def getStudent():
    # Picks a type of student based on same probability
    # 20%: visual, 40%: non-visual, 20%: independant, 20%: dependant
    studType = random.randint(0,9)
    if(studType < 2): 
        student = Student(random.randint(0,2), 0, 0, 0, "Visual") # Visual
    elif(studType <= 5):
        student = Student(0, random.randint(0,1), 1, 1, "Non-visual") # Non-visual
    elif(studType <= 7):
        student = Student(2, 0, random.randint(0,1), 0, "Indepentant") # Indepentant
    else:
        student = Student(1, 1, 1, random.randint(0,1), "Dependant") # Dependant

    return student


def log_results(student, probability, result):
    if(resust == 1):
        res = "PASS"
    else:
        res = "FAIL"
    log = "%s, lambda:%f <%d, %d, %d, %d>, %d\%, %s", %(student.get_name(), student.get_lambda, student.get_ticks(), student.get_hints(), student.get_target(), student.get_label, res)
    return

def simulate(config):
    arm = LineConfig()
    print "ARM:     <%d, %d, %d, %d, %d>" %(arm.getTicks(),
            arm.getFraction(), arm.getHints(), arm.getLabel(),
            arm.getTarget())
    student = getStudent()
    dist = distance(arm, student)
    prob = probability(dist)
    rew = reward(prob)
<<<<<<< HEAD
    # log_results(student, probability, result)
=======
    # log_results(student, question, attempt)
    print "Reward: %d" %(rew)
>>>>>>> cce53e1541baaba3c27b04d2ad73ceac08e92281
    return rew

