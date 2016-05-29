import sys
import os

def buildint(bvals):
    return int.from_bytes(bvals, byteorder='little')

def buildstr(bvals):
    print(str(bvals))
    return bvals.decode("utf-8")

def getOutFile(infilename, outfiledir):
    lastslashind = infilename.rfind("/")
    ifname = infilename[lastslashind+1:]
    ifname = outfiledir+"parsed_"+ifname
    return ifname

infiledir = sys.argv[1]
outfiledir = sys.argv[2]

statenames = ["main", "doencode", "cksum", "compare_files", "treat_file", "make_ofname"]

for infilename in os.listdir(infiledir):
    
    outfilename = getOutFile(infilename, outfiledir)
    infilename = infiledir + infilename
    with open(infilename, 'rb') as infile:
        with open(outfilename, 'w') as ofile:
            bytes_read = infile.read(4)
            while bytes_read:
                ival = buildint(bytes_read)
                print ("read state name size int:"+str(ival))
                bytes_read = infile.read(ival)
                sval = buildstr(bytes_read)

                print("sval:"+sval)
                print("len sval:"+str(len(sval)))
                        

                while bytes_read:
                    print ("read bytes:"+sval)
                    ofile.write("DROPSTATE:"+sval)
                    ofile.write("\n")
                
                    bytes_read = infile.read(4)
                    ival = buildint(bytes_read)
                    print("read paircount:"+str(ival))
                    while bytes_read:
                        bytes_read = infile.read(4)
                        lival = buildint(bytes_read)
                        print("read size of name:"+str(lival))
                        bytes_read = infile.read(lival)
                        sval = buildstr(bytes_read)
                        print("read name:"+sval)
                        if(sval.startswith(tuple(statenames))):
                            print("BREAK!")
                            break
                            
                
                        ofile.write(sval)
                        ofile.write(",")
                
                        bytes_read = infile.read(4)
                        lival = buildint(bytes_read)
                        print("read size of type:"+str(lival))
                        bytes_read = infile.read(lival)
                        sval = buildstr(bytes_read)
                        print("read type:"+sval)
                        ofile.write(sval)
                        ofile.write(",")

                        bytes_read = infile.read(4)
                        lival = buildint(bytes_read)
                        print("read size of data:"+str(lival))
                        bytes_read = infile.read(lival)
                        print("read data:"+str(bytes_read))
                        ofile.write(str(bytes_read))
                        ofile.write("\n")
