#!/usr/bin/env python

import argparse
from xml_parser import xml_parser
from xml_stream_handler import xml_id_annot_seq_to_file as xml_handler


"""
File: xml_to_tsv.py

Parse a uniprot XML file and output as a TSV. Reads input/output
file paths from command line arguments.

"""


def main() :
	"""
	Read command line arguments and invoke xml_to_tsv()
	"""

	parser = argparse.ArgumentParser(description='Parse a uniprot XML file and output as a TSV.')
	parser.add_argument('--uniprotXML', help='path to uniprot XML file', required=True)
	parser.add_argument('--outputTSV', help='path to write output TSV file', required=True)
	args = parser.parse_args()

	xml_to_tsv(args.uniprotXML, args.outputTSV)


def xml_to_tsv(xml_path, tsv_path) :
	"""
	Wrapper function for xml_parser and xml_stream_handler.

	"""
	stream_handler = xml_handler(tsv_path)
	parser = xml_parser(stream_handler)
	parser.parse_xml_file(xml_path)

if __name__ == '__main__' : main()