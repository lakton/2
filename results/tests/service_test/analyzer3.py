import os
print('ANALYZER 3')

file = open("/home/sdn/Desktop/2/results/resultservice.log", "a")

try:
    if os.stat("62.pcap").st_size > 24 and os.stat("63.pcap").st_size < 25:
        file.write("\nHTTP PUT (allowed packet) test : PASS")
    else:
        file.write("\nHTTP PUT (allowed packet) test : FAIL")
except OSError:
    file.write("Какая-то ошибка.. :(")

file.close()
