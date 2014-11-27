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

def armDistribution(log_file, out_file):
    #used for regret summary
    for line in log_file:
        if(line[0] == 'A'):
            temp = line.split(' ')
            out_file.write(temp[-1])
        if(line[0:5] == "--- E"):
                out_file.write("\n")
    out_file.close()


#base = open("lilucb_50runs_conf2_Nov20.out", "r")
#log_file = open("regrets_summary_lilucb_overdist_nov27.data", "r")
#arm_out_file = open("arms_summary_lilucb_largedist_Nov27.data", "w")
#summary_file = open("pull_summary_lilucb_config2_nov27.data", "w")

#reformat_logs(base, summary_file)
#armDistribution(base, log_file)
#summary_file.close()

#Delta average
summary_file = open("pull_summary_lilucb_largedist_nov27.data", "r")
delta_out_file = open("deltas_summary_lilucb_largedist_nov27.data", "w")
averageResults(summary_file, delta_out_file,1001, 1)

#base.close()
#log_file.close()
#arm_out_file.close()
summary_file.close()
delta_out_file.close()