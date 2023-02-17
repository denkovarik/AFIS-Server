#!/bin/bash
#
# This script simply forwards the call to run the matching tests.
# This will run matching tests for the nanoparticle images. For this 
# test, the matching results of minutiaeOut will be compared with that of the
# mindtct. This means that the features will be extracted using both the mindtct
# and the minutiaeOut algorithms. For the MinutiaeOut algorithm, the images 
# will be enhanced before the features are extracted. This script should work
# from any directory, and it requires no arguments.
#
# Usage:
#   ./runMatchingTests

# Create filepaths
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

$DIR"/automatedTests/matching/runMatchingTests.sh"
