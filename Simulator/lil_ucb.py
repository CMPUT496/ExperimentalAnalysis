import numpy
import random
import sample_arm
import sim
import math

def lil_ucb(arms, confidence, epsilon, lambda, beta, sigma):
    time = 0
    n = len(arms)
    mu = numpy.zeros(n) # set of rewards
    T = numpy.zeros(n) # T[i] is the number of times arm i has been pulled
    armList = list()

    for arm in arms:
        s_arm = sample_arm.SampleArm(arm)
        s.append(s_arm)

    #sample each of the n arms once, set T_i(t) = 1, for all i and set t=n
    for i in range(n):
        timestep += 1
        T[i] = 1
        mu[i] = sim.simulate(armList[i])



# def lil_UCB(arms,delta=1,epsilon=1,lambda=1,beta=1,sigma=1):
#     timestep=0
#     n=len(arms)
#     mu=zeros(n)
#     T=zeros(n)
#     for i in range(0,n):
#         timestep=timestep+1
#         T[i]=T[i]+1
#         r=reward(arm[i],timestep,T,i)
#         mu[i]=r


#     while True:

#         counter=0

#         for i in range(0,n):
#             if T[i]<1+lambda*(sum(T)-T[i]):
#                 counter=counter+1

#         if counter!=n:
#             break

#         timestep=timestep+1

#         upper_bound=zeros(n)
#         # for j in range(0,n):

#         # upper_bound[j]=mu[j] + (1+beta)*(1+sqrt(epsilon))*sqrt((2*(sigma**2)*(1+epsilon)*math.log((math.log((1+epsilon)*T[j]))/delta))/T[j])
#         upper_bound=mu + (1+beta)*(1+sqrt(epsilon))*sqrt((2*(sigma**2)*(1+epsilon)*math.log((math.log((1+epsilon)*T))/delta))/T)

#         index=upper_bound.argmax()
#         T[index]=T[index]+1
#         r=reward(arm[index],timestep,T,index)
#         mu[index]=( (T[index]-1)*mu[index] + r)/T[index]

#     return arms[T.argmax()]