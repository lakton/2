click_conf="/home/sdn/Desktop/2/application/nfv"
echo "reloading nfv log file"
touch /var/log/ipsclick.log
chmod 755 /var/log/ipsclick.log
cat /dev/null > /var/log/ipsclick.log
touch /var/log/dnsclick.log
chmod 755 /var/log/dnsclick.log
cat /dev/null > /var/log/dnsclick.log
touch /var/log/wwwclick.log
chmod 755 /var/log/wwwclick.log
cat /dev/null > /var/log/wwwclick.log
touch /var/log/natclick.log
chmod 755 /var/log/natclick.log
cat /dev/null > /var/log/natclick.log

#Kill all first
echo "kill all click script"
pkill click

#Run every click instances
echo "starting ips"
sudo /home/sdn/Desktop/fastclick/bin/click -f $click_conf/ips.click >> /var/log/ipsclick.log 2>&1 &
echo "starting DNS Load Balancer"
sudo /home/sdn/Desktop/fastclick/bin/click -f $click_conf/dns.click >> /var/log/dnsclick.log 2>&1 &
echo "starting WWW Load Balancer"
sudo /home/sdn/Desktop/fastclick/bin/click -f $click_conf/www.click >> /var/log/wwwclick.log 2>&1 &
echo "starting NAPT"
sudo /home/sdn/Desktop/fastclick/bin/click -f $click_conf/nat.click >> /var/log/natclick.log 2>&1 &
echo "All Click Script are running"