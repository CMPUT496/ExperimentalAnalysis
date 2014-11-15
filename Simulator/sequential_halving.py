import math
import numpy
import sample_arm
import sim
import operator

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
    for i in range(len(arms)):
        arm = sample_arm.SampleArm(arms[i])
        inner_list.append(arm)
    s.append(inner_list)

    # run through iterations of algorithm
    for r in range(int(math.ceil(math.log(len(arms), 2)))):

        # compute the pulls per arm per iteration
        pulls_per_arm = int(math.floor(bound / (len(s[r])
                * math.ceil(math.log(len(arms), 2)))))

        # sample each arm pulls_per_arm times and average results
        total = 0
        for i in range(len(s[r])):
            for j in range(pulls_per_arm):
                total += sim.simulate(s[r][i].get_arm(), students, log_file)

            s[r][i].set_average(total/pulls_per_arm)

	# sort the remaining arms by average from above sample
        s[r].sort(key=operator.attrgetter('average'), reverse=True)

        # create next iteration which the upper half of the sorted list
        s.append(s[r][int(math.ceil(len(s[r])/2)):])

        # log the current array s
        log_file.write("\nINDEX: %2d\n" %(r))
        for arm in s[r+1]:
            log_file.write("%s\n" %(str(arm.get_arm())))
    return s[int(math.ceil(math.log(len(arms), 2)))][0].get_arm()
