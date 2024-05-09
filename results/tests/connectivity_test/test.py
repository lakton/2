#!/usr/bin/env python

import re
import sys

if __name__ == "__main__":
    flag = 0
    test = open("/home/sdn/Desktop/2/results/ping.log", "r")
    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        sys.stdout = output_file  # Перенаправление стандартного вывода в файл
        for line in test:
            if re.match("(.*)ping(.*)", line):
                print("=========================")
            print(line.strip())  # Удаление символа новой строки для избежания лишних переносов строк
            if re.match("(.*)ws1(.*)", line) or re.match("(.*)ds1(.*)", line):
                if re.match("(.*)h1(.*)", line) or re.match("(.*)h2(.*)", line):
                    flag = 1
                else:
                    flag = 2

            if re.match(".*connect.*", line):
                print(line.strip())
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
