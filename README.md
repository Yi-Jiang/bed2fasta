# Convert bed files or genomic positions to sequences
```
python3 bed2fasta.saveMem.py
usage: python bed2fasta.saveMem.py -option <argument>
     -i     <STRING>    a string like "chrN:start-end" or a BED file
     -r     <STRING>    can be "hg19", "hg38", or a path to reference genome [hg38]
     --bed              output BED format [FASTA]
     --upper            convert all bases to uppercase
     --mark             mark position at the end of each line
     -h/--help
```
