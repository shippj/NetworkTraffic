# NetworkTraffic
Useful for seeing which devices on a LAN are hogging the ISP’s monthly data allowance.  It records network data usage 24/7 and makes the reports viewable in a web browser.

TODO:
- make index.php sql-injection proof
- survive newyears


This project collects source and destination IPs and port numbers from a network and writes it to a MySQL/MariaDB server.  Then, you can use the PHP script to see which IP numbers are hogging the data usage.  It can run 24/7 for years without interruption. It doesn’t currently support IPv6 but I’ll probably be adding that one day.


Requirements:
- A computer with python, mysql/mariadb, php, and web server such as apache.  A headless core2duo with 1GB ram can handle at least 100mbit/s.
- Either a managed ethernet switch that supports port mirroring so you can mirror all packets to the sniffer computer, or 2 network ports in your computer setup as an ethernet bridge.


Setup:
- Create a new database in your sql server named "traffic".
- Execute the traffic.sql to create the table structures.
- Edit sniffer.py to adjust the SQL user/pass, and run it in screen or make a systemd/sysvinit service for it.
- Put your network interface in promiscuous mode.  On Debian, you can use “ip link” to see your interfaces, then use “ip link set eth0 promisc on” to set the interface to promiscuous mode.  (replace eth0 with your interface name)
- Edit cleanup.py to adjust the SQL user/pass, and put it in crontab to run every day at midnight.  This consolidates the SQL records which makes it possible to record years of data, and also makes the reports faster.
- Edit index.php to adjust the SQL user/pass and move it to a folder where it can be served from your webserver.  Apache on Debian uses /var/www/html
