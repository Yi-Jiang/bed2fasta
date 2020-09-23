# bed2fasta
Convert bed files or genomic positions to sequences.

## Output file: FASTA
```bash
python3 bed2fasta.saveMem.py
output format: FASTA
usage: python bed2fasta.saveMem.py -option <argument>
     -i     <STRING>    a string like "chrN:start-end" or a BED file
     -r     <STRING>    reference FASTA file
     --upper            convert all bases to uppercase
     --mark             mark position for each line
     -h/--help
```

## Output file: BED
```bash
python3 bed2fasta2.saveMem.py
output format: BED
usage: python bed2fasta2.saveMem.py -option <argument>
     -i     <STRING>    a string like "chrN:start-end" or a BED file
     --upper            convert all bases to uppercase
     -r     <STRING>    reference genome. [/zs32/data-analysis/reflib/genomes/human_UCSC_hg19/chrAll.fasta]
     -h/--help
```