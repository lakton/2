app:werf
		@cd /home/sdn/Desktop/2/ik2220-assign-team9/application/sdn && sudo make app

topo:
		@cd /home/sdn/Desktop/2/ik2220-assign-team9/topology/ && sudo make topo

clean:
		@sudo mn -c
		@echo -n "[MAKE] Killing POX..      " 
		@(sudo kill -s SIGINT $$(ps aux | grep pox | grep root | head -n 1 | awk '{print $$2}') 2>/dev/null  && echo "OK") || echo "POX not running!"
		@echo -n "[MAKE] Killing Click..    "
		@sudo pkill --signal SIGINT click && echo "OK" || echo "Click not running!"