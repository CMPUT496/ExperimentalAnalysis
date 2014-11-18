import numpy
import random
import sim
import operator

def pick_arm(arms, epsilon):
    # 1 - epsilon percent of the time choose greedily
    # otherwise randomly choose an arm
    if (random.random() >= epsilon):
        # choose greedily
        return 0
    else:
        # choose randomly
        return random.randint(0, len(arms) - 1)

def get_actual_max(arms):
    arms_copy = arms
    arms_copy.sort(key=operator.attrgetter('config_mu'), reverse=True)
    return arms_copy[0]

def epsilon_greedy(students, arms, bound, epsilon, log_file):
    """
    arms is a list of configurations, each config can be passed as a
    numpy array.
    bound is the number of arm pulls we will limit ourselves to
    """
    # logging header
    log_file.write("\n--- Epsilon Greedy ---\n")

    # build list of sampleArm objects to track rewards and averages
    s = list()
    for arm in arms:
        s_arm = sim.LineConfig(arm[0], arm[1], arm[2], arm[3], arm[4])
        s_arm.set_config_mu(students)
        s.append(s_arm)

    max_arm = get_actual_max(s)

    for i in range(bound):
        # because we are not using a simple numpy.array we will sort
        # the list in place on each interval (ineffeciennnncy)
        # to get the greedy arm
        j = pick_arm(s, epsilon)
        s[j].set_num_pulls(s[j].get_num_pulls() + 1)

        # pull the arm
        reward = sim.simulate(s[j], students, log_file)
        s[j].set_total_reward(
                s[j].get_total_reward() + reward)
        s[j].set_average(
                s[j].get_total_reward() / s[j].get_num_pulls())

        # sort the arms
        s.sort(key=operator.attrgetter('average'), reverse=True)

    # return the best arm
    for arm in s:
        log_file.write("ARM: %s\tAVERAGE: %f\tCONFIGMU: %f\tDELTA: %f\n"
                %(str(arm), arm.get_average(), arm.get_config_mu(), max_arm.get_config_mu() - arm.get_config_mu()))
    return str(s[0])
