#!/usr/bin/env python

import re

if __name__ == "__main__":
    node_flags = {"ws1": 0, "ds1": 0}
    test = open("/home/sdn/Desktop/2/results/ping.log", "r")
    results = []
    ping_data = []
    for line in test:
        if re.match("(.*)ping(.*)", line):
            if ping_data:
                results.extend(ping_data)
                ping_data = []
            results.append("=========================")
            results.append(line.strip())
        elif re.match(".*connect.*", line):
            results.append(line.strip())
        elif re.match("(.*)packet(.*)", line):
            work = line
            number = work.split()
            ping_data.append("transmitted = " + number[0])
            ping_data.append("received = " + number[3])
            transmitted = int(number[0])
            received = int(number[3])
            packet_loss_percent = (1 - received / transmitted) * 100
            ping_data.append("packet loss percent = " + f"{packet_loss_percent:.2f}%")
            if any(node_flags.values()):
                for node, flag in node_flags.items():
                    if flag == 1 or flag == 2 or flag == 3:
                        flag = 0
                        if 0 <= packet_loss_percent < 100 and node not in ["ws1", "ds1"]:
                            ping_data.append("FAIL")
                        else:
                            ping_data.append("PASS")
            else:
                if 0 <= packet_loss_percent < 100 and "ws1" not in line and "ds1" not in line:
                    ping_data.append("FAIL")
                else:
                    ping_data.append("PASS")
                    if "wwwlb" in line and 0 <= packet_loss_percent < 100:
                        ping_data.append("PASS")
                    else:
                        ping_data.append("FAIL")
    if ping_data:
        results.extend(ping_data)

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
