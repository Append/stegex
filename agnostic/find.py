
def main():
	newFileByteArray = bytearray()
	key = open("key2.txt",'rb')
	fsec = open('secret.jpeg','wb')
	payload = open("C:\Windows\system32\calc.exe", 'rb')
	keylist = key.read()
	keylist = keylist.split(',')
	keylist = keylist[:-1]
	for loc in keylist:
		payload.seek(int(loc),0)
		newFileByteArray.append(payload.read(1))

	#print newFileByteArray
	fsec.write(newFileByteArray)

if __name__ == "__main__": main()