#!/usr/bin/env python

import argparse

"""
File: process_tsv.py

Get the specified annotation regions from a uniprot TSV and
write them to a file.

"""

def main() :
	"""
	Read command line arguments and invoke filterTSV()
	"""

	parser = argparse.ArgumentParser(description='Filter a uniprot TSV based on annotation')
	parser.add_argument('--inputTSV', help='input TSV file', required=True)
	parser.add_argument('--outputTSV', help='output TSV file', required=True)
	parser.add_argument('--annot', help='annotation to select', required=True)
	parser.add_argument('--minlen', help='minimum length', required=True)
	parser.add_argument('--maxlen', help='maximum length', required=True)
	args = parser.parse_args()

	filterTSV(args.annot, args.maxlen, args.minlen, args.inputTSV, args.outputTSV)

def filterTSV(annot, maxlen, minlen, input_tsv, output_path) :

	"""
	Get all of the specified annotation regions from a TSV that have
	minlen <= length <= maxlen. Write them to a TSV file.
	"""

	with open(output_path, 'w') as out_f :
		for line in open(input_tsv) :
			if len(line) < 1 or line[0] == '#' : continue
			l = line.split('\t')
			if l[1] != annot : continue
			start = int(l[3])
			stop = int(l[4])
			length = stop - start
			if length < minlen or length > maxlen : continue
			seq = l[5]
			out_f.write('%s\t%s\t%s\t%s' % (l[0], l[1], l[2], seq))

if __name__ == '__main__' : main()