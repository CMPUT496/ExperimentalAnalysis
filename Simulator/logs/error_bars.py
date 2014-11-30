import math

#THIS SHIT AINT TESTED TYLER


def get_error_bars(outfile, regrets, averages, confidence = 0.05, n = 50, N = 1000):
    # The configs file should be a list of the average regret for each arm,
    #   for each distribution. 
    #   i.e. The 120 configuration averages, as seen in files like:
    #       arms_summary_seqhav_config1_november23.data
    # regrets is the original list of unaveraged deltas
    # outfile will be where the data is stored. Naming convention:
    #   errorbars_algorithm_configration_(Distrubution, if non-standard)_date.data

    # standard error = c * sqrt(variance / number_of_samples)
    # c roughly equal to sqrt(log(2/confidence))
    # variance = ((1/(n-1)) * sum(t=1 to n)[ X_t - r_hat ]**2 )**2
    # r_hat = the average for any given arm across 50 runs
    # X_t is the delta for the 't'th run
    r_hat = list()
    for line in averages:
        r_hat.append(float(line))

    i = 0
    t = 0
    X = [[0 for i_i in range(n)] for t_t in range(N)]
    #get each X[t][i]
    for count,line in enumerate(regrets):
        if(line[0] == '\n'):
            for timestep in range(t, N): #fill in all values when lilucb ends early
                #print("..", timestep, i, X[timestep][i])
                X[timestep][i] = val
            t = 0 # reset timestep
            i += 1 # next run
        else:
            val = float(line)
            X[t][i] = val
            t += 1

    s_dev = [0 for t in range(N)]
    const = 1.0/(N + 1)
    for t in range(N):
        val = 0
        for i in range(n):
            val += (X[t][i] - r_hat[t])**2

        s_dev[t] = const*val

    variance = [s**2 for s in s_dev]

    c = math.sqrt(math.log(2.0/confidence))

    for i in range(N):
        stand_err = c * math.sqrt( variance[i] / confidence)
        out_file.write("%f\n" %(stand_err))




out_file = open("standard_errors/errorbars_egreedy_50runs_0-1eps_100000bound_largedist_November29.data", "w")
regret_averages = open("average_regrets/average_regret_egreedy_50runs_0-1eps_100000bounds_largedist_November28.data", "r")
regrets = open("regrets/regrets_egreedy_50runs_0-1eps_100000bounds_largedist_November28.data", "r") 

get_error_bars(out_file,regrets, regret_averages)

out_file.close()
regrets.close()
regret_averages.close()

# out_file = open("OUTPUT.out", "w")
# regret_averages = open("test_average.in", "r")
# regrets = open("test_regrets.in", "r")

# get_error_bars(out_file, regrets, regret_averages, n = 3, N = 5)
