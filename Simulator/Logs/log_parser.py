import math
import sys
import operator
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def parse_deltas(log_file):
    delta_list = list()
    pull_list = list()
    pull_dict = dict()
    pull_count = dict()

    for line in log_file:
        info = line.split()
        if info and info[0] == 'PULLED':
            for i in range(len(info)):
                var = info[i].strip('<>:,') 
                if var == "DELTA":
                    delta = float(info[i+1].strip('<>:,'))
                elif var == "PULLS":
                    pull = int(info[i+1].strip('<>:,'))
                    if pull_dict.has_key(pull):
                        pull_dict[pull] += delta
                        pull_count[pull] += 1
                    else:
                        pull_dict[pull] = delta
                        pull_count[pull] = 1
                        pull_list.append(pull)
    
    # iterate through and average deltas
    for pull in pull_list:
        delta = pull_dict[pull] / pull_count[pull]
        delta_list.append((delta, pull))        
    log_file.seek(0, 0)
    return delta_list

def write_deltas_to_file(delta_file, timestep_file, delta_list):
    for delta in delta_list:
        delta_file.write(str(delta[0]) + "\n")
        timestep_file.write(str(delta[1]) + "\n")

def parse_all_arm_deltas(log_file, out_file):
    flag = False

    for line in log_file:
        info = line.split()
        if info and info[0] == 'ARM:':
            flag = True
            for i in range(len(info)):
                var = info[i].strip('<>:,')
                if var == "DELTA":
                    delta = float(info[i+1].strip('<>:,'))
                    out_file.write("%f\n" %(delta))
        elif (info and info[0] != 'ARM:' and flag):
            flag = False
            out_file.write('\n')
        else:
            flag = False

def parse_best_arm_deltas(log_file):
    best_delta_list = list()

    for line in log_file:
        info = line.split()
        if info and info[0] == 'BEST':
            for i in range(len(info)):
                var = info[i].strip('<>:,') 
                if var == "DELTA":
                    best_delta_list.append(float(info[i+1].strip('<>:,')))
    log_file.seek(0, 0)
    return best_delta_list

def parse_arm_distribution(log_file):
    arm_dict = dict()           # holds average configmu for an arm
    arm_count = dict()          # holds how many times an arm has occurred
    arm_list = list()           # holds list of all arms, used for iteration
    arm_configmus = list()      # the list of average configmus to be returned 
    
    for line in log_file:
        info = line.split()
        if info and info[0] == 'ARM:':
            arm = (info[1].strip('<,>') + info[2].strip('<,>') 
                    + info[3].strip('<,>') + info[4].strip('<,>') 
                    + info[5].strip('<,>'))
            for i in range(len(info)):
                var = info[i].strip('<>:,')
                if var == "CONFIGMU":
                    configmu = float(info[i+1].strip('<>:,'))
                    if arm in arm_dict:
                        arm_count[arm] = arm_count[arm] + 1
                        arm_dict[arm] += configmu 
                    else:
                        arm_list.append(arm)
                        arm_count[arm] = 1
                        arm_dict[arm] = configmu 
    for arm in arm_list:
        arm_configmus.append(arm_dict[arm] / arm_count[arm])
    log_file.seek(0, 0)         # point to the start of the logfile
    return arm_configmus

def calculate_arm_stdev(arm_configmus):
    sample_mean = sum(arm_configmus) / len(arm_configmus)
    sum_error = 0.0
    for arm in arm_configmus:
        sum_error += (arm - sample_mean)**2
    st_dev = math.sqrt(sum_error/len(arm_configmus))    
    return st_dev

def write_arms_to_file(arm_file, arm_configmus):
    for arm in arm_configmus:
        arm_file.write(str(arm) + '\n')

def average_delta(d_list):
    return sum(d_list)/len(d_list)

def success_rate(delta_list, threshold):
    success = 0.0
    for delta in delta_list:
        if delta < threshold:
            success += 1.0
    return success / len(delta_list)

def write_summary_stats_to_file(summary_file, best_delta_list, arm_configmus):
    # summary statistics
    threshold = 0.01
    summary_file.write("Average Best Arm Delta: %f\n" 
            %(average_delta(best_delta_list)))
    summary_file.write("Success Rate with threshold: %f, is: %f\n" 
            %(threshold, success_rate(best_delta_list, threshold)))

    sample_mean = sum(arm_configmus) / len(arm_configmus)
    st_dev = calculate_arm_stdev(arm_configmus)
    summary_file.write("Arms Sample Mean: %f\n" %(sample_mean))
    summary_file.write("Arms Standard Deviation: %f\n" %(st_dev))

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
    plt.axis([0,1,-1,1])
    plt.savefig(pp, format='pdf')
    
def main():
    # open log file, new output file
    if (len(sys.argv) > 3):
        alg = int(sys.argv[1])
        log_file = open(sys.argv[2], 'r')
        summary_file = open(sys.argv[3], 'w')
        delta_file = open('deltas_' + sys.argv[3], 'w')
        regret_file = open('regrets_' + sys.argv[3], 'w')
        timestep_file = open('timestep_' + sys.argv[3], 'w')
        arm_file = open('arms_' + sys.argv[3], 'w')
        # pp = PdfPages('plots_' + sys.argv[3]) 
    else:
        print("log file, and new file arguments are required, exiting...")
        sys.exit(0)

    # get the regrets for matthew
    parse_all_arm_deltas(log_file, regret_file)

    # get how delta progresses over time (number of pulls)
    delta_list = parse_deltas(log_file)
    write_deltas_to_file(delta_file, timestep_file, delta_list)
    
    # arm distributions (configmus)
    arm_dist = parse_arm_distribution(log_file)
    write_arms_to_file(arm_file, arm_dist)

    # deltas (regrets) of the best arms
    best_delta_list = parse_best_arm_deltas(log_file)
    write_summary_stats_to_file(summary_file, best_delta_list, arm_dist)

    # plot the graphs and save them to pdfs
    # plot_arm_distribution(arm_dist, pp)
    # if alg == 0:
    #     plot_egreedy_delta_progress(delta_list, pp)
    # else:
    #     plot_seqhav_delta_progress(delta_list, pp)

    # close 
    log_file.close()
    regret_file.close()
    summary_file.close()    
    delta_file.close()
    timestep_file.close()
    arm_file.close()
    # pp.close()

if __name__=="__main__":
    main()
