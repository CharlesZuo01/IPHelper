from classip import ipobject
import requests
import json


#this function is copy pasted from the classip.py file because of short sighted planning.  I needed 
#to call this function but not against an IPobject which is why it was copy pasted out of the class

def decimal(x, mask):  #converts 32 bit number back to IP address
	dec = ''
	for i in range(0,4):
		octet = x[i*8:(i + 1) * 8]
		dec = dec + str(int(octet, 2)) + '.' 
	dec = dec[:len(dec)-1] 
	return dec + '/' + str(mask)


def getinput():
	ip = raw_input('Please enter your IP address: ')
	mask = raw_input('Please enter your subnet mask: ')

	#add some error checking
	
	return [ip, mask]


def runprogram():
	print('What would you like to do? \n 1.  Subnet Calculator \n \
2.  Find common subnet(supernet) \n 3.  IP lookup')

	users_choice = raw_input('Select what you would like to do: ')
	try:

		'''
		Subnet Calculator
		'''
		if int(users_choice) == 1:
			print '2'
			argumentspassedtoa = getinput()
			a = ipobject(argumentspassedtoa[0], argumentspassedtoa[1])
			ip_and_mask = a.return_ip_and_mask()
			if ip_and_mask[1] == 31: #p2p networks
				print 'This is a point to point network'
				print 'Your usable address range address is ',  a.decimal(str(a.netbroadadd(a.binary(ip_and_mask[0]))[0])), 'to', a.decimal(str(a.netbroadadd(a.binary(ip_and_mask[0]))[1]))
				print 'Your subnetmask is 255.255.255.254'
			elif ip_and_mask[1] == 32: #host network
				print 'This is a host address.  Your IP is', a.ip, 'and your mask is', a.mask
			elif ip_and_mask[1] >= 0 and ip_and_mask[1] < 31:
				#Ugly AF but takes IP in a list format [a.b.c.d], converts to binary, from the binary string the network address, broadcast address,
				#and usable range are determined.  Decimal() function converts everything back to readable decimal format
				print 'Your network is: ', a.decimal(str(a.netbroadadd(a.binary(a.return_ip_and_mask()[0]))[0])),'/', a.mask
				print 'Your subnet mask in dotted decimal is ', a.decimal(str(a.getnetmask(a.mask)))
				print 'Your network address is ',  a.decimal(str(a.netbroadadd(a.binary(a.return_ip_and_mask()[0]))[0]))
				print 'Your broadcast address is ',  a.decimal(str(a.netbroadadd(a.binary(a.return_ip_and_mask()[0]))[1]))
				print 'Your usable range is between ',  a.decimal(str(a.netbroadadd(a.binary(a.return_ip_and_mask()[0]))[2])), 'and', a.decimal(str(a.netbroadadd(a.binary(a.return_ip_and_mask()[0]))[3]))
			else:
				print "Something broke, copy paste and send to Charles"
				exit() 

		elif int(users_choice) ==2:
			#need error checking here.
			ips = str(raw_input('Enter subnets or IPs in x.x.x.x/y format: '))
			#subnets splits the user input subnets.  subnets2 breaks them apart by IP and mask, subnet3 contains 
			#the network and broadcast addresses of the input in binary format to be used for supernet calculation
			subnets= ips.split(' ')
			subnets2 = []
			subnets3 = []
			for i in subnets:
				subnets2.append(i.split('/'))

			for i in subnets2:
				a = ipobject(i[0], i[1])
				subnets3.append(a.netbroadadd(a.binary(a.return_ip_and_mask()[0]))[0]) #network address
				subnets3.append(a.netbroadadd(a.binary(a.return_ip_and_mask()[0]))[1]) #broadcast address
			mask = 35
			current = 0
			for i in range(0, len(subnets3)-1):
				current = 0
				for h in range(0,32):
					if subnets3[i][h] == subnets3[i+1][h]:  #create var that matches the current address and then compare that to next iteration of loop
						current += 1
					else:
						if i == 0:
							mask = current
						else:
							if current < mask:	
								mask = current
						break

			netbits = subnets3[0][:mask]
			while len(netbits) < 32:
				netbits = netbits + '0'
			print "Your supernet is: " (decimal(netbits, mask))
		elif int(users_choice) == 3:
			IP = str(raw_input("Enter the IP to lookup: "))
			response = requests.get("http://ip-api.com/json/" + IP)
			JSON_OBJ = json.loads(response.text)
			print("AS is: " + str(JSON_OBJ["as"]))
			print("ORG is: " + str(JSON_OBJ["org"]))
			print("ISP is: " + str(JSON_OBJ["isp"]))
			print("Located in: " + str(JSON_OBJ["city"]) + ', ' + str(JSON_OBJ["regionName"]) + ', ' + str(JSON_OBJ["country"]))
		else: 
			print('That was not a valid option.  Please try again')
			runprogram()
	except:
		print('That was not a valid option.  Please try again')
		runprogram()


runprogram()



