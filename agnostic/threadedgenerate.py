import argparse
import os
# drop in replacement for threading when we want a return value
from multiprocessing.pool import ThreadPool
import threading

output = {}

# credit for this "bs_from_file" method to http://stackoverflow.com/questions/1035340/reading-binary-file-in-python-and-looping-over-each-byte
# by skurmedel
# this method reads in the file in binary to a buffer passed back to the
# main func, used for improved processing speed by buffering the object


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

# this function contains the find call/ find() uses the
# Boyer-moore-horspool algorithm


def search(buff, cut_s):
    return buff.find(cut_s)

# search for string/made to handle a multi byte input, however the current
# code version only sends 1 byte at a time


def cut(buff, minus_s, idn):
    # full length of string then repeat with len-1 til found then return a
    # tuple of the location and how many bs
    while(len(minus_s) > 0):
        tool = search(buff, minus_s)
        if(tool != -1):
            output[idn] = tool;
            return
        else:
            minus_s = minus_s[:-1]
            # print minus_s


def main():
    # simple arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("secret", type=str,
                        help="the file you are attempting to hide")
    parser.add_argument("output", type=str,
                        help="where you are outputing the key")
    parser.add_argument("payload", type=str,
                        help="the payload you are using to hide it against, to unhide file, you must have an exact copy of this file")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    #dictionary for output
    threads = []
    idn = 0
    # open secret with the first method
    for b in bs_from_file(args.secret):
        idn += 1
        # open payload and read into buffer
        with open(args.payload, 'rb') as f:
            # thread the searching for efficiency
            buff = f.read()

            #while(threading.active_count()>700):
            #    continue
            # run search against the byte and store it
            # thread this but pass it a sequence id
            #pool = ThreadPool(processes=1)
            #async_result = pool.apply_async(cut, (buff, b, idn,))
            t = threading.Thread(target=cut, args=(buff,b,idn,))
            threads.append(t)
            t.start()
            #foo = async_result.get(timeout=2)
            #output[foo] = idn;
            # key = cut(buff,b)
            # output.append(idn)
            # output.append(key[0])

    fout = open(args.output, 'wb')
    # run a sort on the output to order them by sequencer and then strip the id off of them
    # output all the bytes locations to the keyfile
    for key in sorted(output):
        fout.write(str(output[key]))
        fout.write(',')
        #print "%s: %s" % (key, output[key])

    fout.close()

if __name__ == "__main__":
    main()
