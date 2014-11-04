import math
from numpy import *

def lil_UCB(arms,delta=1,epsilon=1,lambda=1,beta=1,sigma=1):
"""
Parameters:
* arms is a row vector containing ID of different arms.
* Other parameters are just different constants
* T is a row vector having the number of times an arm is pulled after n iterations. So T[i] represents the same arm that arms[i] represents
* mu[i] represents mean value of arm i
* upper_bound is a vector that has upper bounds of every arms in a single iteration. After calculating upper_bound, the algorithm chooses that arm that has the maximum upper bound from upper_bound vector.

"""
	timestep=0
	n=len(arms)
	mu=zeros(n)
	T=zeros(n)
	for i in range(0,n):
		timestep=timestep+1
		T[i]=T[i]+1
		r=reward(arm[i],timestep,T,i)
		mu[i]=r


	while True:

		counter=0

		for i in range(0,n):
			if T[i]<1+lambda*(sum(T)-T[i]):
				counter=counter+1

		if counter!=n:
			break

		timestep=timestep+1

		upper_bound=zeros(n)
		# for j in range(0,n):

		# upper_bound[j]=mu[j] + (1+beta)*(1+sqrt(epsilon))*sqrt((2*(sigma**2)*(1+epsilon)*math.log((math.log((1+epsilon)*T[j]))/delta))/T[j])
		upper_bound=mu + (1+beta)*(1+sqrt(epsilon))*sqrt((2*(sigma**2)*(1+epsilon)*math.log((math.log((1+epsilon)*T))/delta))/T)

		index=upper_bound.argmax()
		T[index]=T[index]+1
		r=reward(arm[index],timestep,T,index)
		mu[index]=( (T[index]-1)*mu[index] + r)/T[index]

	return arms[T.argmax()]


def reward(arm,timestep,T,index):

	return reward
