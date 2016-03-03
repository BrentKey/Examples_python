#!/usr/bin/env python2.7

"""
This program takes an input fasta file, reference fasta file, and name for output file.
Reference is checked against input for pairwise alignment, if 100% local 
alignment is found, the input description and sequence are written to
the output fasta file. Scoring can be altered for looser alignment.

Author: Brent Key, brentmkey@gmail.com, 2/20/16
"""

import argparse
import re
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import pairwise2


def main():
    parser = argparse.ArgumentParser(description='Searching for 100% local alignment between query and reference fasta files.')
    
    # Input, reference, and output files needed to run sequences. Input/ref must be fasta
    parser.add_argument('-i', '--input', type=str, required=True, help='Fasta file with unknown transcripts')
    parser.add_argument('-r', '--ref', type=str, required=True, help='Reference file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Name of output fasta file')
    args = parser.parse_args()
    
    #Run alignment and write output
    check_match(args.input, args.ref, args.output)
   
#translate to protein sequence 
def trans(cds):
    start = re.compile('ATG')
    nuc = cds.replace('\n','')
    longest = [0,0,0]
    pro_list = ("A","A","A")
    
    #find longest ORF in each of 3 positions
    for m in start.finditer(nuc):
        frame = m.start()%3
        pro = Seq(nuc)[m.start():].translate(to_stop=True)
        if (frame == 0) and (len(pro) > longest[0]):
            longest[0] = len(pro)
            orf1 = str(pro)
        elif (frame == 1) and (len(pro) > longest[1]):
            longest[1] = len(pro)
            orf2 = str(pro)
        elif (frame == 2) and (len(pro) > longest[2]):
            longest[2] = len(pro)
            orf3 = str(pro)
        else:
            continue 
       
    pro_list = (orf1, orf2, orf3)   
    print(pro_list)         
    return pro_list
  
# Pairwise alignment  
def check_match(input, reference, output):
    in_record = open(input)
    ref_record = open(reference)    
    fasta_list = []
    
    for in_record in SeqIO.parse(input, "fasta"): #parse input and reference seqs
        #translate to peptide seq
        orf = trans(str(in_record.seq))
        written = 0
            
        for aa_seq in orf:
            if (written == 0) and (len(aa_seq) >= 140): #shortest length of a ref seq
                for ref_record in SeqIO.parse(reference, "fasta"):
                    # pairwise alignment of input seq and each ref until a match found
                    # 1 point for match, -1 for mistmatch, -.5 for gab, -.1 for gap extension. 
                    # Can alter scoring for looser alignments
                    align = pairwise2.align.localms(aa_seq, ref_record.seq, 1, -1, -.5, -.1, score_only=True)
            
                    #scores equal to ref length (100% alignment)
                    if align == len(ref_record.seq):
                        fasta_list.append('>%s\n%s\n' % (in_record.description + " len:" + str(len(aa_seq)), aa_seq))    
                        written = 1
                        break
    
    #write query descriptions and seqs that match ref
    with open(output + ".fna", 'a') as file:
        file.write('\n'.join(fasta_list))
        file.close()      

if __name__ == '__main__':
    main()
