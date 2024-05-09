#!/usr/bin/env python

import re

if __name__ == "__main__":
    flag = 0
    test = open("/home/sdn/Desktop/2/results/ping.log", "r")
    results = []
    for line in test:
        if re.match("(.*)ping(.*)", line):
            results.append("=========================")
            results.append(line.strip())
        elif re.match(".*connect.*", line):
            results.append(line.strip())
        elif re.match("(.*)packet(.*)", line):
            work = line
            number = work.split()
            results.append("transmitted = " + number[0])
            results.append("received = " + number[3])
            if re.match("(.*)ws1(.*)", line) or re.match("(.*)ds1(.*)", line):
                if re.match("(.*)h1(.*)", line) or re.match("(.*)h2(.*)", line):
                    flag = 1
                else:
                    flag = 2
            if flag == 1:
                flag = 0
                results.append("packet loss percent = " + number[7])
                if number[7] == "100%":
                    results.append("FAIL")
                else:
                    results.append("PASS")
            elif flag == 2:
                flag = 0
                results.append("packet loss percent = " + number[5])
                if number[5] == "100%":
                    results.append("FAIL")
                else:
                    results.append("PASS")
            else:
                results.append("packet loss percent = " + number[5])
                if number[5] == "100%":
                    results.append("FAIL")
                else:
                    results.append("PASS")

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
