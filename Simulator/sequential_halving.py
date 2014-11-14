import math
import numpy
import sample_arm
import sim

def sequential_halving(arms, bound):
    """
    Sequential Halving -- (Fixed Bound)
    Parameters:
    * let arms be an array of vectors, where each vector is a configuration
    * bound is an integer which represents the maximum number of
        arms pulls the algorithm is limited to find optimal arms with
    ** still unsure how we will set up our s, right now it is a list of
        the array arms, which shrinks by half on each iteration
    """
    s = list()

    # add arms with initialized values to the list
    for i in range(len(arms)):
        a = list()
        arm = sample_arm.sampleArm(arms[i])
        a.append(arm)
    s.append(a)

    # run through iterations of algorithm
    for r in range(math.log2(len(arms)) - 1):

        # compute the pulls per arm per iteration
        pulls_per_arm = math.floor(bounds / (len(s[r])
                * math.ceil(math.log2(len(arms)))))

        # sample each arm pulls_per_arm times and average results
        total = 0
        for i in range(len(s[r])):
            for j in range(pulls_per_arm):

                # sample arm i from remaining arms pulls_per_arm times
                total += sim.simulate(s[r][i].getArm())
            s[r][i].setAverage(total/pulls_per_arm)

        # sort the remaining arms by average from above sample
        s[r] = s[r].sort(key=lambda x: x.get_average, reverse=False)

        # create next iteration which the upper half of the sorted list
        s.append(math.ceil(s[r][(len(s[r])/2):]))

    return s[math.log2(len(arms))]
