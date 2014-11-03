import math
import numpy

def sequential_halving(arms, bound):
    """
    Sequential Halving -- (Fixed Bound)
    Parameters:
    * let arms be a an array where each entry is an arm and all of
        it's simulated results
    * bound is an integer which represents the maximum number of 
        arms pulls the algorithm is limited to find optimal arms with
    ** still unsure how we will set up our s, right now it is a list of
        the array arms, which shrinks by half on each iteration
    """
    s = list()
    s.append(arms)
    for r in range(math.log2(len(arms)) - 1):

        # compute the pulls per arm per iteration
        pulls_per_arm = math.floor(bounds / (len(s[r])
                * math.ceil(math.log2(len(arms)))))

        # sample each arm pulls_per_arm times and average results
        total = 0
        for i in range(len(s[r])):
            for j in range(pulls_per_arm):

                # sample arm i from remaining arms pulls_per_arm times
                total += sample(s[r][i])
            s[r][i].setAverage(total/pulls_per_arm)
        
        # sort the remaining arms by average from above sample
        s[r] = sortArms(s[r])

        # create next iteration which the upper half of the sorted list
        s.append(math.ceil(s[r][(len(s[r])/2):]))

    return s[math.log2(len(arms))]
            
        
