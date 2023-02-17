#!/bin/bash
#
# This script will run all the manual tests for the image enhancement and 
# feature extration modules. These tests rely on dispalying images in order
# to test the modules. These tests may require X server to run. Note that 
# there is no instruction on how to set this up on the server. These tests are 
# best run on a local computer in a linux environment. For windows users running
# a linux sub shell, Xming will need to be installed to run X server.
#
# Usage:
#   ./runManualTests.sh

# Create filepaths
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

echo "Testing Fingerprint Segmentation from the Image Enhancement Module"
python3 $DIR"/manualTests/imEnhancement/testRidgeSegment.py"
echo ""
echo "Testing Image Enhancement"
python3 $DIR"/manualTests/imEnhancement/testEnhanceFingerprintImage.py"
echo ""
echo "Testing Feature Extraction"
python3 $DIR"/manualTests/featureExtraction/testFeatureExtraction.py"
