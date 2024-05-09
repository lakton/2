#!/usr/bin/env python

import re

if __name__ == "__main__":
    # Словарь для хранения флагов для каждого узла
    node_flags = {
        "ws1": 0, "ds1": 0, "h1": 0, "h2": 0, "h3": 0, "h4": 0, "dnslb": 0, "wwwlb": 0, "napt": 0
    }

    # Открываем файл с результатами ping-тестов для чтения
    test = open("/home/sdn/Desktop/2/results/ping.log", "r")
    results = []

    # Цикл по строкам в файле
    for line in test:
        # Проверяем, соответствует ли строка формату ping
        if re.match("(.*)ping(.*)", line):
            # Если есть данные о предыдущем ping-тесте, добавляем их к результатам
            if results:
                results.append("=========================")
                results.extend(ping_data)
                ping_data = []

            results.append(line.strip())  # Добавляем строку с заголовком ping-теста
        elif re.match(".*connect.*", line):
            results.append(line.strip())  # Добавляем строки о соединении
        elif re.match("(.*)packet(.*)", line):
            # Обрабатываем строку с данными о пакетах
            work = line
            number = work.split()
            transmitted = int(number[0])
            received = int(number[3])
            packet_loss_percent = (1 - received / transmitted) * 100

            # Проверяем условия для каждой пары узлов
            if "h3" in line or "h4" in line:
                if "ws1" in line or "ds1" in line:
                    if packet_loss_percent == 100:
                        results.append("PASS")
                    else:
                        results.append("FAIL")
                else:
                    if packet_loss_percent != 100:
                        results.append("PASS")
                    else:
                        results.append("FAIL")
            elif "h1" in line or "h2" in line:
                if "ws1" in line or "ds1" in line:
                    if packet_loss_percent == 100:
                        results.append("PASS")
                    else:
                        results.append("FAIL")
                else:
                    if packet_loss_percent != 100:
                        results.append("PASS")
                    else:
                        results.append("FAIL")
            else:
                if packet_loss_percent != 100:
                    results.append("PASS")
                else:
                    results.append("FAIL")

            # Форматируем данные о пакетах и добавляем их к результатам
            ping_data = [
                "--- " + number[1] + " ping statistics ---",
                "transmitted = " + number[0],
                "received = " + number[3],
                "packet loss percent = " + f"{packet_loss_percent:.2f}%"
            ]

    # Добавляем данные о последнем ping-тесте к результатам
    if ping_data:
        results.append("=========================")
        results.extend(ping_data)

    # Записываем результаты в файл
    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
