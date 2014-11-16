import numpy
import sim
import egreedy
import lil_ucb
import sequential_halving
import datetime


def main():
    cFile = open("configs.txt", "r")
    log_file = open("log_file.txt", "a+")
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

    best_arm = egreedy.epsilon_greedy(students, configs, 10000, 0.05, log_file)
    #best_arm = lil_ucb.lil_ucb(students, configs, 0.001 , 0.5, 1.0 + (10/144), 1, 0.05, log_file)
    #best_arm = sequential_halving.sequential_halving(students, configs, 10000, log_file)

    log_file.write("\nBEST ARM: %s\n" %(str(best_arm)))
    log_file.write("--- END OF EXPERIMENT ---\n\n")
    print("BEST ARM:")
    print(best_arm)
    log_file.close()


if __name__=="__main__":
    main()
