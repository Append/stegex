
def bs_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break
    f.close()

#this function contains the find call
def search(buff, cut_s):
	return buff.find(cut_s)

#search for string
def cut(buff, minus_s):
	#full length of string then repeat with len-1 til found then return a tuple of the location and how many bs
	while(len(minus_s)>0):
		tool = search(buff, minus_s)
		if(tool!=-1):
			return (tool,minus_s)
			print '1'
		else:
			minus_s = minus_s[:-1]
			#print minus_s

def main():
	# example:
	output = []
	for b in bs_from_file('test.jpeg'):
		# Do stuff with b.
		with open("C:\Windows\system32\calc.exe", 'rb') as f:
			buff = f.read()
			output.append(cut(buff,b)[0])

	fout = open("key2.txt",'wb')

	for thing in output:
		fout.write(str(thing))
		fout.write(',')

	fout.close()

if __name__ == "__main__": main()