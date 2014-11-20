import sys

def parse_deltas(log_file, delta_list):
    for line in log_file:
        info = line.split()
        if info and info[0] == 'BEST':
            for i in range(len(info)):
                var = info[i].strip('<>,:') 
                if var == "DELTA":
                    delta_list.append(float(info[i+1].strip('<>,:')))
                    break

def average_delta(delta_list):
    return sum(delta_list)/len(delta_list)

def rate_of_success(delta_list, threshold):
    failures = 0.0
    for delta in delta_list:
        if delta > threshold:
            failures += 1.0
    return failures / len(delta_list)

def main():
    # open log file, new output file
    if (len(sys.argv) > 2):
        log_file = open(sys.argv[1], 'r')
        new_file = open(sys.argv[2], 'w')
    else:
        print("log file, and new file arguments are required, exiting...")
        sys.exit(0)

    delta_list = list()
    parse_deltas(log_file, delta_list)
    print("Average Delta: %f over %d runs" 
            %(average_delta(delta_list), len(delta_list)))
    print("Rate of failure: %f" %(rate_of_success(delta_list, 0.01)))

    # close 
    log_file.close()
    new_file.close()    

if __name__=="__main__":
    main()
