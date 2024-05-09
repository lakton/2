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
                total_tests += 1/2
                
            if re.match("(.*)ws1(.*)", line) or re.match("(.*)ds1(.*)", line):
                if re.match("(.*)h1(.*)", line) or re.match("(.*)h2(.*)", line):
                    flag = 1
                else:
                    flag = 2

            if re.match(".*()connect(.*)", line):
                output_file.write(line)
                
            if re.match("(.*)packet(.*)", line):
                work = line
                number = work.split()
                output_file.write("Пакетов отправлено = " + number[0] + "\n")
                output_file.write("Пакетов принято = " + number[3] + "\n")
                if flag == 1:
                    flag = 0
                    output_file.write("Процент потерь пакетов = " + number[7] + "\n")
                    if number[7] == "100%":
                        output_file.write("PASS\n")
                        correct_tests += 1
                    else:
                        output_file.write("FAIL\n")
                        incorrect_tests += 1
                elif flag == 2:
                    flag = 0
                    output_file.write("Процент потерь пакетов = " + number[5] + "\n")
                    if number[5] == "100%":
                        output_file.write("PASS\n")
                        correct_tests += 1
                    else:
                        output_file.write("FAIL\n")
                        incorrect_tests += 1
                else:
                    output_file.write("Процент потерь пакетов = " + number[5] + "\n")
                    if number[5] == "100%":
                        output_file.write("FAIL\n")
                        incorrect_tests += 1
                    else:
                        output_file.write("PASS\n")
                        correct_tests += 1

        # Запись информации о количестве тестов и количестве корректных и некорректных результатов
        output_file.write("\n=========================\n")
        output_file.write("Общее количество тестов: {}\n".format(total_tests))
        output_file.write("Количество корректных результатов: {}\n".format(correct_tests))
        output_file.write("Количество некорректных результатов: {}\n".format(incorrect_tests))
