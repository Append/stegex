import argparse
import difflib

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', dest="suspect", type=str,help="The path to the potentially stego'd PE")
	parser.add_argument('-l', dest="original", type=str,help="A 'clean' version of the exe")
	parser.add_argument('-o', dest='output', type=str,help="What is the output for the secret message")
	args = parser.parse_args()

	fs = open(args.suspect,'rb')
	fo = open(args.original,'rb')
	fs.seek(0x16000,0)
	fo.seek(0x16000,0)

	diff = difflib.ndiff(fs.read(), fo.read())

	delta = ''.join(x[2:] for x in diff if x.startswith('- '))
	print delta

if __name__ == "__main__": main()