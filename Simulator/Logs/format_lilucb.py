def reformat_logs(logFile, newLog):
    delta_val = -1
    count = 0
    for line in logFile:
        if(line[0] != 'I'):
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

def armDistribution(logFile, tempFile):
    for line in logFile:
        if(line[0] == 'A'):
            temp = line.split(' ')
            tempFile.write(temp[-1])
        if(line[0:5] == "--- E"):
                tempFile.write("\n")
    tempFile.close()


base = open("lilucb_50runs_conf2_Nov20.out", "r")
temp = open("condensed_results", "w")
#outfile = open("lilucb_50runs_base_largedist_averages_nov22", "w")
arm_out_file = open("arms_summary_lilucb_conf2_Nov25", "w")
#reformat_logs(f, f2)
#averageResults(temp, outfile, 1001, 1)
armDistribution(base, temp)
temp = open("condensed_results", "r")
averageResults(temp, arm_out_file,720, 6)
temp.close()
base.close()