app:
		@sudo python3 /home/sdn/Desktop/2/application/sdn/pox.py controller log --file=/home/sdn/Desktop/2/results/pox.log,w samples.pretty_log log.level --DEBUG
click:
		@sudo /home/sdn/Desktop/fastclick/bin/click -f /home/sdn/Desktop/2/application/nfv/ips.click >> /home/sdn/Desktop/2/results/ipsclick.log 2>&1 &
		@sudo /home/sdn/Desktop/fastclick/bin/click -f /home/sdn/Desktop/2/application/nfv/dns.click >> /home/sdn/Desktop/2/results/dnsclick.log 2>&1 &
		@sudo /home/sdn/Desktop/fastclick/bin/click -f /home/sdn/Desktop/2/application/nfv/www.click >> /home/sdn/Desktop/2/results/wwwclick.log 2>&1 &
		@sudo /home/sdn/Desktop/fastclick/bin/click -f /home/sdn/Desktop/2/application/nfv/nat.click >> /home/sdn/Desktop/2/results/natclick.log 2>&1 &
clean:
		@echo -n "[MAKE] Killing POX..      "
		@(sudo kill -s SIGINT $$(ps aux | grep pox | grep root | head -n 1 | awk '{print $$2}') 2>/dev/null  && echo "OK") || echo "POX not running!"
		@echo -n "[MAKE] Killing Click..    "
		@sudo pkill --signal SIGINT click && echo "OK" || echo "Click not running!"
		@echo -n "[MAKE] Killing SDN App..  "
		@(sudo kill -s SIGTERM $$(ps aux | grep sdn | grep root | head -n 1 | awk '{print $$2}')  2>/dev/null && echo "OK") || echo "SDN not running!"
		@sudo mn -c