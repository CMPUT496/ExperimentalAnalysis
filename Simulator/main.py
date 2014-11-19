import numpy
import sim
import egreedy
import lil_ucb
import sequential_halving
import datetime
import sys
import math


def main():
    if len(sys.argv) > 2:
        file_name = "Logs/"
        file_name += sys.argv[2]
    elif len(sys.argv) > 1:
        file_name = "Logs/log_file.txt"
    else:
        print("Not enough arguments")
        sys.exit(0)

    cFile = open("configs.txt", "r")
    log_file = open(file_name, "a+")
    configs = list()

    # construct a list of config arrays representing all tha arms
    for line in cFile:
        config = numpy.asarray([int(n) for n in line.split()])
        configs.append(config)

    # Header for the log file
    time = datetime.datetime.now().time()
    log_file.write("%s" %(time.strftime("%Y-%m-%d %H:%M:%S")))

    # retrieve list of students for this run
    students = sim.get_student_list(log_file)

    if (int(sys.argv[1]) == 0):
        epsilon = 0.1
        bound = 100000
        print("Running epsilon greedy algorithm with epsilon = %f, and bounded by %d pulls..."
                %(epsilon, bound))
        best_arm = egreedy.epsilon_greedy(students, configs, bound, epsilon, log_file)
    elif (int(sys.argv[1]) == 1):
        conf = 0.95
        e = 0.01 #epsilon
        c_e = ((2+e)/2) * ((1/math.log(1+e))** ( 1 + e)) # C sub epsilon
        beta = 1
        lambda_ = 9

        print("Running lil-UCB algorithm with epsilon: %.3f, confidence: %.3f, beta: %d, lambda: %d...\n" %( e, conf, beta, lambda_))
        best_arm = lil_ucb.lil_ucb(students, configs, (((math.sqrt(1 + (conf/2)) - 1)**2)/(4*c_e)) , e, lambda_, beta , 1-conf, log_file)
    else:
        bound = 100000
        print("Running sequential-halving algorithm bounded by %d pulls..."
                %(bound))
        best_arm = sequential_halving.sequential_halving(students, configs, bound, log_file)

    log_file.write("\nBEST ARM: %s\n" %(str(best_arm)))
    log_file.write("--- END OF EXPERIMENT ---\n\n")
    print("BEST ARM:")
    print(best_arm)
    log_file.close()


if __name__=="__main__":
    main()
