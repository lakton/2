import os
print('ANALYZER 4')

file = open("/home/sdn/Desktop/2/results/resultservice.log", "a")
file.write("\nips тест для заблокированных пакетов")
try:
    if os.stat("63.pcap").st_size > 24:
        file.write("\nHTTP PUT (blocked packet) test : PASS")
    else:
        file.write("\nHTTP PUT (blocked packet) test : FAIL")
except OSError:
    file.write("Какая-то ошибка.. :(")

file.close()
