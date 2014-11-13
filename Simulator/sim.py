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
    """
    LineConfig is a representation of a number line configuration.

    Variables:
        ticks: [0, 2] represents the number of ticks on the number line
        fractison: [0, 5] represents the difficulty of fractions
        hints: [0, 1] boolean, represents if there are hints or not
        target: [0, 1] represents target representation (either pie chart or symbolic)
        label: [0, 1] represents label representation (either pie chart or symbolic)
    """

    def __init__(self, ticks, fractions, hints, target, label):
        self.ticks = ticks
        self.fractions = fractions
        self.hints = hints
        self.target = target
        #self.ticks = random.randint(0,2)
        #self.fractions = random.randint(0,5)
        #self.hints = random.randint(0,1)
        #self.target_rep = random.randint(0,1)
        #self.label_rep = random.randint(0,1)

    def getTicks(self):
        return self.ticks

    def getFraction(self):
        return self.fractions

    def getHints(self):
        return self.hints

    def getTarget(self):
        return self.target

    def getLabel(self):
        return self.label


class Student(LineConfig):
    """
    Student is a representation of student's preferred configuration,
    a lambda representing how *good* a student is (inversely), and the name
    of the type of student for logging purposes

    Student inherits from LineConfig
    """
    def __init__(self, ticks, fractions, hints, target, label, name):
        # call line_config
        LineConfig.__init__(self, ticks, fractions, hints, target, label)
        self.s_lambda = 0
        self.name = name

    def get_lambda(self):
        return self.s_lambda

    def get_name(self):
        return self.name


def distance(arm, student):
    # calculate distance
    dist = 0.0    # offset
    dist += 0.1 * (numpy.absolute(arm.getTicks() - student.getTicks()))
    dist += 0.08 * (numpy.absolute(arm.getFraction() - student.getFraction()))
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

def getStudent():
    # randomly returns a student config vector
    # generate ticks
    ticks = numpy.random.normal(1, 1)
    if ticks >= 2:
        ticks = 2
    elif ticks <= 0:
        ticks = 0
    else:
        ticks = 1

    # generate fractions
    fractions = numpy.random.randint(0, 6)

    # gemerate hints
    hints = 0
    if (random.random() <= 0.3):
        hints = 1

    # gemerate hints
    target = 0
    if (random.random() <= 0.5):
        target = 1

    # gemerate hints
    label = 0
    if (random.random() <= 0.5):
        label = 1

    s = numpy.array([ticks, fractions, hints, target, label])

    student = LineConfig()
    print "Student: <%d, %d, %d, %d, %d>" %(student.getTicks(),
            student.getFraction(), student.getHints(), student.getLabel(),
            student.getTarget())
    return student

def log_results(student, question, attempt):
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
    # log_results(student, question, attempt)
    print "Reward: %d" %(rew)
    return rew
