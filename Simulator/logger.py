import sim

def open_log(file_name):
    log_file = open(file_name, "a+")
    return log_file

def close_log(log_file):
    log_file.close()

def log_arms(log_file, arms):
    for arm in arms:
        log = ("ARM: %s\tCONFIGMU: %f\tDELTA: %f\n" 
                %(str(arm), arm.get_config_mu(), arm.get_delta()))
        log_file.write(log) 

def log_best_arm(log_file, arm, pulls):
    log = ("\nBEST ARM: %s\tAVERAGE: %f\tCONFIGMU: %f\tDELTA: %f\t" \
            "NUM PULLS: %d\n" %(str(arm), arm.get_average(),
            arm.get_config_mu(), arm.get_delta(), pulls))
    log_file.write(log)

