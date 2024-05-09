#!/usr/bin/env python

import re

if __name__ == "__main__":
    flag = 0
    test = open("/home/sdn/Desktop/2/results/ping.log", "r")
    results = []
    for line in test:
        print("Обрабатывается строка:", line.strip())  # Добавлено отладочное сообщение
        if re.match(".*ping.*", line):
            print("Совпадение с шаблоном 'ping'")  # Добавлено отладочное сообщение
            results.append("=========================")
        results.append(line.strip())  # Удаление символа новой строки для избежания лишних переносов строк
        if re.match(".*ws1.*", line) or re.match(".*ds1.*", line):
            if re.match(".*h1.*", line) or re.match(".*h2.*", line):
                flag = 1
            else:
                flag = 2

        if re.match(".*connect.*", line):
            results.append(line.strip())
            if re.match(".*packet.*", line):
                work = line
                number = work.split()
                results.append("Передано = " + number[0])
                results.append("Получено = " + number[3])
                if flag == 1:
                    flag = 0
                    results.append("Процент потерь = " + number[7])
                    if number[7] == "100%":
                        results.append("PASS")
                    else:
                        results.append("FAIL")
                elif flag == 2:
                    flag = 0
                    results.append("Процент потерь = " + number[5])
                    if number[5] == "100%":
                        results.append("PASS")
                    else:
                        results.append("FAIL")
                else:
                    results.append("Процент потерь = " + number[5])
                    if number[5] == "100%":
                        results.append("FAIL")
                    else:
                        results.append("PASS")

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
