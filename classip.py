class ipobject:
	"""Moms Sphagetti"""


	def __init__(self, ip, mask):
		self.ip = ip
		self.mask = mask


	#takes IP and mask attributes and returns them in list and number format,
	#e.g [[10.1.1.1], 30]
	def return_ip_and_mask(self):
		masknumber = 0
		maskinput = self.mask
		IP = self.ip.split('.')
		IP = [int(i) for i in IP]
		netmask = ''
		if len(str(maskinput)) < 3:
			masknumber = int(maskinput)
		else:
			maskdotted = maskinput.split('.')
			maskdotted = [int(i) for i in maskdotted]
			for i in self.binary(maskdotted): #converts binmask in list of 4 octets to 32 bit binary string
				if i == '1':
					masknumber += 1
		self.mask = masknumber


		return [IP, masknumber]

	#takes an IP (or subnet mask) in a list as dotted decimal format and returns as 32 bit string
	#e.g [255.255.255.0] returns as 11111111111111111111111100000000
	def binary(self, ip_in_list_format):
		bit32_string = ''
		for i in ip_in_list_format:
			octet =  bin(i)[2:]
			while len(octet) < 8:
				octet = '0' + octet
			bit32_string +=  octet
		return bit32_string

	 #takes a 32 bit binary number as a str, and given the network mask, returns the network address and host address
	def netbroadadd(self, bit32_string):
		# print x[:mask]
		networkad = bit32_string[:self.mask]
		broadad = networkad
		while len(networkad) < 31:
			networkad = networkad + '0'
		netstart = networkad + '1'	
		networkad = networkad + '0'
		while len(broadad) < 31:
			broadad = broadad + '1'
		netend = broadad + '0'
		broadad = broadad + '1'

		return [networkad, broadad, netstart, netend]


	def network_and_broadcast_address(self, bit32_string):
		# print x[:mask]
		networkad = bit32_string[:self.mask]
		broadad = networkad
		while len(networkad) < 32:
			networkad = networkad + '0'
		while len(broadad) < 32:
			broadad = broadad + '1'

		return [networkad, broadad]

		return [networkad, broadad, netstart, netend]
	#converts 32 bit number back to IP address
	def decimal(self, x):  
		dec = ''
		for i in range(0,4):
			octet = x[i*8:(i + 1) * 8]
			dec = dec + str(int(octet, 2)) + '.' 
		dec = dec[:len(dec)-1] 
		return dec 
	
	def getnetmask(self, slashmask):  #Converts netmask /x format to a.b.c.d
		netmask = ''
		for i in range (0, slashmask):
			netmask = netmask + '1'
		while len(netmask) < 32:
			netmask = netmask + '0'
		return netmask
	

	def addresstype(self):
	
		if return_ip_and_mask()[1] == 32:
			self.addrtype = 'Host address'
		return self.addrtype

