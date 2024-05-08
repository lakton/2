app:
	@sudo python3 pox.py controller samples.pretty_log log.level --DEBUG >> /var/log/pox.log 2>&1 &
clean:
	@echo -n "[MAKE] Killing POX..      " 
	@(sudo kill -s SIGINT $$(ps aux | grep pox | grep root | head -n 1 | awk '{print $$2}') 2>/dev/null  && echo "OK") || echo "POX not running!"
	@echo -n "[MAKE] Killing Click..    "
	@sudo pkill --signal SIGINT click && echo "OK" || echo "Click not running!"
	@sudo mn -c