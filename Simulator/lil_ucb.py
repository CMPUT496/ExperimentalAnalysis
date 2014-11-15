import numpy
import random
import sample_arm
import sim
import math

def lil_ucb(arms, delta, epsilon, lambda_p, beta, sigma):
    # delta == confidence
    # 
    time = 0
    n = len(arms)
    mu = numpy.zeros(n) # set of rewards
    T = numpy.zeros(n) # T[i] is the number of times arm i has been pulled
    armList = list()

    for arm in arms:
        s_arm = sample_arm.SampleArm(arm)
        armList.append(s_arm)

    #sample each of the n arms once, set T_i(t) = 1, for all i and set t=n
    for i in range(n):
        T[i] = 1
        mu[i] = sim.simulate(armList[i]) #pull the arm

    timestep = n

    while True:
        counter = 0
        done = False
        total_pulls = sum(T)
        timestep += 1

        for i in range(n):
            #check if an arm has been pulled more than all others combined
            if T[i] > 1 + lambda_p*(total_pulls - T[i]): 
                done = True
                break

        if done:
            break

        index = 0
        upper_bound_value = 0

        for i in range(n):
            #temp is that magic value used to determine the best, next arm to pull
            temp = math.sqrt((2*sigma**2 * (1 + epsilon) * math.log( math.log((1 + epsilon)* T[i])/delta))/T[i])
            temp = mu[i] + (1 + beta)*(1 + math.sqrt(epsilon))*temp

            if(temp > upper_bound_value):
                upper_bound_value = temp
                index = i


        T[index] += 1
        reward = sim.simulate(armList[index])
        mu[index] = ((T[index]-1)*mu[index] + reward) / T[index] #average the rewards

    return armList[T.argmax()]