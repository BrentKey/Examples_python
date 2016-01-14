#!/usr/bin/env python3

# Summarize FASTA file with regards to protein lengths
# Return count of genes, average protein length, maximum and minimum protein lengths

from __future__ import division
import re

file = open("", "r") #add filename

#gene count
g_count = 0

#protein length
protein_length = 0
min_protein = 2000
max_protein = 0
total_protein = 0
for line in file:
     if ">gi" not in line:
          protein_length = len(line) + protein_length
     else:
          g_count = g_count + 1
          if (protein_length > 0 and protein_length < min_protein): 
               min_length = protein_length #if protein is less than previous minumum, reassign
          if (protein_length > max_protein):
               max_protein = protein_length #if protein is greater than previous max, reassign
          total_protein = total_protein + protein_length
          protein_length = 0
                       
file.close()

#count of hypothetical genes
file = open("e_coli_k12_dh10b.faa", "r")
hypo_count = 0
for line in file:
     if "hypothetical" in line:
          hypo_count = hypo_count + 1
    
file.close()
          
avg_protein = total_protein//g_count              
          
#print information
print("Gene Count: " + str(g_count))
print("Minimum Protein Length: " + str(min_protein))
print("Maximum Protein Length: " + str(max_protein))
print("Average Protein Length: " + str(avg_protein))
print("Hypothetical Genes: " + str(hypo_count))
