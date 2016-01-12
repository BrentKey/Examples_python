#!/usr/bin/env python3

#Search gff file for specific geneID, return ID and coordinates of the nucleotide sequence within the genome
#If nucleotide sequence is for the negative strand, return reverse complement

coord_list = []

#find gene and ID, split string, append list with data being searched for
def get_feat_coord(gff_file):
	my_file = open(gff_file)
	for line in my_file.readlines():
		split_string = line.split("\t")
		if split_string[0].startswith(">"):
			break
		if split_string[0].startswith("#"):
			continue
		elif (split_string[2] == 'gene') & (split_string[8].startswith("ID=YAR003W")):	#update geneID to refine search		
			coord_list.extend([split_string[0], split_string[3], split_string[4], split_string[6]])
	my_file.close()
	print(">geneID:" + "YAR003W") #update gene ID to refine input

	
seq_bases = ''
seq_area = False
#search for chromosome name, record all base pair residues for the chromosome
def get_seq(gff_file):
	my_file = open(gff_file)
	global seq_bases
	global seq_area
	for line in my_file.readlines():
		line = line.rstrip()
		if line.startswith(">"):
			if line == ">{0}".format(coord_list[0]):
				seq_area = True
			else:
				seq_area = False
		elif seq_area:
			seq_bases += line
	if coord_list[3] == '-':	
		print(rev_comp(seq_bases[(int(coord_list[1])-1):int(coord_list[2])]))
	else:
		print(seq_bases[(int(coord_list[1])-1):int(coord_list[2])])
	return
	

#reverse complement, if DNA strand is on the negative side	
def rev_comp (seq):
	seq1 = seq.replace('A', 't')
	seq2 = seq1.replace('T', 'a')
	seq3 = seq2.replace('C', 'g')
	seq4 = seq3.replace('G', 'c')
	rseq = seq4[::-1]
	return(rseq.upper())
	
	
def main ():
	get_feat_coord("") #add gff input file
	get_seq("") #add gff input file
	return
	
if __name__ == '__main__':
    main()
