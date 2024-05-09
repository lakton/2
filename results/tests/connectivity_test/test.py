#!/usr/bin/env python

import re

if __name__ == "__main__":
    flag = False
    results = []

    with open("/home/sdn/Desktop/2/results/ping.log", "r") as test:
        for line in test:
            if re.match(".*ping.*", line):
                results.append("=========================")
                results.append(line.strip())  # Добавление строки пинга

            elif re.match(".*connect:.*", line):
                results.append(line.strip())  # Добавление строки ошибки соединения

            elif re.match(".*ping statistics.*", line):
                results.append(line.strip())  # Добавление строки статистики пинга
                stats = next(test)  # Чтение следующей строки для получения статистики
                transmitted = int(re.search(r"transmitted = (\d+)", stats).group(1))
                received = int(re.search(r"received = (\d+)", stats).group(1))
                loss = re.search(r"packet loss percent = ([\d+%-]+)", stats).group(1)
                if "100%" in loss:
                    result = "FAIL"
                else:
                    result = "PASS"
                results.append("transmitted = " + str(transmitted))
                results.append("received = " + str(received))
                results.append("packet loss percent = " + loss)
                results.append(result)

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
