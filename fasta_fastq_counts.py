#!/usr/bin/env python3

#Protein FASTA/FASTQ counter
#takes uncompressed or gz compressed files as input
#Returns total number of residues and amino acids within the file

import gzip
import sys
import re

def main():
#open and read file - compressed or uncompressed
    filename = sys.argv[-1]
    if filename.endswith('.gz'):
        file = gzip.open(filename, 'rb')
        is_com = True
    else:
        file = open(filename, 'rU')
        is_com = False
        
#initiate counts
    seq_count = 0
    res_count = 0
#find file format    
    if re.search('.fastq', filename) or re.search('.fq', filename):
        #count seq and aa residues for fastq
        prev = "four"
        for line in file:
            if is_com:
                line = line.decode()
            
            #four lines for every fastq entry
            line = line.rstrip()
            if line.startswith("@") and prev == "four":
                seq_count += 1
                prev = "one"
            elif re.match('[ATCG]+', line) and prev == "one":
                res_count += len(line)
                prev = "two"
            elif line.startswith("+") and prev == "two":
                prev = "three"
            else:
                prev = "four"
    else:
        #count seq and amino acids for fasta
        for line in file:
            if is_com:
                line = line.decode()
          
            if line.startswith(">"):
                seq_count = seq_count + 1
            else:
                res_count = len(line.rstrip()) + res_count
                
    file.close()
    sys.stdout.write("Total sequences found: " + str(seq_count) +"\n")
    sys.stdout.write("Total residues found: " + str(res_count))



if __name__ == '__main__':
    main()
