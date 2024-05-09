import os
# print('ANALYZER 5')

file = open("/home/sdn/Desktop/2/results/resultservice.log", "a")
try:
    if os.stat("63.pcap").st_size > 24:
        file.write("\nHTTP GET blocking test : PASS")
    else:
        file.write("\nHTTP GET blocking test : FAIL")
except OSError:
    file.write("Some error happened")

file.close()
