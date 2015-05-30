#!/bin/sh

#
# Run a given model, and save output to given location
#


BASEDIR=/home/gene245/cprobert/deep-psp/keras/
OUTPUT_DIR=${BASEDIR}output/

MODEL=$1
OUTPUT=${OUTPUT_DIR}${2}
NUMEXS=$3

echo ">>running model ${MODEL}"
echo ">>writing model output to ${OUTPUT}"
echo ">>using ${NUMEXS} examples"

python ${BASEDIR}train_model.py --model $MODEL --numexs $NUMEXS --outputName $OUTPUT > ${OUTPUT}_log.txt

echo ">>Finished running model"
