#!/bin/bash
# This bash script copies .jpg images from on directory to the images directory.
# In addition, each image copied is converted from a .jpg image format to a 
# .wsq image format.

inputDirectory='/mnt/c/Users/1985937/Documents/MATLAB/Fingerprint/Images/UpdatedProcessedImages/grayscaleImages/'
outputDirectory='images/'
jpgExt='.jpg'
rawExt='.raw'
ncmExt='.ncm'
wsqExt='.wsq'

if [ "$#" -eq 1 ] 
then
    inputDirectory=$1
elif [ "$#" -eq 2 ]
then
    inputDirectory=$1
    outputDirectory=$2
elif [ "$#" -gt 0 ] 
then
    echo "Invalid number of arguments. This script can be run with 0, 1, or 2"
    echo "arguments, where the first argument is the file path of the input"
    echo "directory from which the images will be copied from. The second"
    echo "argument is the file path to the directory where the images will be"
    echo "copied to. If no arguments are provided, then the default file paths"
    echo "for both the input and output directories will be used, which is"
    echo "specific to Dennis' file system. If one argument is provided, then"
    echo "the input directory will be set to the file path provided. If 2"
    echo "arguments are provided, then both the input and output directories"
    echo "will be set the the 1st and 2nd command line arguments respectively."
    echo " "
    echo "usage:    ./copyAndConvertImages.sh"
    echo "          ./copyAndConvertImages.sh inputDir"
    echo "          ./copyAndConvertImages.sh inputDir outputDir"

    exit 1;
    
fi

curDir=${PWD##*/}

# Test if the input directory exists
if test ! -d $inputDirectory
then
    echo "$inputDirectory does not exist"
    exit 3
fi

# Test if outputDirectory exists
if test ! -d $outputDirectory
then
    echo "$outputDirectory does not exist"
    exit 4
fi



for entry in $inputDirectory*
do
    filename=${entry##*/}
    filename="$(cut -d'.' -f 1 <<<"$filename")"
    newFilename="$(sed -r 's/[ -]+/_/g' <<<"$filename")"

    echo "copying $filename into directory $outputDirectory"
    cp "$inputDirectory$filename$jpgExt" "$outputDirectory$newFilename$jpgExt"

    echo "Converting image type from .jpg to .raw for $newFilename"
    ./bin/djpegb raw "$outputDirectory$newFilename$jpgExt" -r

    echo "Reading .ncm file for $newFilename"
    width="$(cat "$outputDirectory$newFilename$ncmExt" | grep "PIX_WIDTH")"
    width=${width##* }
    height="$(cat "$outputDirectory$newFilename$ncmExt" | grep "PIX_HEIGHT")"
    height=${height##* }
    depth="$(cat "$outputDirectory$newFilename$ncmExt" | grep "PIX_DEPTH")"
    depth=${depth##* }
    ppi="$(cat "$outputDirectory$newFilename$ncmExt" | grep "PPI")"
    ppi=${ppi##* }
    
    echo "Converting image format from .raw to .wsq for $newFilename"
    ./bin/cwsq 0.75 wsq "$outputDirectory$newFilename$rawExt" -r $width,$height,$depth,$ppi
done
