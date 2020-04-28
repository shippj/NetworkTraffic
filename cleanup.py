import os
import mysql.connector
import sys
#import datetime

print("stopping sniffer service...")
os.system("systemctl stop sniffer")

print("Connecting to DB...\n")
mysql = mysql.connector.connect(
        host="127.0.0.1",
        user="sniffer",
        password="sniffer",
        database="traffic"
    );
print (mysql)

print("preparing sql cursor...")
c = mysql.cursor()

print("Finding DAY... ")
c.execute("select dayofyear(curdate()-1) as day")
r = c.fetchone()
day = r[0]
print(" day = " + str(day) )

print("Checking to make sure we dont already have reports for this day...")
c.execute("select count(*) from reports where day="+str(day))
r = c.fetchone()
if (r[0]>0) :
	print(" WE ALREADY DONE THIS REPORT!  ABORTING!")
	sys.exit(0)

print("Calculating new reports...")
c.execute("insert into reports select day, from_ip, to_ip, sum(size), count(*) from data where day = " + str(day) + " group by day, from_ip, to_ip");
r = c.fetchone()

print("Deleting data table...")
c.execute("delete from data")
r = c.fetchone()

print("Starting sniffer service...")
os.system("systemctl start sniffer")

print("Done!")

