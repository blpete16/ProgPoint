import sys
import os

def getOutFile(infilename, outfiledir):
    lastslashind = infilename.rfind("/")
    ifname = infilename[lastslashind+1:]
    ifname = outfiledir+"parsed_"+ifname
    return ifname

def convertBstrToDecStr(bstr):
    istr = "".join(map(lambda b: format(
    return bstr

infiledir = sys.argv[1]
outfiledir = sys.argv[2]
filternamefile = sys.argv[3]
filternames = []
with open(filternamefile, 'r') as ffile:
    for line in ffile:
        filternames.append(line)

for infilename in os.listdir(infiledir):
    outfilename = getOutFile(infilename, outfiledir)
    infilename = infiledir + infilename
    with open(infilename, 'rb') as infile:
        with open(outfilename, 'w') as ofile:
            totalbstr = ""
            for line in infile:
                if(line.startswith("DROPSTATE")):
                    if(len(totalbstr) > 0):
                        intstr = convertBstrToDecStr(totalbstr)
                        ofile.write(intstr)
                        ofile.write("\n")
                    totalbstr = ""
                    ofile.write(line)
                else:
                    vals = line.split(",")
                    if(not (vals[0] in filternames)):
                        totalbstr = totalbstr + (vals[2])[2:-2]
