import math

#THIS SHIT AINT TESTED TYLER

def get_error_bars(outfile, in_file, averages, confidence = 0.05, n = 50, configs = 120):
    # The configs file should be a list of the average regret for each arm,
    #   for each distribution. 
    #   i.e. The 120 configuration averages, as seen in files like:
    #       arms_summary_seqhav_config1_november23.data
    # in_file is the original list of unaveraged deltas
    # outfile will be where the data is stored. Naming convention:
    #   errorbars_algorithm_configration_(Distrubution, if non-standard)_date.data

    # standard error = c * sqrt(variance / number_of_samples)
    # c roughly equal to sqrt(log(2/confidence))
    # variance = ((1/(n-1)) * sum(t=1 to n)[ X_t - r_hat ]**2 )**2
    # r_hat = the average for any given arm across 50 runs
    # X_t is the delta for the 't'th run

    c = math.sqrt(math.log(2.0/confidence))

    r_hat_list = list()
    for line in averages:
        r_hat_list.append(float(line))

    s_dev_list = list()
    for i in range(configs):
        s_dev_list.append(0)

    arm_index = 0
    for line in in_file:
        if(line[0] == '\n'):
            arm_index = 0
        else:
            v = float(line) - r_hat_list[arm_index]
            s_dev_list[arm_index] += (v**2)/(n - 1)
            arm_index += 1


    variance = list() #rename for clarity
    for s in s_dev_list:
        variance.append(s**2)


    for i in range(configs):
        val = c
        val *= math.sqrt(variance[i]/n)
        outfile.write("%f\n" %(val))




out_file = open("errorbars_seqhav_largedist_Nov27.data", "w")
arms_averages = open("arms_summary_seqhav_largedist_November26.data", "r")
in_file = open("regrets_summary_seqhav_largedist_November26.data", "r") #This should be the temporarp file in arm distribution,
                                                                # not the regret values per 100th arm pull
get_error_bars(out_file,in_file, arms_averages)

