config_file = open("configs.txt", "w")

for i in range(3):
    for j in range(2):
        for k in range(2):
            for h in range (2):
                config_file.write("%d %d %d %d\n" %(i,j,k,h))
config_file.close()
