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
            results.append(line.strip())
        if re.match(".*ping statistics.*", line):
            work = line
            number = work.split()
            results.append("=========================")
            results.append(line.strip())
            results.append("transmitted = " + number[0])
            results.append("received = " + number[3])
            if "%" in line:
                packet_loss = re.search(r"(\d+)%", line)
                if packet_loss:
                    loss_percent = packet_loss.group(1)
                    results.append("packet loss percent = " + loss_percent + "%")
                    if int(loss_percent) == 0:
                        results.append("PASS")
                    else:
                        results.append("FAIL")
            else:
                results.append("packet loss percent = 0%")
                results.append("PASS")
        if re.match("connect: Network is unreachable", line):
            results.append(line.strip())
            results.append("FAIL")
        if re.match(".*ws1.*", line) or re.match(".*ds1.*", line):
            if re.match(".*h1.*", line) or re.match(".*h2.*", line):
                flag = 1
            else:
                flag = 2

    test.close()

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
