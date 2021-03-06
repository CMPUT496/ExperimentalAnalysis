import math
import sys
import operator
import numpy as np
import matplotlib.pyplot as plt

def parse_regrets(log_file):
    regret_list = list()
    pull_list = list()
    pull_dict = dict()
    pull_count = dict()
    log_file.seek(0, 0)

    for line in log_file:
        info = line.split()
        if info and info[0] == 'PULLED':
            for i in range(len(info)):
                var = info[i].strip('<>:,') 
                if var == "DELTA":
                    regret = float(info[i+1].strip('<>:,'))
                elif var == "PULLS":
                    pull = int(info[i+1].strip('<>:,'))
                    if pull_dict.has_key(pull):
                        pull_dict[pull] += regret 
                        pull_count[pull] += 1
                    else:
                        pull_dict[pull] = regret 
                        pull_count[pull] = 1
                        pull_list.append(pull)
    
    # iterate through and average deltas
    for pull in pull_list:
        regret = pull_dict[pull] / pull_count[pull]
        regret_list.append((regret, pull))        
    log_file.seek(0, 0)
    return regret_list 

def write_deltas_to_file(delta_file, timestep_file, delta_list, seqhav_flag):
    for delta in delta_list:
        delta_file.write(str(delta[0]) + "\n")
        if seqhav_flag:
            timestep_file.write(str(delta[1]) + "\n")

def parse_every_deltas(log_file, regret_file):
    log_file.seek(0,0)
    flag = False
    for line in log_file:
        info = line.split()
        if info and info[0] == 'PULLED':
            flag = True
            for i in range(len(info)):
                var = info[i].strip('<>:,')
                if var == "DELTA":
                    delta = float(info[i+1].strip('<>:,'))
                    regret_file.write("%f\n" %(delta))
        elif (info and info[0] != 'PULLED' and flag):
            flag = False
            regret_file.write('\n')
        else:
            flag = False

def parse_best_arm_deltas(log_file):
    best_delta_list = list()
    log_file.seek(0, 0)

    for line in log_file:
        info = line.split()
        if info and info[0] == 'BEST':
            for i in range(len(info)):
                var = info[i].strip('<>:,') 
                if var == "DELTA":
                    best_delta_list.append(float(info[i+1].strip('<>:,')))
    log_file.seek(0, 0)
    return best_delta_list

def parse_arm_distribution(log_file, arm_file, pull_count_file):
    arm_dict = dict()           # holds average configmu for an arm
    arm_count = dict()          # holds how many times an arm has occurred
    arm_pulls = dict()
    arm_list = list()           # holds list of all arms, used for iteration
    arm_configmus = list()      # the list of average configmus to be returned 
    
    log_file.seek(0,0)
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
                        arm_pulls[arm] = 0

    log_file.seek(0,0)
    for line in log_file:
        info = line.split()
        if info and info[0] == 'ARMPULLCOUNT:':
            arm = (info[1].strip('<,>') + info[2].strip('<,>') 
                    + info[3].strip('<,>') + info[4].strip('<,>') 
                    + info[5].strip('<,>'))
            arm_pulls[arm] += int(info[6].strip('<,>'))    

    for arm in arm_list:
        arm_configmus.append(arm_dict[arm] / arm_count[arm])
        arm_file.write(str(arm_dict[arm] / arm_count[arm]) + '\n')
        pull_count_file.write(str(arm_pulls[arm] / arm_count[arm]) + '\n')
        
    log_file.seek(0, 0)         # point to the start of the logfile
    return arm_configmus

def calculate_arm_stdev(arm_configmus):
    sample_mean = sum(arm_configmus) / len(arm_configmus)
    sum_error = 0.0
    for arm in arm_configmus:
        sum_error += (arm - sample_mean)**2
    st_dev = math.sqrt(sum_error/len(arm_configmus))    
    return st_dev

#def write_arms_to_file(arm_file, arm_configmus):
#    for arm in arm_configmus:
#        arm_file.write(str(arm) + '\n')

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
   
def main():
    # open log file, new output file
    if (len(sys.argv) > 2):
        alg = int(sys.argv[1])
        log_file = open('./raw_data/' + sys.argv[2] + '.log', 'r')
        summary_file = open('summaries/summary_' + sys.argv[2] + '.data', 'w')
        regret_file = open('regrets/regrets_' + sys.argv[2] + '.data', 'w')
        average_regret_file = open('average_regrets/average_regret_' + sys.argv[2] + '.data', 'w')
        arm_file = open('arm_distributions/arms_' + sys.argv[2] + '.data', 'w')
        arm_pull_file = open('arm_distributions/pullcount_' + sys.argv[2] + '.data', 'w')
        if alg == 1:
            timestep_file = open('timesteps_for_seqhav/timestep_' + sys.argv[2] + '.data', 'w')
    else:
        print("log file, and new file arguments are required, exiting...")
        sys.exit(0)

    # get the regrets for matthew
    parse_every_deltas(log_file, regret_file)

    # get average deltas per timestep
    delta_list = parse_regrets(log_file)
    if (alg == 1):
        write_deltas_to_file(average_regret_file, timestep_file, delta_list, True)
    else:
        write_deltas_to_file(average_regret_file, None, delta_list, False)
    
    # arm distributions (configmus)
    arm_dist = parse_arm_distribution(log_file, arm_file, arm_pull_file)
    
    # write_arms_to_file(arm_file, arm_dist)

    # deltas (regrets) of the best arms
    best_delta_list = parse_best_arm_deltas(log_file)
    write_summary_stats_to_file(summary_file, best_delta_list, arm_dist)

    # close 
    log_file.close()
    average_regret_file.close()
    regret_file.close()
    summary_file.close()    
    arm_file.close()
    arm_pull_file.close()
    if alg == 1:
        timestep_file.close()

if __name__=="__main__":
    main()
