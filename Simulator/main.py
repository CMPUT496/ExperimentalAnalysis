import numpy
import sim
import egreedy
import sequential_halving

def main():
	cFile = open("configs.txt", "r")
	configs = list()
	for line in cFile:
		config = numpy.asarray([int(n) for n in line.split()])
		configs.append(config)

	best_arm = egreedy.epsilon_greedy(configs, 1000, 0.05)
	print("BEST ARM:")
	print(best_arm)
	#sequential_halving.sequential_halving(configs, 10000)

if __name__=="__main__":
	main()
