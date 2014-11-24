

def reformat_logs(logFile):
    newLog = open("parsed.out2", "w")
    delta_val = -1
    old = -2
    for line in logFile:
        if(line[0] != 'I'):
            continue
        components = line.split(" ")
        delta_val = components[-1]
        newLog.write("%s" %(delta_val))


f = open("Logs/lilucb_1000runs_baseconf_Nov20.out", "r")
reformat_logs(f)