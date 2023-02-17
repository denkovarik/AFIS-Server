#!/bin/bash
#
# This script simply forwards the call to run tests to test the performance
# of the tensorflow neural networks for ridge shade dectectino and for 
# validating minutiae.
#
# Usage:
#   ./runTensorflowNeuralNetTests.sh

# Create filepaths
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

echo "Testing Neural Network for Ridge Shade Detection"
python3 $DIR"/automatedTests/tensorflowNN/testRidgeShadeNN.py"
echo ""
echo ""
echo "Testing Neural Network for Validating Minutiae"
python3 $DIR"/automatedTests/tensorflowNN/testValidateMinutiae.py"
