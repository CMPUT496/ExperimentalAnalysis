def reformat_logs(logFile, newLog):
    delta_val = -1
    count = 0
    for line in logFile:
        if(line[0] != 'I'):
			if(line[0:5] == "--- E"):
				newLog.write("\n")
				print( count)
			continue
        components = line.split(" ")
        delta_val = components[-1]
        newLog.write("%s" %(delta_val))
        count += 1


def averageResults(logFile):
	newLog = open("lilucb_50runs_base_largedist_averages_nov22", "w")
	averages = [0 for i in range(1001)]
	last_val = 0
	lc = 0
	for line in logFile:
		if(line[0] == '\n'):
			if(lc != 1001):
				for i in range(lc,1001):
					averages[i] += last_val
			lc = 0

		else:
			last_val = float(line)
			averages[lc] += last_val
			lc += 1

	for i in range(1001):
		newLog.write("%f\n" %(averages[i]/50))


f = open("lilucb_50runs_baseconf_overdist_Nov22.out", "r")
f2 = open("condensed_results", "w")
reformat_logs(f, f2)
f.close()
f2.close()
f2 = open("condensed_results", "r")
averageResults(f2)