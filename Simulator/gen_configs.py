cfile = open("configs.txt", "w")

for a1 in range(3): #hints
    for a2 in range(6):
        for a3 in range(2):
            for a4 in range(2):
                for a5 in range(2):
                    line = "%s %s %s %s %s\n" %(a1, a2, a3, a4, a5)
                    cfile.write(line)

cfile.close()
