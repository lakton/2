# README
## Mininet POX
- `make topo` - **topo**
- `make clean` - **clean** ALL
- `make app` - **pox.py** находится в `/2/application/sdn/pox.py`

## Журналы вывода генерируются в каталоге `</var/log>`:
- `pox.log` -> журнал **pox**
- `ipsclick.log` -> журнал **ips**
- `dnsclick.log` -> журнал **dns lb (lb1)**
- `wwwclick.log` -> журнал **www lb (lb2)**
- `natclick.log` -> журнал **napt**

## Результат
### Содержит два тестовых случая:

#### 1. Тест связности
   - `connectivity.sh` -> **сценарий для запуска тестов связности между хостами и/или серверами и/или балансировщиками нагрузки**
   - `ping.log` -> вывод **stdout** из `connectivity.sh`, перенаправленный **в файл**
   - `test.py` -> сценарий на Python для **разбора stdout (ping.log) в удобный для восприятия результат**
   - `connectivity_test_results` -> **выходные результаты для всех тестов выше**

#### 2. Тест служб

**Тесты служб можно выполнить, запустив `service.sh`. 
Он будет тестировать следующее:**

   - Функциональность сервера **DNS**
   - Функциональность веб-сервера **WWW**
   - Функциональность round-robin **LB**
   - Функциональность **ips**, содержит **5 тестов**

#### Файлы:
   ##### Сводки, результаты, выводы:
- `resultservice.log` -> **Содержит сводку результатов всех тестов служб** (PASS или FAIL)
- `service.log` -> Содержит файл журнала тестов служб.
- `servicedns.log`-> Содержит результат команды **dig** в тесте 1 (тест функциональности **DNS**)
- `servicewww.log` -> Содержит результат команды **curl** в тесте 2 (тест функциональности веб-сервера **WWW**)
   ##### Анализаторы и тесты:
- `servdnschecker.py` -> Содержит скрипт анализатора для определения успешности или неуспешности теста 1 (тест функциональности **DNS**).
- `servwwwchecker.py` -> Содержит скрипт анализатора для определения успешности или неуспешности теста 2 (тест функциональности веб-сервера **WWW**).
- `rrdnschecker.py` -> Содержит скрипт анализатора для определения успешности или неуспешности теста 3 (тест функциональности round-robin **LB**).
- `analyzer1.py` to `analyzer5.py` -> Содержат скрипты анализаторов для определения успешности или неуспешности теста функциональности **ips**. Есть 5 файлов, по одному для каждого теста в функциональности ips.
   ##### Дополнительный анализ трафика:
- `61.pcap` -> Содержит файл захвата **tcpdump** для **s6-eth1 (ips, интерфейс, обращенный к SW2)** -> этот файл будет всегда перезагружаться при каждом запуске теста ips
- `62.pcap` -> Содержит файл захвата **tcpdump** для *s6-eth2 (ips, интерфейс, обращенный к LB2)* -> этот файл будет всегда перезагружаться при каждом запуске теста ips
- `63.pcap` -> Содержит файл захвата **tcpdump** для *s6-eth3 (ips, интерфейс, обращенный к INSP)* -> этот файл будет всегда перезагружаться при каждом запуске теста ips
- `71.pcap` -> Содержит файл захвата **tcpdump** для **s7-eth1 (LB2, интерфейс, обращенный к ips)**
- `72.pcap` -> Содержит файл захвата **tcpdump** для **s7-eth2 (LB2, интерфейс, обращенный к SW4)**
- `insptest1.pcap` -> Содержит файл захвата **tcpdump** для h11-eth0 (**INSP**) во время теста *ips* 1
- `insptest2.pcap` -> Содержит файл захвата **tcpdump** для h11-eth0 (**INSP**) во время теста *ips* 2
- `insptest3.pcap` -> Содержит файл захвата **tcpdump** для h11-eth0 (**INSP**) во время теста *ips* 3
- `insptest4.pcap` -> Содержит файл захвата **tcpdump** для h11-eth0 (**INSP**) во время теста *ips* 4
- `insptest5.pcap` -> Содержит файл захвата **tcpdump** для h11-eth0 (**INSP**) во время теста *ips* 5

### Результат 2

**Набор файлов, которые оценивают производительность каждой сетевой функции на основе (Fast)Click. 
Фактически все они реализованы вместе с конфигурацией (Fast)Click в каждого модуля. 
Существует два вида файлов:**

- `<service>.report` -> образец отчета для каждого модуля
- `<service>.click`-> конфигурация (Fast)Click для каждого модуля. Как требуется в документе, файл отчета генерируется после завершения работы модуля (Fast)Click.
