import logging
from io import StringIO
import scapy.all as scapy
import sys

# pcap file name
file = "72.pcap"

# Print pcap to screen and capture
# Source: http://stackoverflow.com/questions/29288848/get-info-string-from-scapy-packet
try:
    capture = StringIO()
    save_stdout = sys.stdout
    sys.stdout = capture
    scapy.rdpcap(file).show()
    sys.stdout = save_stdout
except Exception as e:
    print("Не удалось прочитать pcap файл:", e)

# Convert capture to string
raw_output = capture.getvalue()
with open("out1.txt", "w") as f1:
    f1.write(raw_output)

# Remove other packets
with open("out1.txt", "r") as f1, open("out2.txt", "w") as f2:
    source = "100.0.0.45"
    type = "PA"  # P for POST
    for line in f1:
        index1 = line.find(source)
        index2 = line.find(type)
        if 'http' in line and index1 == 22 and index2 == 57:
            f2.write(line)

# Check the sequence 40-41-42
with open("out2.txt", "r") as f2:
    result = 'PASS'
    first_line = f2.readline()
    previous = int(first_line[49:51])
    for line in f2:
        current = int(line[49:51])
        if current == 40:
            if previous == 42 or previous == 40:
                previous = current
                continue
            else:
                result = 'FAIL'
                break
        elif current == 41:
            if previous == 40 or previous == 41:
                previous = current
                continue
            else:
                result = 'FAIL'
                break
        elif current == 42:
            if previous == 41 or previous == 42:
                previous = current
                continue
            else:
                result = 'FAIL'
                break
        else:
            print("Ошибка здесь")

# Print result. Return "True" if round robin works properly
with open("/home/sdn/Desktop/2/results/resultservice.log", "a") as file:
    file.write("\n\nWWW LB round robin test : " + result)