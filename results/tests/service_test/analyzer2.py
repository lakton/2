import os
print('ANALYZER 2')

file = open("/home/sdn/Desktop/2/results/resultservice.log", "a")

try:
    if os.stat("/home/sdn/Desktop/2/results/service_test/62.pcap").st_size > 24 and os.stat("/home/sdn/Desktop/2/results/service_test/63.pcap").st_size < 27:
        file.write("\nHTTP POST test        : PASS")
    else:
        file.write("\nHTTP POST test        : FAIL")
except OSError:
    file.write("Какая-то ошибка.. :(")

file.close()
