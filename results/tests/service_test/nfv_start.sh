click_conf="/home/sdn/Desktop/2/application/nfv"
echo "reloading nfv log file"
touch /home/sdn/Desktop/2/results/ipsclick.log
chmod 755 /home/sdn/Desktop/2/results/ipsclick.log
cat /dev/null > /home/sdn/Desktop/2/results/ipsclick.log
touch /home/sdn/Desktop/2/results/dnsclick.log
chmod 755 /home/sdn/Desktop/2/results/dnsclick.log
cat /dev/null > /home/sdn/Desktop/2/results/dnsclick.log
touch /home/sdn/Desktop/2/results/wwwclick.log
chmod 755 /home/sdn/Desktop/2/results/wwwclick.log
cat /dev/null > /home/sdn/Desktop/2/results/wwwclick.log
touch /home/sdn/Desktop/2/results/natclick.log
chmod 755 /home/sdn/Desktop/2/results/natclick.log
cat /dev/null > /home/sdn/Desktop/2/results/natclick.log

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
