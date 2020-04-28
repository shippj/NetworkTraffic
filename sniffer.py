#https://www.binarytides.com/python-packet-sniffer-code-linux/
import socket, sys
from struct import *
import mysql.connector
import datetime

#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b

#create a AF_PACKET type raw socket (thats basically packet level)
try:
	s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
except socket.error , msg:
	print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

# open mysql for writing
mysql = mysql.connector.connect(
        host="127.0.0.1",
        user="sniffer",
        password="sniffer",
        database="traffic"
    );
print (mysql)

#prepare sql cursor
mycursor = mysql.cursor()
sql = "INSERT INTO data (day, hour, minute, from_ip, from_port, to_ip, to_port, size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

#prepare vars for storing last packet info
last_si = ""
last_sp = 0
last_di = ""
last_dp = 0
last_size = 0

#sys.exit()


# receive a packet
while True:
	packet = s.recvfrom(65565)
	packet = packet[0]
	eth_length = 14
	eth_header = packet[:eth_length]
	eth = unpack('!6s6sH' , eth_header)
	eth_protocol = socket.ntohs(eth[2])
#	print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)

	#Parse IP packets, IP Protocol number = 8
	if eth_protocol == 8 :
		#Parse IP header
		ip_header = packet[eth_length:20+eth_length]
		iph = unpack('!BBHHHBBH4s4s' , ip_header)
		version_ihl = iph[0]
		version = version_ihl >> 4
		ihl = version_ihl & 0xF
		iph_length = ihl * 4
		ttl = iph[5]
		protocol = iph[6]
		s_addr = socket.inet_ntoa(iph[8]);
		d_addr = socket.inet_ntoa(iph[9]);

		#filters
		if str(s_addr) == "127.0.0.1" : continue
		if str(d_addr) == "127.0.0.1" : continue

#		print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)

		#get current date and time
		now = datetime.datetime.now()

		#TCP protocol
		if protocol == 6 :
			t = iph_length + eth_length
			tcp_header = packet[t:t+20]

			#now unpack them :)
			tcph = unpack('!HHLLBBHHH' , tcp_header)
			
			source_port = tcph[0]
			dest_port = tcph[1]
#			print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)

		#UDP packets
		elif protocol == 17 :
			u = iph_length + eth_length
			udph_length = 8
			udp_header = packet[u:u+8]

			#now unpack them :)
			udph = unpack('!HHHH' , udp_header)
			
			source_port = udph[0]
			dest_port = udph[1]
#			length = udph[2]
#			checksum = udph[3]
			
#			print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum) + ' LenPacket: ' + str(len(packet))
		else:
			continue

		if (source_port==last_sp) and (dest_port==last_dp) and (s_addr==last_si) and (d_addr==last_di):
			last_size+=len(packet)
		else:
			val = (int(now.strftime("%j")), now.hour, now.minute,
			 str(last_si), int(last_sp), str(last_di), int(last_dp), last_size)
#			print(val)

			mycursor.execute(sql,val)
#			mysql.commit()

			last_size = len(packet)
			last_sp = source_port
			last_dp = dest_port
			last_si = s_addr
			last_di = d_addr
