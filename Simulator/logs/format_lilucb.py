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
        if(line[0] == 'A'):
            if(count%step== 0):
                temp = line.split(' ')
                out_file.write(temp[-1])
        if(line[0:5] == "--- E"):
                out_file.write("\n")
        count += 1
    out_file.close()

def remove_duplicates(in_file, out_file):
    temp = "\n"
    for line in in_file:
        if (line != temp):
            temp = line
            out_file.write(line)



# base = open("lilucb_50runs_conf2_Nov20.out", "r")
# log_file = open("regrets_summary_lilucb_config2_nov27.data", "w")
#arm_out_file = open("arms_summary_lilucb_largedist_Nov27.data", "w")
#summary_file = open("pull_summary_lilucb_config2_nov27.data", "w")

#reformat_logs(base, summary_file)
#armDistribution(base, log_file, 6)
#summary_file.close()

#Delta average
# summary_file = open("pull_summary_lilucb_largedist_nov27.data", "r")
# delta_out_file = open("deltas_summary_lilucb_largedist_nov27.data", "w")
# averageResults(summary_file, delta_out_file,1001, 1)

# base.close()
# log_file.close()
#arm_out_file.close()
# summary_file.close()
# delta_out_file.close()

#remove_duplicates
in_f = open("regrets_summary_seqhav_config1_November23.data", "r")
out_f = open("regrets_summary_seqhav_config1_November27.data", "w")
remove_duplicates(in_f, out_f)