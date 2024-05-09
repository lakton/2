#!/usr/bin/env python

import re

if __name__ == "__main__":
    flag = 0
    test = open("/home/sdn/Desktop/2/results/ping.log", "r")
    results = []
    ping_data = []  # Создание временного списка для данных ping-сессий
    for line in test:
        if re.match("(.*)ping(.*)", line):
            if ping_data:  # Если временный список не пустой, добавляем его к результатам
                results.extend(ping_data)
                ping_data = []  # Очищаем временный список
            results.append("=========================")
            results.append(line.strip())
        elif re.match(".*connect.*", line):
            results.append(line.strip())
        elif re.match("(.*)packet(.*)", line):
            work = line
            number = work.split()
            ping_data.append("transmitted = " + number[0])
            ping_data.append("received = " + number[3])
            if flag == 1:
                flag = 0
                ping_data.append("packet loss percent = " + number[7])
                if number[7] == "100%":
                    ping_data.append("FAIL")
                else:
                    ping_data.append("PASS")
            elif flag == 2:
                flag = 0
                ping_data.append("packet loss percent = " + number[5])
                if number[5] == "100%":
                    ping_data.append("FAIL")
                else:
                    ping_data.append("PASS")
            else:
                ping_data.append("packet loss percent = " + number[5])
                if number[5] == "100%":
                    ping_data.append("FAIL")
                else:
                    ping_data.append("PASS")

    if ping_data:  # Добавляем оставшиеся данные из временного списка, если таковые имеются
        results.extend(ping_data)

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
