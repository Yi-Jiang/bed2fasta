#!/usr/bin/env python3
import os, sys, re, getopt, math

def usage():
    print("usage: python %s -option <argument>" %sys.argv[0])
    print("     -i     <STRING>    a string like \"chrN:start-end\" or a BED file")
    print("     -r     <STRING>    can be \"hg19\", \"hg38\", or a path to reference genome [hg38]")
    print("     --bed              output BED format [FASTA]")
    print("     --upper            convert all bases to uppercase")
    print("     --mark             mark position at the end of each line")
    print("     -h/--help                      ")

if len(sys.argv) < 2:
    usage()
    sys.exit(2)

try:
    opts, args = getopt.getopt( sys.argv[1:], "i:r:h", ["help", "bed", "upper", "mark", ] )
except getopt.GetoptError:
    print("Get option error!")
    usage()
    sys.exit(2)

isBed = 0
toUpper = 0
mark = 0

for opt, val in opts:
    if opt in ( "-h", "--help" ):
        usage()
        sys.exit(1)
    else:
        if opt in ( "-i", ):
            infile = val
        if opt in ( "-r", ):
            ref = val
        if opt in ( "--bed", ):
            isBed = 1
        if opt in ( "--upper", ):
            toUpper = 1
        if opt in ( "--mark", ):
            mark = 1

if "ref" in dir():
    if ref=="hg19":
        ref = "/home/yjiang/database/refGenome/hg19/hg19.fa"
    elif ref=="hg38":
        ref = "/home/data/refGenome/hg38/hg38.fa"
    else:
        if not os.path.isfile(ref):
            print("Get option error: reference genome is not exist!")
            usage()
            sys.exit(2)
else:
    ref = "/home/data/refGenome/hg38/hg38.fa"

# function
refFile=open(ref,"r")
refIndex=open("%s.fai"%ref, "r")
indexDict = dict()
length_chr = dict()
for line in refIndex:
    line_s = line.split("\t")
    indexDict[line_s[0]] = int(line_s[2])
    length_chr[line_s[0]] = int(line_s[1])
lineWidth = int(line_s[3])
refIndex.close()

def bed2fasta(chr,start,end):
    if end>length_chr[chr]:
        sys.stderr.write("Warn: Window out of range on %s:%s-%s!\n"%(chr,start,end))
        return "-"
        
    index = start+int((start-1)/lineWidth)+indexDict[chr]-1
    refFile.seek(index)
    
    seq = ""
    for i in range(int((end-start)/lineWidth)+2):
        seq += refFile.readline().rstrip("\n")
    
    mySeq = seq[:end-start+1]
    
    return mySeq

def printFASTA(myseq0,ch0,st0,en0):
    if toUpper==1:
        myseq0 = myseq0.upper()
    length = len(myseq0)
    lines = math.ceil(length/lineWidth)
    print(">",ch0,":",st0,"-",en0,sep="")
    if mark==0:
        for i in range(lines-1):
            print(myseq0[i*lineWidth:(i+1)*lineWidth])
        print(myseq0[(lines-1)*lineWidth:])
    else:
        start0 = st0
        for i in range(lines-1):
            print(myseq0[i*lineWidth:(i+1)*lineWidth], "[%s:%s-%s]"%(ch0,start0,start0+49))
            start0 = start0 + lineWidth
        print(myseq0[(lines-1)*lineWidth:], "[%s:%s-%s]"%(ch0,start0,en0))

def printBED(myseq0,prefix0):
    if toUpper==1:
        myseq0 = myseq0.upper()
    print("%s\t%s"%(prefix0,myseq0))

# main
if re.search(r'\w+:\d+',infile):
    infile = re.sub(",","",infile)
    infile = re.sub(" ","",infile)
    if re.search("-",infile):
        ch,st,en = re.split("[:-]",infile)
    else:
        ch,st = re.split("[:-]",infile)
        en = st
    st = int(st)
    en = int(en)
    myseq = bed2fasta(ch,st,en)
    if isBed:
        prefixCol = "%s\t%s\t%s"%(ch,st,en)
        printBED(myseq,prefixCol)
    else:
        printFASTA(myseq,ch,st,en)
else:
    if not os.path.isfile(infile):
        print("You did not infile a eligible string or a file name, please check your infile.")
        usage()
        sys.exit(2)
    f = open(infile,"r")
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.rstrip()
        s = line.split("\t")
        ch,st,en = s[:3]
        st = int(st)
        en = int(en)
        myseq = bed2fasta(ch,st,en)
        if isBed:
            printBED(myseq,line)
        else:
            printFASTA(myseq,ch,st,en)

refFile.close()


