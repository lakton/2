import os
print('ANALYZER 5')

file = open("/home/sdn/Desktop/2/results/tests/service_test/resultservice.log", "a")
try:
    if os.stat("/home/sdn/Desktop/2/results/tests/service_test/63.pcap").st_size > 24:
        file.write("\nHTTP GET blocking test : PASS")
    else:
        file.write("\nHTTP GET blocking test : FAIL")
except OSError:
    file.write("Какая-то ошибка.. :(")

file.close()
