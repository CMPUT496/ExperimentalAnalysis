import math
import numpy
import sim
import operator

def get_actual_max(arms):
    arms_copy = arms
    arms_copy.sort(key=operator.attrgetter('config_mu'), reverse=True)
    return arms_copy[0]

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
        #arm = sample_arm.SampleArm(arms[i])
        #print("INPUTTED ARM: %s" %(arm))
        s_arm = sim.LineConfig(arm[0], arm[1], arm[2], arm[3])
        s_arm.set_config_mu(students)
        #print("GENERATTED LINECONFIG: %s" %(s_arm))
        inner_list.append(s_arm)
    s.append(inner_list)

    #for arm in s[0]:
    #    print(arm)
    # get the arm with the highest config_mu for comparison
    actual_max = get_actual_max(s[0])

    # run through iterations of algorithm
    for r in range(int(math.ceil(math.log(len(arms), 2)))):

        # compute the pulls per arm per iteration
        pulls_per_arm = int(math.floor(bound / (len(s[r])
                * math.ceil(math.log(len(arms), 2)))))

        # sample each arm pulls_per_arm times and average results
        total = 0
        for i in range(len(s[r])):
            for j in range(pulls_per_arm):
                total += sim.simulate(s[r][i], students, log_file)

            s[r][i].set_average(total/pulls_per_arm)

	# sort the remaining arms by average from above sample
        s[r].sort(key=operator.attrgetter('average'), reverse=False)

        # create next iteration which the upper half of the sorted list
        s.append(s[r][int(math.ceil(len(s[r])/2)):])

        # log the current array s
        log_file.write("\nINDEX: %2d -- PULLS PER ARM: %d\n" %(r, pulls_per_arm))
        for arm in s[r+1]:
            log_file.write("ARM: %s\tAverage: %f\n"
                    %(str(arm), arm.get_average()))
    return s[int(math.ceil(math.log(len(arms), 2)))][0]
