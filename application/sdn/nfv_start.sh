click_conf="/home/sdn/Desktop/2/application/nfv"
echo "reloading nfv log file"
# Очистка выводных файлов перед запуском скриптов
echo "" > /home/sdn/Desktop/2/results/ipsclick.log
echo "" > /home/sdn/Desktop/2/results/dnsclick.log
echo "" > /home/sdn/Desktop/2/results/wwwclick.log
echo "" > /home/sdn/Desktop/2/results/natclick.log

#Kill all first
echo "kill all click script"
pkill click

#Run every click instances
echo "запуск ips"
sudo /home/sdn/Desktop/fastclick/bin/click -f $click_conf/ips.click >> /home/sdn/Desktop/2/results/ipsclick.log 2>&1 &
echo "запуск DNS Load Balancer"
sudo /home/sdn/Desktop/fastclick/bin/click -f $click_conf/dns.click >> /home/sdn/Desktop/2/results/dnsclick.log 2>&1 &
echo "запуск WWW Load Balancer"
sudo /home/sdn/Desktop/fastclick/bin/click -f $click_conf/www.click >> /home/sdn/Desktop/2/results/wwwclick.log 2>&1 &
echo "запуск NAPT"
sudo /home/sdn/Desktop/fastclick/bin/click -f $click_conf/nat.click >> /home/sdn/Desktop/2/results/natclick.log 2>&1 &
echo "ВСЕ МОДУЛИ ЗАПУЩЕНЫ"
