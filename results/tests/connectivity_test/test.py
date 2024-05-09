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
                stats = next(test)  # Чтение следующей строки для получения статистики
                transmitted = int(re.search(r"(\d+) packets transmitted", stats).group(1))
                received = int(re.search(r"(\d+) received", stats).group(1))
                loss_percent = re.search(r"([\d+.]+)% packet loss", stats).group(1)
                results.append("--- " + line.strip() + " ping statistics ---")
                results.append("transmitted = " + str(transmitted))
                results.append("received = " + str(received))
                results.append("packet loss percent = " + loss_percent + "%")
                if loss_percent == "100.0":
                    results.append("FAIL")
                else:
                    results.append("PASS")

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
