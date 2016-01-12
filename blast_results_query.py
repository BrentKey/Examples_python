#!/usr/bin/env python3

#query results of BLAST alignment

import re

file = open("").read() #add input file of BLAST results

# find and print query ID and query length
query_id = re.search(r"Query=\s(.+)", file)
query_length = re.search(r'\s{2}Length=(.+)', file)
print("\tQuery ID: " + query_id.group(1) + "\n\tQuery Length: " + query_length.group(1))

# find accession, accn length, and accn score
acc = re.findall(r"\>(.+\|.+\|)", file) #also included text before accession (gb/ref)
acc_length = re.findall(r".\sLength=(.+)", file)
acc_score = re.findall(r"\s+Score\s=\s+(\d+)", file)

#print accession information
for i in range(0, 10):
	print("\nAlignment #" + str(i+1) + ": Accession = " + str(acc[i]) + "(Length = " + str(acc_length[i]) + ", Score = " + str(acc_score[i]) + ")")
	
