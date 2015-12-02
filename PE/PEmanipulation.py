import pefile
import argparse
import shutil

#used for spliting up the data for hiding
def split(secret, size):
	return 0

#method for inseting data using a tuple
def hide(off,outPath):
	print hex(off[0]),hex(off[1])
	with open(outPath, 'r+b') as fi:
		fi.seek(off[0],0)
		#junk = fi.read(off[1])
		#fi.seek(off[0],0)
		string = ('61' * 80).decode('hex')
		#print string
		newFileByteArray = bytearray(string)
		#print newFileByteArray
		fi.write(newFileByteArray)
	return


def main():
	#simple arg parse to get filenames
	parser = argparse.ArgumentParser()
	parser.add_argument("pePath", type=str,help="The path to the PE you wish to work with")
	#parser.add_argument("payload", type=str,help="the payload used to store the data")
	parser.add_argument("output", type=str,help="What is the output for the new executable with hidden data")
	args = parser.parse_args()

	pe = pefile.PE(args.pePath, fast_load=True)
	sectionGaps = []
	#secNum = pe.FILE_HEADER.NumberOfSections
	#print secNum
	shutil.copyfile(args.pePath, args.output)
	for section in pe.sections:
		tup = ()
		print (section.Name, hex(section.VirtualAddress), hex(section.Misc_VirtualSize), section.SizeOfRawData )
		tup = (section.Name, section.VirtualAddress, section.Misc_VirtualSize, section.SizeOfRawData)
		sectionGaps.append(tup)

	for x in range(len(sectionGaps)):
		#where to start hiding
		if x == (len(sectionGaps) - 1):
			break
		if min(sectionGaps[x][2],sectionGaps[x][3]) == 0:
			continue
		else:
			startADDR = max(sectionGaps[x][2],sectionGaps[x][3]) + sectionGaps[x][1]
		#how much can be hid
		#print hex(startADDR)
		availSpace = int(sectionGaps[x+1][1]) - int(startADDR)

		#tuple used for hiding
		hideOffset = (startADDR, availSpace)

		#print hideOffset
		hide(hideOffset,args.output)
		break
	#pe.write(filename=args.output)
	#print sectionGaps


if __name__ == "__main__": main()