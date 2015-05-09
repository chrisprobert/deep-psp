#!/bin/sh
source /home/${USER}/.bash_profile

#
# convert the given XML file to TSV
#


# source directory for uniprot parser
export SOURCE_DIR=/home/${USER}/deep-psp/uniprot_parser/

# uniprot data directory
export UNIPROT_DIR=${PI_HOME}/uniprot_data/

# uniprot file to convert
export UNIPROT_XML=${UNIPROT_DIR}uniprot.xml

# output TSV file
export UNIPROT_TSV=${UNIPROT_XML}.tsv


python ${SOURCE_DIR}xml_to_tsv.py --uniprotXML ${UNIPROT_XML} --outputTSV ${UNIPROT_TSV}

