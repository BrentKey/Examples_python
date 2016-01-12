#!/usr/bin/env python3

"""
Remove spliced genes from a GFF file using Args Parser

"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser( description='Put a description of your script here')

    # output file to be written
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Path to an input file to be read' )
    args = parser.parse_args()
    cds_count = 0
    lines = list()

    # iterate through file, line by line
    for line in open(args.input_file):
        line = line.rstrip()
        cols = line.split("\t")

        if len(cols) != 9:
            print(line)
            continue

        # the tab-delimited column lines
        type = cols[2]

        if type == 'CDS':
            cds_count += 1
        elif type == 'gene':
            ## process what we've seen so far
            if cds_count == 1:
                for l in lines:
                    print(l)

            ## reset short-term memory of the last entry
            cds_count = 0
            lines = list()

        lines.append(line)

    # check the last gene
    if cds_count == 1:
        for l in lines:
            print(l)

if __name__ == '__main__':
    main()
