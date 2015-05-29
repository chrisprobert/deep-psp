#!/bin/sh

#
# Run a given model, and save output to given location
#

BASEDIR=/home/gene245/cprobert/deep-psp/
OUTPUT_DIR=${BASEDIR}output/

MODEL=$1
OUTPUT=${OUTPUT_DIR}${2}

echo "running model ${MODEL}"
echo "writing model output to ${OUTPUT}"

python ${BASEDIR}train_model.py --model $1 --numexs 100000 --outputName $2

echo "Finished running model"
