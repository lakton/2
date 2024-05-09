#!/usr/bin/env python

import re

if __name__ == "__main__":
    flag = 0
    test = open("ping.log", "r")
    for line in test:
        if re.match("(.*)ping(.*)", line):
            print("=========================")
        print(line)
        if re.match("(.*)ws1(.*)", line) or re.match("(.*)ds1(.*)", line):
            if re.match("(.*)h1(.*)", line) or re.match("(.*)h2(.*)", line):
                flag = 1
            else:
                flag = 2

        if re.match(".*connect.*", line):
            print(line)
            if re.match("(.*)packet(.*)", line):
                work = line
                number = work.split()
                print("передано = ", number[0])
                print("получено = ", number[3])
                if flag == 1:
                    flag = 0
                    print("процент пакет лосса = ", number[7])
                    if number[7] == "100%":
                        print("PASS")
                    else:
                        print("FAIL")
                elif flag == 2:
                    flag = 0
                    print("процент пакет лосса = ", number[5])
                    if number[5] == "100%":
                        print("PASS")
                    else:
                        print("FAIL")
                else:
                    print("процент пакет лосса = ", number[5])
                    if number[5] == "100%":
                        print("FAIL")
                    else:
                        print("PASS")
