#!/usr/bin/env python

import re

if __name__ == "__main__":
    flag = 0
    test = open("/home/sdn/Desktop/2/results/ping.log", "r")
    results = []
    for line in test:
        print("Processing line:", line.strip())  # Добавлено отладочное сообщение
        if re.match("(.*)ping(.*)", line):
            print("Matched 'ping' pattern")  # Добавлено отладочное сообщение
            results.append("=========================")
        # Убираем строки с пакетами DUP!
        if "DUP!" in line:
            print("Skipping line with DUP!")  # Добавлено отладочное сообщение
            continue
        results.append(line.strip())  # Удаление символа новой строки для избежания лишних переносов строк
        if re.match("(.*)ws1(.*)", line) or re.match("(.*)ds1(.*)", line):
            print("Matched 'ws1' or 'ds1' pattern")  # Добавлено отладочное сообщение
            if re.match("(.*)h1(.*)", line) or re.match("(.*)h2(.*)", line):
                flag = 1
            else:
                flag = 2

        if re.match(".*connect.*", line):
            print("Matched 'connect' pattern")  # Добавлено отладочное сообщение
            results.append(line.strip())
            if re.match("(.*)packet(.*)", line):
                print("Matched 'packet' pattern")  # Добавлено отладочное сообщение
                work = line
                number = work.split()
                results.append("передано = " + number[0])
                results.append("получено = " + number[3])
                if flag == 1:
                    flag = 0
                    results.append("процент пакет лосса = " + number[7])
                    if number[7] == "100%":
                        results.append("PASS")
                    else:
                        results.append("FAIL")
                elif flag == 2:
                    flag = 0
                    results.append("процент пакет лосса = " + number[5])
                    if number[5] == "100%":
                        results.append("PASS")
                    else:
                        results.append("FAIL")
                else:
                    results.append("процент пакет лосса = " + number[5])
                    if number[5] == "100%":
                        results.append("FAIL")
                    else:
                        results.append("PASS")

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
