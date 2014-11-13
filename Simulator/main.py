import sim

def main():

    cFile = open("configs.txt", "r")
    configs = []
    for line in cFile:
        configs = [int(n) for n in line.split()]
        sim.simulate(configs)
    return
	sim.simulate()
	return

if __name__=="__main__":
	main()


