#!/usr/bin/env python3.5
import sys, re, getopt, math

def usage():
    print("output format: BED")
    print("usage: python %s -option <argument>" %sys.argv[0])
    print("     -i     <STRING>    a string like \"chrN:start-end\" or a BED file")
    print("     --upper            convert all bases to uppercase")
    print("     -r     <STRING>    reference genome. [/zs32/data-analysis/reflib/genomes/human_UCSC_hg19/chrAll.fasta]")
    print("     -h/--help                     ")

if len(sys.argv) < 2:
    usage()
    sys.exit(2)

try:
    opts, args = getopt.getopt( sys.argv[1:], "i:r:h", ["help", "upper"] )
except getopt.GetoptError:
    print("get option error!")
    usage()
    sys.exit(2)

# deal with the options
upper = 0
refGenome = "/zs32/data-analysis/reflib/genomes/human_UCSC_hg19/chrAll.fasta"
for opt, val in opts:
    if opt in ( "-h", "--help" ):
        usage()
        sys.exit(1)
    else:
        if opt in ( "-i", ):
            input = val
        if opt in ( "--upper", ):
            upper = 1
        if opt in ( "-r", ):
            refGenome = val
            
# function
refFile=open(refGenome,"r")
refIndex=open("%s.fai"%refGenome, "r")
indexDict = dict()
length = dict()
for line in refIndex:
    line_s = line.split("\t")
    indexDict[line_s[0]] = int(line_s[2])
    length[line_s[0]] = int(line_s[1])
refIndex.close()

def bed2fasta(chr,start,end):
    start = int(start)
    end = int(end)
    
    if end>length[chr]:
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
    myseq = bed2fasta(ch,st,en)
    if upper==1: myseq = myseq.upper()
    length = len(myseq)
    lines = math.ceil(length/50)
    #print(">",ch,":",st,"-",en,sep="")
    print(">%s:%s-%s"%(ch,st,en))
    for i in range(lines-1):
        print(myseq[i*50:(i+1)*50])
    print(myseq[(lines-1)*50:])
else:
    try:
        f = open(input,"r")
    except:
        print("You did not input a eligible string or a file name, please check your input.")
        usage()
        sys.exit(2)

    #f.readline()
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.rstrip()
        s = line.split("\t")
        ch,st,en = s[:3]
        if len(s)<3:
            continue
        elif len(s)==3:
            myseq = bed2fasta(ch,st,en)
            if upper==1: myseq = myseq.upper()
            print("%s\t%s\t%s\t%s"%(s[0],s[1],s[2],myseq))
        else:
            myseq = bed2fasta(ch,st,en)
            if upper==1: myseq = myseq.upper()
            print("%s\t%s\t%s\t%s\t%s"%(s[0],s[1],s[2],myseq,"\t".join(s[3:])))



refFile.close()
