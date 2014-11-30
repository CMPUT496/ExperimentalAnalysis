def reformat_logs(logFile, newLog):
    #used for delta summary
    delta_val = 0
    count = 0
    for line in logFile:
        if(line[0:5] == "--- E"):
            newLog.write("\n")
        if(line[0:2] == 'IT'):
            components = line.split(" ")
            delta_val = components[-1]
            newLog.write("%s" %(delta_val))
        count += 1

def averageResults(logFile, outFile, length, step):
    #used for delta summary, arm summary
	averages = [0 for i in range(length)]
	last_val = 0
	lc = 0
	for line in logFile:
		if(line[0] == '\n'):
			if(lc != length):
				for i in range(lc,length):
					averages[i] += last_val
			lc = 0
		else:
			last_val = float(line)
			averages[lc] += last_val
			lc += 1

	for i in range(length):
		if(i%step == 0):
			outFile.write("%f\n" %(averages[i]/50))

def armDistribution(log_file, out_file, step):
    #used for regret summary
    count = 0
    for line in log_file:
        if(line[0:4] == 'ARM:'):
            if(count%step== 0):
                temp = line.split(' ')
                out_file.write(temp[-1])
        # if(line[0:5] == "--- E"):
        #         out_file.write("\n")
        if(line[0:7] == "Running" and count > 10):
                out_file.write("\n")
        count += 1
    out_file.close()

def remove_duplicates(in_file, out_file):
    temp = "\n"
    for line in in_file:
        if (line != temp):
            temp = line
            out_file.write(line)

def get_arm_pull_count(in_file, out_file):
    pulls = [0 for i in range(120)]
    index = 0
    for i,line in enumerate(in_file):
        if(line[0:4] == "ARMP"):
            temp = line.split()
            pulls[index%120] += int(temp[-1])
            index += 1

        if(line[0:7] == "Running" and i > 10):
            index = 0

    for i in range(120):
        out_file.write("%d\n" %(pulls[i]))


#Regrets
# raw_file = open("raw_data/lilucb_50runs_largedist_Nov28.out", "r")
# log_file = open("regrets/regrets_lilucb_50runs_largedist_November29.data", "w")
# reformat_logs(raw_file, log_file)
# raw_file.close()
# log_file.close()


# Average Regrets
# summary_file = open("regrets/regrets_lilucb_50runs_extraparams2_November29.data", "r")
# averages_file = open("average_regrets/average_regret_lilucb_50runs_extraparams2_November29.data", "w")
# averageResults(summary_file, averages_file,1001, 1)
# summary_file.close()
# averages_file.close()

#remove_duplicates
# in_f = open("regrets_summary_seqhav_config1_November23.data", "r")
# out_f = open("regrets_summary_seqhav_config1_November27.data", "w")
# remove_duplicates(in_f, out_f)

# Arm Distributions all runs
# raw_data = open("raw_data/lilucb_50runs_largedist_Nov28.out", "r")
# temp_file = open("temporary_files/arms_distributions_per_run_lilucb_largedist_November29.data", "w")
# armDistribution(raw_data, temp_file, 1)
# raw_data.close()
# temp_file.close()


# Arm Distributions averages
# arm_vals = open("temporary_files/arms_distributions_per_run_lilucb_largedist_November29.data", "r")
# averages = open("arm_distributions/arms_lilucb_50runs_largedist_November29.data", "w")
# averageResults(arm_vals, averages, 120, 1)
# arm_vals.close()
# averages.close()

# Arm pull Counts
raw_data = open("raw_data/lilucb_50runs_baseconfig_Nov28.out", "r")
pull_file = open("arm_distributions/pullcount_lilucb_50runs_baseconfig_November29.data", "w")
get_arm_pull_count(raw_data, pull_file)
raw_data.close()
pull_file.close()