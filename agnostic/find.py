import argparse

def main():
	#simple arg parse to get filenames
	parser = argparse.ArgumentParser()
	parser.add_argument("key", type=str,help="the keyfile")
	parser.add_argument("output", type=str,help="where you are ouputing the secret")
	parser.add_argument("payload", type=str,help="the payload used to store the data")
	parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	#bytearray for storing the bytes we pull out of the file
	newFileByteArray = bytearray()
	#open the keyfile with relative locations of bytes
	key = open(args.key,'rb')
	#open file for outputing the stuff too later
	fsec = open(args.output,'wb')
	#open the file we used to hide the data in, must be the same version as the one that was used to encode the data
	payload = open(args.payload, 'rb')
	#parse the keyfile
	keylist = key.read()
	keylist = keylist.split(',')
	keylist = keylist[:-1]
	#walk through the key list
	for loc in keylist:
		#make filepointer to the byte that was in the key
		payload.seek(int(loc),0)
		#append that byte to the output byte array
		newFileByteArray.append(payload.read(1))

	#output bytearray to file
	fsec.write(newFileByteArray)

if __name__ == "__main__": main()