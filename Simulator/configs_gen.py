#config_file = open("configs.txt", "w")
config_file = open("configs_extras.txt", "w")

for i in range(3):
    for w in range(5):
        for j in range(2):
            for k in range(2):
                for h in range (2):
                    # Start off fake variables
                    # Colour, Background, Animations
                    for a in range(4):
                        for b in range(2):
                            for c in range(2):
                                config_file.write("%d %d %d %d %d %d %d %d\n" %(i,w,j,k,h,a,b,c))           
                    #config_file.write("%d %d %d %d %d\n" %(i,w,j,k,h))
config_file.close()
