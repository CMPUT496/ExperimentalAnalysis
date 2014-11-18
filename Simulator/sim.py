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
import pdb

class LineConfig():
    """
    LineConfig is a representation of a number line configuration.

    Variables:
        ticks: [0, 2] represents the number of ticks on the number line
        hints: [0, 1] boolean, represents if there are hints or not
        target: [0, 1] represents target representation (either pie chart or symbolic)
        label: [0, 1] represents label representation (either pie chart or symbolic)
    """

    def __init__(self, ticks, hints, target, label):
        self.ticks = ticks
        self.hints = hints
        self.target = target
        self.label = label

    def get_ticks(self):
        return self.ticks

    def get_hints(self):
        return self.hints

    def get_target(self):
        return self.target

    def get_label(self):
        return self.label

    def __str__(self):
        return "<%d, %d, %d, %d>" %(self.ticks, self.hints, self.target, self.label)


class Student(LineConfig):
    """
    Student is a representation of student's preferred configuration,
    a lambda representing how *good* a student is (inversely), and the name
    of the type of student for logging purposes

    Student inherits from LineConfig
    """
    def __init__(self, ticks, hints, target, label, name, prob):
        # call line_config
        LineConfig.__init__(self, ticks, hints, target, label)
        self.s_lambda = numpy.random.normal(1, 0.1)
        self.name = name

    def get_lambda(self):
        return self.s_lambda

    def get_name(self):
        return self.name

    def get_prob(self):
        return self.prob

def distance(arm, student):
    # calculate distance
    dist = 0.0    # offset
    dist += 0.1 * (numpy.absolute(arm.get_ticks() - student.get_ticks()))
    dist += 0.05 * (numpy.absolute(arm.get_hints() - student.get_hints()))
    dist += 0.5 * (numpy.absolute(arm.get_target() - student.get_target()))
    dist += 0.5 * (numpy.absolute(arm.get_label() - student.get_label()))
    dist *= student.get_lambda()
    return dist

def probability(dist):
    # calculate probability of success based on distance
    # this is the distribution function
    prob = numpy.exp(0-dist)
    #print "Probability: %f" %(prob)
    return prob

def reward(prob):
    if random.random() <= prob:
        return 1    # pass
    else:
        return 0    # fail

def get_student():
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

def pick_student(students):
    num = random.randint(0,9)
    if(num < 2):
        return students[0]
    elif(num < 6):
        return students[1]
    elif(num < 8):
        return students[2]
    else:
        return students[3]

def get_student_list(log_file):
    s_list = list()
    s_list.append(Student(random.randint(0,2), 0, 0, 0, "Visual", 0.20)) # Visual
    s_list.append(Student(0, random.randint(0,1), 1, 1, "Non-visual", 0.40)) # Non-visual
    s_list.append(Student(2, 0, random.randint(0,1), 0, "Independant", 0.20)) # Indepentant
    s_list.append(Student(1, 1, 1, random.randint(0,1), "Dependant", 0.20)) # Dependant
    log_file.write("\nStudent List:\n")
    log_file.write("Visual: \t\t lambda:%.2f %s\n" %(s_list[0].get_lambda(), str(s_list[0])))
    log_file.write("Non-Visual: \t lambda:%.2f %s\n" %(s_list[1].get_lambda(), str(s_list[1])))
    log_file.write("Independant: \t lambda:%.2f %s\n" %(s_list[2].get_lambda(), str(s_list[2])))
    log_file.write("Dependant: \t\t lambda:%.2f %s\n" %(s_list[3].get_lambda(), str(s_list[3])))
    return s_list

def getConfigMu(config, students):
    # sum_(over all students) probofchoosing(student) * probofsuccess(config, student)
    total = 0.0
    for student in students:
        dist = distance(config, student)
        total += student.get_prob() * probability(dist)
    return total 

def log_results(log_file, student, arm,  probability, result):
    if(result == 1):
        res = "PASS"
    else:
        res = "FAIL"

    log = "Student(%-11s):\t lambda:%.2f %s\t  arm: %s\t %.2f%s %s\n" %(student.get_name(), student.get_lambda(), str(student), str(arm), probability, "%",res)
    log_file.write(log)


def simulate(config, students, log_file):
    arm = LineConfig(config[0], config[1], config[2], config[3])
    student = pick_student(students)
    dist = distance(arm, student)
    prob = probability(dist)
    rew = reward(prob)
    # log_results(log_file, student, arm, prob, rew)
    return rew
