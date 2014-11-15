import numpy
import sim
import egreedy
import lil_ucb
import sequential_halving
import datetime


def main():
    cFile = open("configs.txt", "r")
    logFile = open("logfile.txt", "a+")
    configs = list()

    # construct a list of config arrays representing all tha arms
    for line in cFile:
        config = numpy.asarray([int(n) for n in line.split()])
        configs.append(config)


    # Header for the log file
    time = datetime.datetime.now().time()
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S"))

    # retrieve list of students for this run
    students = sim.get_specific_student()

    best_arm = egreedy.epsilon_greedy(students, configs, 10000, 0.05, logFile)
    best_arm = lil_ucb.lil_ucb(students, configs, 0.001 , 0.5, 1.0 + (10/144), 1, 0.05, logFile)
    best_arm = sequential_halving.sequential_halving(students, configs, 10000, logFile)

    print("BEST ARM:")
    print(best_arm)


if __name__=="__main__":
    main()
