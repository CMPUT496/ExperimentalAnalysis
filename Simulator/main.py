import numpy
import sim
import egreedy
import sequential_halving

def main():
	cFile = open("configs.txt", "r")
	configs = list()

	# construct a list of config arrays representing all tha arms
	for line in cFile:
		config = numpy.asarray([int(n) for n in line.split()])
		configs.append(config)

	best_arm = egreedy.epsilon_greedy(configs, 10000000, 0.05)
	#sequential_halving.sequential_halving(configs, 10000)
	print("BEST ARM:")
	print(best_arm)

if __name__=="__main__":
	main()
