import re

flag = 0
total_tests = 0
correct_tests = 0
incorrect_tests = 0

if __name__ == "__main__":
    with open("/home/sdn/Desktop/2/results/ping.log", "r") as test, open("/home/sdn/Desktop/2/results/connectivity_test_results", "w") as output_file:
        for line in test:
            if re.match("(.*)ping(.*)", line):
                output_file.write("=========================\n")
                output_file.write(line)
                total_tests += 1
                
            if re.match("(.*)ws1(.*)", line) or re.match("(.*)ds1(.*)", line):
                if re.match("(.*)h1(.*)", line) or re.match("(.*)h2(.*)", line):
                    flag = 1
                else:
                    flag = 2
            if re.match("(.*)unreachable(.*)", line):
                    output_file.write("PASS\n")
                    correct_tests += 1
                    continue
            if re.match(".*()connect(.*)", line):
                output_file.write(line)
            
            if re.match("(.*)packet(.*)", line):
                work = line
                numbers = re.findall(r'\d+', work)  # Извлечение всех чисел из строки
                transmitted = int(numbers[0])
                received = int(numbers[1])
                
                output_file.write("Пакетов отправлено = " + str(transmitted) + "\n")
                output_file.write("Пакетов принято = " + str(received) + "\n")
                
                if flag == 1:
                    flag = 0
                    packet_loss = ((transmitted - received) / transmitted) * 100
                    output_file.write("Процент потерь пакетов = {:.2f}%\n".format(packet_loss))
                    if packet_loss == 100:
                        output_file.write("PASS\n")
                        correct_tests += 1
                    else:
                        output_file.write("FAIL\n")
                        incorrect_tests += 1
                elif flag == 2:
                    flag = 0
                    packet_loss = ((transmitted - received) / transmitted) * 100
                    output_file.write("Процент потерь пакетов = {:.2f}%\n".format(packet_loss))
                    if packet_loss == 100:
                        output_file.write("PASS\n")
                        correct_tests += 1
                    else:
                        output_file.write("FAIL\n")
                        incorrect_tests += 1
                else:
                    packet_loss = ((transmitted - received) / transmitted) * 100
                    output_file.write("Процент потерь пакетов = {:.2f}%\n".format(packet_loss))
                    if packet_loss == 100:
                        output_file.write("FAIL\n")
                        incorrect_tests += 1
                    else:
                        output_file.write("PASS\n")
                        correct_tests += 1

        # Write summary of test results
        output_file.write("\n=========================\n")
        if incorrect_tests == 0:
            output_file.write("Все тесты прошли успешно\n")
        else:
            output_file.write("НЕ все тесты прошли успешно\n")
        output_file.write("\n=========================\n")
        output_file.write("Общее количество тестов: {}\n".format(total_tests // 2))
        output_file.write("Количество корректных результатов: {}\n".format(correct_tests))
        output_file.write("Количество некорректных результатов: {}\n".format(incorrect_tests))
