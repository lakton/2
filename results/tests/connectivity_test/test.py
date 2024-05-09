#!/usr/bin/env python

import re

if __name__ == "__main__":
    test = open("/home/sdn/Desktop/2/results/ping.log", "r")
    results = []
    test_info = ""
    for line in test:
        if re.match("(.*)ping(.*)", line):
            if test_info:
                results.append(test_info)
            test_info = line.strip()
        elif re.match("=========================", line):
            results.append(line.strip())
        elif "DUP!" in line:
            continue
        else:
            test_info += "\n" + line.strip()

        if re.match(".*connect.*", line):
            if re.match(".*packet loss.*", line):
                packet_info = line.split()
                transmitted = packet_info[0]
                received = packet_info[3]
                loss_percent = packet_info[7] if packet_info[7] != "100%" else "+100"  # Handle the 100% loss case
                result = "transmitted = {}\nreceived = {}\npacket loss percent = {}\n".format(transmitted, received, loss_percent)
                if loss_percent == "+100":
                    result += "PASS"
                else:
                    result += "FAIL"
                results.append(result)

    # Добавляем последний блок теста
    if test_info:
        results.append(test_info)

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
