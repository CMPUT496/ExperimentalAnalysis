def reformat_logs(logFile, newLog):
    delta_val = -1
    count = 0
    for line in logFile:
        if(line[0:2] != 'IT'):
			if(line[0:5] == "--- E"):
				newLog.write("\n")
				#print( count)
			continue
        components = line.split(" ")
        delta_val = components[-1]
        newLog.write("%s" %(delta_val))
        count += 1

def averageResults(logFile, outFile, length, step):
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
    for line in log_file:
        if(line[0] == 'A'):
            temp = line.split(' ')
            out_file.write(temp[-1])
        if(line[0:5] == "--- E"):
                out_file.write("\n")
    out_file.close()


base = open("lilucb_50runs_underdist_Nov26.out", "r")
log_file = open("regrets_summary_lilucb_underdist_nov27.data", "w")
#arm_out_file = open("arms_summary_lilucb_conf2_Nov25", "w")
#outfile = open("lilucb_50runs_base_largedist_averages_nov22", "w")
#reformat_logs(base, log_file)
#averageResults(log_file, outfile, 1001, 1)
#armDistribution(base, log_file)
#log_file = open("condensed_results", "r")
#averageResults(log_file, arm_out_file,720, 6)
armDistribution(base, log_file)
log_file.close()
base.close()