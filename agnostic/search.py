import argparse

#this method reads in the file in binary to a buffer passed back to the main func, used for improved processing speed by buffering the object
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

#this function contains the find call/ find() uses the Boyer-moore-horspool algorithm
def search(buff, cut_s):
	return buff.find(cut_s)

#search for string/made to handle a multi byte input, however the current code version only sends 1 byte at a time
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
	#simple arg parser
	parser = argparse.ArgumentParser()
	parser.add_argument("secret", type=str,help="the file you are attempting to hide")
	parser.add_argument("output", type=str,help="where you are outputing the key")
	parser.add_argument("payload", type=str,help="the payload you are using to hide it against, to unhide file, you must have an exact copy of this file")
	parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	args = parser.parse_args()
	
	output = []
	#open secret with the first method
	for b in bs_from_file(args.secret):
		#open payload and read into buffer
		with open(args.payload, 'rb') as f:
			buff = f.read()
			#run search against the byte and store it
			output.append(cut(buff,b)[0])

	#output all the bytes locations to the keyfile
	fout = open(args.output,'wb')

	for thing in output:
		fout.write(str(thing))
		fout.write(',')

	fout.close()

if __name__ == "__main__": main()