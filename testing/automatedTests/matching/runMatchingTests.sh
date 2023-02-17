#!/bin/bash
#
# This script will run matching tests for the nanoparticle images. For this 
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
projRootPath="$(cd -P ../../../; pwd)/"
genXytMinutiaeFilesPath=$projRootPath"source/pythonScripts/genXytMinutiaeFiles.py"
nanoJpgDir=$projRootPath"testing/images/Nanoparticle_Images_jpg/"
nanoWsqDir=$projRootPath"testing/images/Nanoparticle_Images_wsq_invertedGrayscale/"
mindtctXytPath=$projRootPath"testing/automatedTests/matching/mindtctXyt/"
minutiaeOutXytPath=$projRootPath"testing/automatedTests/matching/minutiaeOutXyt/"
matchingTestDir=$projRootPath"testing/automatedTests/matching/"
lisFilesDir=$matchingTestDir"lisFiles/"
matchingResults=$matchingTestDir"matchingResults/"
runMindtct=$projRootPath"testing/automatedTests/matching/runMindtct.sh"
countMatches=$matchingTestDir"bin/countMatches"
analyzeResults=$matchingTestDir"bin/analyzeResults"

# Check if cpp executables exist
if [[ ! -r $countMatches ]] || [[ ! -f $analyzeResults ]]
then
    make
fi

echo "Running Matching Tests on Fingerprint Images Collected Using the Upconverting Nanoparticles"
echo ""

rm -rf $lisFilesDir 2>/dev/null || true 
rm -rf $mindtctXytPath $minutiaeOutXytPath 2>/dev/null || true
rm -rf $matchingResults 2>/dev/null || true

# Generate mindtct .xyt files
echo "Generating mindtct .xyt files"
if [[ ! -d $mindtctXytPath ]]
then
    mkdir $mindtctXytPath
    chmod a+r $mindtctXytPath
    chmod a+w $mindtctXytPath
fi
$runMindtct $nanoWsqDir $mindtctXytPath

# Generate minutiaeOut .xyt files
echo "Generating minutiaeOut .xyt files."
echo "    This may take a few minutes..."
if [[ ! -d $minutiaeOutXytPath ]]
then
    mkdir $minutiaeOutXytPath
    chmod a+r $minutiaeOutXytPath
    chmod a+w $minutiaeOutXytPath
fi
python3 $genXytMinutiaeFilesPath $nanoJpgDir $minutiaeOutXytPath

# Generate .lis file for mindtct output
if [[ ! -d $lisFilesDir ]]
then
    mkdir $lisFilesDir
    chmod a+r $lisFilesDir
    chmod a+w $lisFilesDir
fi
ls $mindtctXytPath | grep .xyt | sed s%^%$mindtctXytPath%g > $lisFilesDir"nanoparticlesMindtctXyt.lis"

# Generate .lis file for minutiaeOut output
ls $minutiaeOutXytPath | grep .xyt | sed s%^%$minutiaeOutXytPath%g > $lisFilesDir"nanoparticlesMinutiaeOutXyt.lis"

if [[ ! -d $matchingResults ]]
then
    mkdir $matchingResults
    chmod a+r $matchingResults
    chmod a+w $matchingResults
fi

runBozorthMatchingTest=$matchingTestDir"runBozorthMatchingTest.sh"
nanoMindtctLisFile=$lisFilesDir"nanoparticlesMindtctXyt.lis"
nanoMinutiaeOutLisFile=$lisFilesDir"nanoparticlesMinutiaeOutXyt.lis"
nanoMindtctMatchingResults=$matchingResults"nanoparticlesMindtctMatchingResults.txt"
nanoMinutiaeOutMatchingResults=$matchingResults"nanoparticlesMinutiaeOutMatchingResults.txt"

# Perform Matching for Mindtct
echo "Matching Fingerprints based on Mindtct extracted Features"
$runBozorthMatchingTest $nanoMindtctLisFile $nanoMindtctLisFile > $nanoMindtctMatchingResults

# Perform Matching for MinutiaeOut
echo "Matching Fingerprints based on MinutiaeOut extracted Features"
$runBozorthMatchingTest $nanoMinutiaeOutLisFile $nanoMinutiaeOutLisFile > $nanoMinutiaeOutMatchingResults


echo ""
echo "================================================================================"
echo "Analyzing Matching Results"
echo "--------------------------------------------------------------------------------"
# Count the total number of correct matches
$countMatches '-Nanoparticles' $nanoMindtctLisFile $nanoMindtctLisFile
echo "--------------------------------------------------------------------------------"
echo ""

# Analyze Mindtct results
echo "Matching results for Mindtct"
echo "--------------------------------------------------------------------------------"
$analyzeResults '-Nanoparticles' $nanoMindtctMatchingResults
echo "--------------------------------------------------------------------------------"
echo""

# Analyze MinutiaeOut results
echo "Matching results for MinutiaeOut"
echo "--------------------------------------------------------------------------------"
$analyzeResults '-Nanoparticles' $nanoMinutiaeOutMatchingResults
echo "--------------------------------------------------------------------------------"
echo "================================================================================"
