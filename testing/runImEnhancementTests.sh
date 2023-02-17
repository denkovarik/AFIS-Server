#!/bin/bash
#
# This script simply forwards the call to run image enhancement tests.
#
# Usage:
#   ./runImEnhancementTests

# Create filepaths
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

python3 $DIR"/automatedTests/imEnhancement/imEnhancementTests.py"
