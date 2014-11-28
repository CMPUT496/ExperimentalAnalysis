import math
import numpy
import sim
import logger
import operator

def get_actual_max(arms):
    arms_copy = sorted(arms, key=operator.attrgetter('config_mu'), reverse=True)
    return arms_copy[0]

def calculate_delta(arms, actual_max):
    for arm in arms:
        arm.set_delta(actual_max.get_config_mu() - arm.get_config_mu())

def sequential_halving(students, arms, bound, log_file):
    """
    Sequential Halving -- (Fixed Bound)
    Parameters:
    * let arms be an array of vectors, where each vector is a configuration
    * bound is an integer which represents the maximum number of
        arms pulls the algorithm is limited to find optimal arms with
    ** still unsure how we will set up our s, right now it is a list of
        the array arms, which shrinks by half on each iteration
    """
    # logging header
    log_file.write("\n--- Sequential Halving ---\n")

    s = list()
    # add arms with initialized values to the list
    inner_list = list()
    for arm in arms:
        s_arm = sim.LineConfig(arm[0], arm[1], arm[2], arm[3], arm[4])
        s_arm.set_config_mu(students)
        inner_list.append(s_arm)
    s.append(inner_list)

    # get the arm with the highest config_mu for comparison
    actual_max = get_actual_max(s[0])

    # set deltas
    calculate_delta(s[0], actual_max)

    # log all arms
    logger.log_arms(log_file, s[0])

    current_pulls = 0
    # run through iterations of algorithm
    for r in range(int(math.ceil(math.log(len(arms), 2)))):

        # compute the pulls per arm per iteration
        pulls_per_arm = int(math.floor(bound / (len(s[r])
                * math.ceil(math.log(len(arms), 2)))))
        current_pulls += pulls_per_arm + 1

        # sample each arm pulls_per_arm times and average results
        for i in range(len(s[r])):
            total = 0.0
            for j in range(pulls_per_arm):
                s[r][i].set_num_pulls(s[r][i].get_num_pulls() + 1)
                total += sim.simulate(s[r][i], students, log_file)
            s[r][i].set_average(total/pulls_per_arm)

	# sort the remaining arms by average from above sample
        s[r].sort(key=operator.attrgetter('average'), reverse=False)

        # create next iteration which the upper half of the sorted list
        s.append(s[r][int(math.ceil(len(s[r])/2)):])

        # log the current empirical best arm
        logger.log_pulled_arm(log_file, s[r][len(s[r]) - 1], current_pulls)  

    arm = s[int(math.ceil(math.log(len(arms), 2)))][0]
    logger.log_pulled_arm(log_file, arm, bound)
    logger.log_best_arm(log_file, arm, bound)

    for arm in s[0]:
        logger.log_num_pulls(log_file, arm)
    
    return arm
