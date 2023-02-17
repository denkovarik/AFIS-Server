#!/bin/bash
# This bash script runs the NIST mindtct algorithm on all .wsq files within 
# a specified directory, and it will write the results to another specified 
# directory. The input directory (the directory containing the images to 
# extract minutia from) is passed in as the first command line argument. The 
# output directory (where the output files produced from the mindtct algorithm
# are written to) is passed in as the second command line argument. If no 
# arguments areprovided, then the default file paths for both the input and
# output directories will be used, which is specific to Dennis' file system. 
# If one argument is provided, then the input directory will be set to the file 
# path provided. If 2 arguments are provided, then both the input and output 
# directories will be set the the 1st and 2nd command line arguments 
# respectively.
#
# Usage:
#       ./runMindtct
#       ./runMindtct inputDir
#       ./runMindtct inputDir outputDir



# Check the number of command line arguments
if [ "$#" -eq 0 ] 
then
    inputDir='images/'
    outputDir='mindtctOutput/'
elif [ "$#" -eq 1 ]
then
    inputDir=$1
    outputDir='mindtctOutput/'
elif [ "$#" -eq 2 ]
then
    inputDir=$1
    outputDir=$2
else
    echo "Invalid number of arguments. This script can be run with 0, 1, or 2"
    echo "arguments, where the first argument is the file path of the input"
    echo "directory from which the mindtct algorithm will be run on. The second"
    echo "argument is the file path to the directory where the images produced"
    echo "from the mindtct algorithm will be copied to. If no arguments are"
    echo "provided, then the default file paths for both the input and"
    echo "output directories will be used, which is specific to Dennis' file"
    echo "system. If one argument is provided, then the input directory will be"
    echo "set to the file path provided. If 2 arguments are provided, then both" 
    echo "the input and output directories will be set the the 1st and 2nd"
    echo "command line arguments respectively."
    echo " "
    echo "usage:    ./runMindtct.sh"
    echo "          ./runMindtct.sh inputDir"
    echo "          ./runMindtct.sh inputDir outputDir"

    exit 1;
fi

# Test if inputDir exists
if test ! -d $inputDir 
then
   echo "$inputDir does not exist" 
    echo "usage:    ./runMindtct.sh"
    echo "          ./runMindtct.sh inputDir"
    echo "          ./runMindtct.sh inputDir outputDir"
    exit 2
fi

# Test if outputDir exists
if test ! -d $outputDir
then
    echo "$outputDir does not exist"
    echo "usage:    ./runMindtct.sh"
    echo "          ./runMindtct.sh inputDir"
    echo "          ./runMindtct.sh inputDir outputDir"
    exit 3
fi



dir=$inputDir
for entry in $dir*
do
    filename=${entry##*/}
    ext="$(cut -d'.' -f 2 <<<"$filename")"
    if [ $ext == "wsq" ]
    then
		outputFilename=$filename
        outputFilename="$(cut -d'.' -f 1 <<<"$outputFilename")"
        inputFilePath=$inputDir$filename
        outputFilePath=$outputDir$outputFilename
        ./bin/mindtct "$inputFilePath" "$outputFilePath"
    fi
done
