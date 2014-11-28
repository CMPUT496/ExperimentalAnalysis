import numpy
import sim
import egreedy
import lil_ucb
import sequential_halving
import datetime
import sys
import math
import logger


def main():
    if len(sys.argv) > 3:
        file_name = "logs/raw_data/"
        file_name += sys.argv[2]
        config_name = "configs/" + sys.argv[3]
    elif len(sys.argv) > 1:
        file_name = "logs/raw_data/log_file.txt"
    else:
        print("Not enough arguments")
        sys.exit(0)

    print(config_name)
    cFile = open(config_name, "r")
    #cFile = open("configs_extras.txt", "r")
    log_file = logger.open_log(file_name)
    configs = list()

    # construct a list of config arrays representing all tha arms
    for line in cFile:
        config = numpy.asarray([int(n) for n in line.split()])
        configs.append(config)

    # retrieve list of students for this run
    students = sim.get_student_list(log_file)
    #students = list()
    #students.append(sim.Student(0, 0, 0, 1, 1, "Test", 1.0))


    if (int(sys.argv[1]) == 0):
        epsilon = 0.05
        bound = 100000
        if (len(sys.argv) > 4):
            epsilon = float(sys.argv[4])
        if (len(sys.argv) > 5):
            bound = int(sys.argv[5])
        message = "Running epsilon greedy algorithm with epsilon = %f," \
                " and bounded by %d pulls...\n" %(epsilon, bound)
        print(message)
        log_file.write(message)
        best_arm = egreedy.epsilon_greedy(students, configs,
                bound, epsilon, log_file)

    elif (int(sys.argv[1]) == 1):
        conf = 0.95
        e = 0.01 #epsilon
        c_e = ((2+e)/2) * ((1/math.log(1+e))** ( 1 + e)) # C sub epsilon
        beta = 1
        lambda_ = 9
        bound = 100000
        delta = (((math.sqrt(1 + (conf/2)) - 1)**2)/(4*c_e))

        if (len(sys.argv) > 4):
            bound = int(sys.argv[4])

        message = "Running lil-UCB algorithm with epsilon: %.3f, confidence:" \
                " %.3f, beta: %d, lambda: %d...\n" %( e, conf, beta, lambda_)
        print(message)
        log_file.write(message)
        best_arm = lil_ucb.lil_ucb(students, configs, delta,
                e, lambda_, beta , 1-conf, log_file, bound)
    else:
        bound = 50000
        if (len(sys.argv) > 4):
            bound = int(sys.argv[4])
        message = "Running sequential-halving algorithm bounded " \
                "by %d pulls...\n" %(bound)
        print(message)
        log_file.write(message)
        best_arm = sequential_halving.sequential_halving(students,
                configs, bound, log_file)

    log_file.write("--- END OF EXPERIMENT ---\n\n")
    logger.close_log(log_file)


if __name__=="__main__":
    main()
