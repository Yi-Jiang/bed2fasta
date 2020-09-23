#!/usr/bin/env python3.5
import sys, re, getopt, math

def usage():
    print("output format: FASTA")
    print("usage: python %s -option <argument>" %sys.argv[0])
    print("     -i     <STRING>    a string like \"chrN:start-end\" or a BED file")
    print("     -r     <STRING>    reference FASTA file")
    print("     --upper            convert all bases to uppercase")
    print("     --mark             mark position for each line")
    print("     -h/--help                      ")

if len(sys.argv) < 2:
    usage()
    sys.exit(2)

try:
    opts, args = getopt.getopt( sys.argv[1:], "i:r:h", ["help", "upper", "mark", ] )
except getopt.GetoptError:
    print("get option error!")
    usage()
    sys.exit(2)

# deal with the options
ref = "/zs32/data-analysis/reflib/genomes/human_UCSC_hg19/chrAll.fasta"
toUpper = 0
mark = 0

for opt, val in opts:
    if opt in ( "-h", "--help" ):
        usage()
        sys.exit(1)
    else:
        if opt in ( "-i", ):
            input = val
        if opt in ( "-r", ):
            ref = val
        if opt in ( "--upper", ):
            toUpper = 1
        if opt in ( "--mark", ):
            mark = 1
            
# function
refFile=open(ref,"r")
refIndex=open("%s.fai"%ref, "r")
indexDict = dict()
length_chr = dict()
for line in refIndex:
    line_s = line.split("\t")
    indexDict[line_s[0]] = int(line_s[2])
    length_chr[line_s[0]] = int(line_s[1])
refIndex.close()

def bed2fasta(chr,start,end):
    if end>length_chr[chr]:
        sys.stderr.write("Warn: Window out of range on %s:%s-%s!\n"%(chr,start,end))
        return "-"
        
    index = start+int((start-1)/50)+indexDict[chr]-1
    refFile.seek(index)
    
    seq = ""
    for i in range(int((end-start)/50)+2):
        seq += refFile.readline().rstrip("\n")
    
    mySeq = seq[:end-start+1]
    
    return mySeq

# main
if re.search(r'\w+:\d+',input):
    input = re.sub(",","",input)
    input = re.sub(" ","",input)
    if re.search("-",input):
        ch,st,en = re.split("[:-]",input)
    else:
        ch,st = re.split("[:-]",input)
        en = st
    st = int(st)
    en = int(en)
    myseq = bed2fasta(ch,st,en)
    if toUpper==1:
        myseq = myseq.upper()
    length = len(myseq)
    lines = math.ceil(length/50)
    print(">",ch,":",st,"-",en,sep="")
    if mark==0:
        for i in range(lines-1):
            print(myseq[i*50:(i+1)*50])
        print(myseq[(lines-1)*50:])
    else:
        start0 = st
        for i in range(lines-1):
            print(myseq[i*50:(i+1)*50], "[%s:%s-%s]"%(ch,start0,start0+49))
            start0 = start0 + 50
        print(myseq[(lines-1)*50:], "[%s:%s-%s]"%(ch,start0,en))
else:
    try:
        f = open(input,"r")
    except:
        print("You did not input a eligible string or a file name, please check your input.")
        usage()
        sys.exit(2)

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
        if toUpper==1:
            myseq = myseq.upper()
        length = len(myseq)
        lines = math.ceil(length/50)
        #print(">",ch,":",st,"-",en,sep="")
        print(">%s"%line)
        if mark==0:
            for i in range(lines-1):
                print(myseq[i*50:(i+1)*50])
            print(myseq[(lines-1)*50:])
        else:
            start0 = st
            for i in range(lines-1):
                print(myseq[i*50:(i+1)*50], "[%s:%s-%s]"%(ch,start0,start0+49))
                start0 = start0 + 50
            print(myseq[(lines-1)*50:], "[%s:%s-%s]"%(ch,start0,en))
            
refFile.close()


