#!/usr/bin/env python3

#Input FASTQ sequencing file, from multiplex run
#Bins DNA sequences into individual files based on tags provided prior to sequencing
#Only copies sequences between 200-300 nucleotides and removes sequences with low quality scores
#Author: Brent Key

import sys
import re


def main():
    #open and read file
    filename = sys.argv[-1]
    file = open(filename, 'rU')
    
    #maintains accuracy throughout iteration of file
    prev = "four"

    for line in file:
        if line.startswith("@") and prev == "four":
            line1 = line.strip()
            prev = "three"
            
            #match length, remove sequences outside 200-300
            length = re.search(r'length\S(\d+)', line)
            size = int(length.group(1))
            if size >= 200 and size <= 300:
                chk = "yes"
            else:
                chk = "no"
                
        elif line.startswith("TCAG") and prev == "three":
            line2 = line.strip()
            prev = "two"    
            mid = re.match(r'TCAG(\w{10})', line)
            tag = mid.group(1)
            
        elif line.startswith("+") and prev == "two":
            line3 = line.strip()
            prev = "one"
        
        elif prev == "one":
            line4 = line.strip()
            prev = "four"
            
            #remove low FASTQ quality scores, do not bin these sequences
            if re.search(r'[!"$%$&\'\(\)\*\+,\-]', line):
                chk = "no"
                continue
                
            #bin to out_file based on sequence tag
            elif chk == "yes":
                if tag == "ACGAGTGCGT": #Western 1 month post colonization
                    out_file = "" #add file 1 name
                elif tag == "AGACGCACTC": #LF 4wk/1day post colonization
                    out_file = "" #add file 2 name
                elif tag == "AGCACTGTAG": # Western 1 day post diet switch
                    out_file = "" #add file 3 name
                elif tag == "ATCAGACACG": #LF 5 wks post colonization
                    out_file = "" #add file 4 name
                elif tag == "ATATCGCGAG": #Western 1 week post diet switch
                    out_file = "" #add file 5 name
                elif tag == "CGTGTCTCTA": #human donor sample
                    out_file = "" #add file 6 name
                elif tag == "CTCGCGTGTC": #LF 1 day post colonization
                    out_file = "" #add file 7 name
                elif tag == "TAGTATCAGC": #Western 1 day post colonization
                    out_file = "" ##add file 8 name
                elif tag == "TCTCTATGCG": #LF 1 week post colonization
                    out_file = "" #add file 9 name
                elif tag == "TGATACGTCT": #Western  1 week post colonization
                    out_file = "" #add file 10 name
                elif tag == "TACTGAGCTA": #LF 1 month post colonization
                    out_file = "" #add file 11 name
                else:              
                    out_file = "overflow.fastq" #any sequences without proper tags
                
                output = open(""+out_file, 'a') #add directory path for writing files
                output.write(line1)
                output.write("\n")
                output.write(line2)
                output.write("\n")
                output.write(line3)
                output.write("\n")
                output.write(line4)
                output.write("\n")
                output.close()
                chk = "no"
            else:
                continue
        else:
            continue
            
if __name__ == '__main__':
    main()
