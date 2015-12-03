import pefile
import argparse
import shutil
import os

#encode/encrypt the stego secret data before hiding
def encode(secret):
	return None

#decode/decrypt the stego secret data after extracting
def decode(secret):
	return None

#method for inseting data using a tuple consisting of size of data and location in file to start
def hide(off,outPath,secret):
	#opens the outPath for reading and writing in binary
	with open(outPath, 'r+b') as fi:
		#open the secret message and read it into a string=sec
		se = open(secret, 'rb')
		sec = se.read()
		se.close()

		#open secret again this time for writing
		#the writing will be deleting the data we already hid
		se = open(secret, 'wb')

		#place the filepointer at the location to start writing the data
		fi.seek(off[0],0)

		#string set to the data we can fit in this area
		modsec = sec[:off[1]]

		#write back to the secret file without the data we just hid
		se.write(sec[off[1]:])
		
		#create a byte array to write binary to the file
		newFileByteArray = bytearray(modsec)
		fi.write(newFileByteArray)
		se.close()

	return None

#method to extract the data we have hidden in the sections
def find(off,outPath,pePath):
	#open files
	fo = open(outPath, 'ab')
	with open(pePath, 'r+b') as fi:
		#set the file pointer
		fi.seek(off[0],0)

		#read all bytes at once
		bytes = fi.read(off[1])

		fo.write(bytes)

		# while loop to read byte by byte for improved accuracy
		# x=0
		# while x < off[1]:
		# 	#read the byte
		# 	byte = fi.read(1)
		# 	#write the byte
		# 	fo.write(byte)
		# 	x += 1

	return None

def main():
	#simple argparse --help for more info
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', dest="pePath", type=str,help="The path to the PE you wish to work with")
	parser.add_argument('-l', dest="payload", type=str,help="the data you wish to store within the PE")
	parser.add_argument('-o', dest='output', type=str,help="What is the output for the new executable with hidden data/Where do you want the hidden data output")
	parser.add_argument('-s', dest='showSize',action='store_true',help="Show the size that is available for hiding")
	parser.add_argument('--hide', dest='hide', action='store_true',help="set flag to hide the data in the file")
	parser.add_argument('--extract', dest='extract', action='store_true',help="set flag to extract the data")

	args = parser.parse_args()

	#create pefile instance using the pefile we want to use
	pe = pefile.PE(args.pePath, fast_load=True)

	#instantiate size to 0
	size = 0

	#setup some files for the hide method
	if args.hide:
		shutil.copyfile(args.payload, 'a'+args.payload)
		shutil.copyfile(args.pePath, args.output)

	#iterate through sections to pull header data from them
	for section in pe.sections:
		#tuple containing the section data require for hiding in the section space
		tup = (section.Name, section.PointerToRawData, section.Misc_VirtualSize, section.SizeOfRawData)
		
		#where to place the file pointer for the start of hidden data
		startADDR = tup[1] + tup[2]

		#how much can be hidden or is hidden within the area
		availSpace = tup[3] - tup[2]

		#tuple passed to methods for extracting or hiding
		hideOffset = (startADDR, availSpace)

		#unable to handle the section slack if there will be dynamic allocation out of my scope
		if availSpace > 0:
			#run the hiding algorithm
			if args.hide:
				print "\n[*]HIDING %d BYTES OF DATA IN %s[*]"%(availSpace, section.Name)
				hide(hideOffset,args.output, args.payload)

			#run th extraction algorithm
			elif args.extract:
				print "\n[*]EXTRACTING %d BYTES OF DATA FROM %s[*]"%(availSpace, section.Name)
				find(hideOffset,args.output,args.pePath)

			#add the size of this slack space to the overall available possible hiding size
			size += availSpace

	#if the showSize flag is set, output the area available
	if args.showSize:
		print "Size available to store payload in %s is %d bytes.\n" % (args.pePath, size)

	#cleanup after the hide
	if args.hide:
		os.remove(args.payload)
		shutil.copyfile('a'+args.payload, args.payload)
		os.remove('a'+args.payload)



if __name__ == "__main__": main()