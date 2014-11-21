import sys
import operator
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

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
    log_file.seek(0, 0)

def parse_arm_distribution(log_file):
    arm_dict = dict()
    arm_count = dict()
    arm_list = list()
    arm_deltas = list()
    
    for line in log_file:
        info = line.split()
        if info and info[0] == 'ARM:':
            arm = (info[1].strip('<,>') + info[2].strip('<,>') 
                    + info[3].strip('<,>') + info[4].strip('<,>') 
                    + info[5].strip('<,>'))
            for i in range(len(info)):
                var = info[i].strip('<>:,')
                if var == "CONFIGMU":
                    delta = float(info[i+1].strip('<>:,'))
                    if arm in arm_dict:
                        arm_count[arm] = arm_count[arm] + 1
                        arm_dict[arm] = (arm_dict[arm] + delta) / arm_count[arm]
                    else:
                        arm_list.append(arm)
                        arm_count[arm] = 1
                        arm_dict[arm] = delta
    for arm in arm_list:
        arm_deltas.append(arm_dict[arm])
    log_file.seek(0, 0)
    return arm_deltas

def average_delta(d_list):
    return sum(d_list)/len(d_list)

def success_rate(delta_list, threshold):
    success = 0.0
    for delta in delta_list:
        if delta < threshold:
            success += 1.0
    return success / len(delta_list)

def plot_egreedy_delta_progress(d_list, pp):
    d_list.sort(key=lambda x: x[1])
    deltas = list()
    pulls = list()

    delta_sum = 0.0
    count = 1
    for i in range(len(d_list)):
        delta_sum += d_list[i][0]
        print(d_list[i][0])
        if (i == len(d_list)-1 or d_list[i][1] == d_list[i+1][1]):
            count += 1
        else:
            deltas.append(delta_sum / count)
            pulls.append(d_list[i][1])
            delt_sum = 0.0
            count = 1
    
    plt.plot(pulls, deltas, '-')
    plt.axis([0,10000,0,0.5])
    plt.savefig(pp, format='pdf')

def plot_seqhav_delta_progress(d_list, pp):
    d_list.sort(key=lambda x: x[1])
    deltas = list()
    pulls = list()
    
    delta_sum = 0.0
    count = 1
    for i in range(len(d_list)):
        delta_sum += d_list[i][0]
        if (i == len(d_list)-1 or d_list[i][1] == d_list[i+1][1]):
            count += 1
        else:
            deltas.append(delta_sum / count)
            pulls.append(d_list[i][1])
            delta_sum = 0.0
            count = 1
    plt.plot(pulls, deltas, '-')
    plt.axis([0,10000,0,0.2])
    plt.savefig(pp, format='pdf')

def plot_arm_distribution(arm_dist, pp):
    val = 0.
    plt.plot(arm_dist, np.zeros_like(arm_dist) + val, 'o')
    plt.savefig(pp, format='pdf')
    
def main():
    # open log file, new output file
    if (len(sys.argv) > 3):
        alg = int(sys.argv[1])
        log_file = open(sys.argv[2], 'r')
        new_file = open(sys.argv[3], 'w')
        pp = PdfPages('plots_' + sys.argv[3]) 
    else:
        print("log file, and new file arguments are required, exiting...")
        sys.exit(0)

    # get how delta progresses over time (number of pulls)
    delta_list = list()
    parse_deltas(log_file, delta_list)
    
    # deltas (regrets) of the best arms
    best_delta_list = list()
    threshold = 0.01
    parse_best_arm_deltas(log_file, best_delta_list)

    # arm distributions (configmus)
    arm_dist = parse_arm_distribution(log_file)

    # summary statistics
    print("Average Best Arm Delta: %f" %(average_delta(best_delta_list)))
    print("Success Rate with threshold: %f, is: %f" 
            %(threshold, success_rate(best_delta_list, threshold)))
    
    # plot the graphs and save them to pdfs
    plot_arm_distribution(arm_dist, pp)
    if alg == 0:
        plot_egreedy_delta_progress(delta_list, pp)
    else:
        plot_seqhav_delta_progress(delta_list, pp)

    # close 
    log_file.close()
    new_file.close()    
    pp.close()

if __name__=="__main__":
    main()
