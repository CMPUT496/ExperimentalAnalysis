import sys

def parse_deltas(log_file, delta_list):
    delta = 0.0
    pull = 0

    for line in log_file:
        info = line.split()
        if info and info[0] == 'PULLED':
            for i in range(len(info)):
                var = info[i].strip('<>:,') 
                if var == "DELTA":
                    delta = float(info[i+1].strip('<>:,'))
                elif var == "PULLS":
                    pull = int(info[i+1].strip('<>:,'))
            delta_list.append((delta, pull))        
    log_file.seek(0, 0)

def parse_best_arm_deltas(log_file, best_delta_list):
    for line in log_file:
        info = line.split()
        if info and info[0] == 'BEST':
            for i in range(len(info)):
                var = info[i].strip('<>:,') 
                if var == "DELTA":
                    best_delta_list.append(float(info[i+1].strip('<>:,')))

def average_delta(d_list):
    return sum(d_list)/len(d_list)

def success_rate(delta_list, threshold):
    success = 0.0
    for delta in delta_list:
        if delta < threshold:
            success += 1.0
    return success / len(delta_list)

def main():
    # open log file, new output file
    if (len(sys.argv) > 2):
        log_file = open(sys.argv[1], 'r')
        #new_file = open(sys.argv[2], 'w')
    else:
        print("log file, and new file arguments are required, exiting...")
        sys.exit(0)

    delta_list = list()
    parse_deltas(log_file, delta_list)
    
    best_delta_list = list()
    threshold = 0.01
    parse_best_arm_deltas(log_file, best_delta_list)
    print("Average Best Arm Delta: %f" %(average_delta(best_delta_list)))
    print("Success Rate with threshold: %f, is: %f" 
            %(threshold, success_rate(best_delta_list, threshold)))

    # close 
    log_file.close()
    #new_file.close()    

if __name__=="__main__":
    main()
