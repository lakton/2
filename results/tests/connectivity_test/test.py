#!/usr/bin/env python

import re

if __name__ == "__main__":
    node_flags = {"ws1": 0, "ds1": 0}  # Словарь для хранения состояний флагов для каждой ноды
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
            transmitted = int(number[0])
            received = int(number[3])
            packet_loss = transmitted - received
            loss_percent = (packet_loss / transmitted) * 100
            ping_data.append("transmitted = " + str(transmitted))
            ping_data.append("received = " + str(received))
            ping_data.append("packet loss percent = " + "{:.2f}".format(loss_percent) + "%")
            if any(node_flags.values()):  # Если хотя бы для одной ноды флаг установлен, то оцениваем по PASS/FAIL
                for node, flag in node_flags.items():
                    if flag == 1:
                        flag = 0
                        if loss_percent == 0 and node != "ws1" and node != "ds1":
                            ping_data.append("PASS")
                        else:
                            ping_data.append("FAIL")
                    elif flag == 2:
                        flag = 0
                        if loss_percent == 0 and node != "ws1" and node != "ds1":
                            ping_data.append("PASS")
                        else:
                            ping_data.append("FAIL")
                    else:
                        if loss_percent == 0 and node != "ws1" and node != "ds1":
                            ping_data.append("PASS")
                        else:
                            ping_data.append("FAIL")
            else:
                if loss_percent == 0 and "ws1" not in line and "ds1" not in line:  # Учитываем случаи с ws1 и ds1
                    ping_data.append("PASS")
                else:
                    ping_data.append("FAIL")
    if ping_data:  # Добавляем оставшиеся данные из временного списка, если таковые имеются
        results.extend(ping_data)

    with open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for result in results:
            output_file.write(result + '\n')
