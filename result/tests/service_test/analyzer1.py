import os

print('ANALYZER 1')

file = open("/home/sdn/Desktop/2/results/tests/service_test/resultservice.log", "a")
file.write("\nips тест для разрешённых пакетов\n")

try:
    if os.stat("/home/sdn/Desktop/2/results/tests/service_test/62.pcap").st_size > 24:
        file.write("ARP PING test         : PASS")
    else:
        file.write("ARP PING test         : FAIL")
except OSError:
    file.write("Какая-то ошибка.. :(")

file.close()
