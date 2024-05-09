import logging
from io import StringIO
import scapy.all as scapy
import sys

# pcap file name
file = "52.pcap"

# Print pcap to screen and capture
# Source: http://stackoverflow.com/questions/29288848/get-info-string-from-scapy-packet
try:
    capture = StringIO()
    save_stdout = sys.stdout
    sys.stdout = capture
    scapy.rdpcap(file).show()
    sys.stdout = save_stdout
except:
    print("Error reading pcap file")

# Convert capture to string
rawoutput = capture.getvalue()
f1 = open("outdns1.txt", "w")
f1.write(rawoutput)
f1.close()

# Remove other packets
with open("outdns1.txt", "r") as f1, open("outdns2.txt", "w") as f2:
    source = "100.0.0.25"
    type = "PA"  # P for POST
    for line in f1:
        index1 = line.find(source)
        index2 = line.find(type)
        if 'http' in line and index1 == 22 and index2 == 57:
            f2.write(line)

# Check the sequence 40-41-42
with open("outdns2.txt", "r") as f2:
    is_consecutive = True
    first_line = f2.readline()
    previous = int(first_line[49:51])
    for line in f2:
        current = int(line[49:51])
        if current == 40:
            if previous == 42 or previous == 40:
                previous = current
                continue
            else:
                is_consecutive = False
                break
        elif current == 41:
            if previous == 40 or previous == 41:
                previous = current
                continue
            else:
                is_consecutive = False
                break
        elif current == 42:
            if previous == 41 or previous == 42:
                previous = current
                continue
            else:
                is_consecutive = False
                break
        else:
            is_consecutive = False
            print("Error here")

# Print result. Return "True" if round robin works properly
print(is_consecutive)
