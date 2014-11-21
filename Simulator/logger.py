import sim
import datetime

def open_log(file_name):
    log_file = open(file_name, "a+")

    # Header for the log file
    time = datetime.datetime.now()
    log_file.write("%s" %(time.strftime("%Y-%m-%d %H:%M:%S")))
    return log_file

def close_log(log_file):
    log_file.close()

def log_arms(log_file, arms):
    for arm in arms:
        log = ("ARM: %s\tCONFIGMU: %f\tDELTA: %f\n"
                %(str(arm), arm.get_config_mu(), arm.get_delta()))
        log_file.write(log)

def log_pulled_arm(log_file, arm, pulls):
    log = ("PULLED ARM: %s\tAVERAGE: %f\tCONFIGMU: %f\tDELTA: %f\t" \
            "NUM PULLS: %d\n" %(str(arm), arm.get_average(),
            arm.get_config_mu(), arm.get_delta(), pulls))
    log_file.write(log)

def log_best_arm(log_file, arm, pulls):
    log = ("BEST ARM: %s\tAVERAGE: %f\tCONFIGMU: %f\tDELTA: %f\t" \
            "NUM PULLS: %d\n" %(str(arm), arm.get_average(),
            arm.get_config_mu(), arm.get_delta(), pulls))
    log_file.write(log)
