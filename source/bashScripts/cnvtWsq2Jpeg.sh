#!/bin/bash
# This bash script converts a .wsq image file to a .jpeg fileusing the cjpegb 
# executable provide by the NIST Biometric software. This executable can be 
# found in the bin/ directory. This script takes 1 or 2 command line arguments, 
# which are the filepath and name for the input .wsq image to convert and the
# filepath of the directory to write the output jpeg file to. The output file 
# will have the same name as the input file.
#
# Usage:    cnvtWsq2Jpeg.sh inImage.wsq
#           cnvtWsq2Jpeg.sh inImage.wsq outDir


jpegExt='jpeg'
rawExt='raw'
wsqExt='wsq'
ncmExt='ncm'

inputImagePath='thepath/DoesNotExist'
imageName='DoesNotExist'
inDir=""
outDir=""

# Check for correct number of command line arguments
if [ "$#" -eq 1 ]
then
    inputImagePath=$1
elif [ "$#" -eq 2 ]
then
    inputImagePath=$1
    outDir=$2
else
    echo "Invalid number of command line argurments."
    echo "This bash script converts a .wsq image file to a .jpeg fileusing the cjpegb "
    echo "executable provide by the NIST Biometric software. This executable can be "
    echo "found in the bin/ directory. This script takes 2 command line arguments, "
    echo "which are the filepath and name for the input .raw image to convert and the "
    echo "filepath of the directory to write the output jpeg file to. The output file "
    echo "will have the same name as the input file."
    echo ""
    echo "Usage:    cnvtWsq2Jpeg.sh inImage.wsq"
    echo "          cnvtWsq2Jpeg.sh inImage.wsq outDir"

    exit 1;
    
fi

# Test if the input file exists
if test ! -f $inputImagePath
then
    echo "$inputImagePath does not exist"

    exit 2
fi

fileType="$(echo "$inputImagePath" | rev | cut -d'.' -f1 | rev)"
inDir="$(echo "$inputImagePath" | rev | cut -d'.' -f2- | rev)"
inDir="$(echo "$inDir" | rev | cut -d'/' -f2- | rev)/"

# Ensure image filetype is .wsq
if [ "$fileType" != "$wsqExt" ]
then
    echo "Invalid filetype. Input image must be a .wsq image."
    echo "This bash script converts a .wsq image file to a .jpeg fileusing the cjpegb "
    echo "executable provide by the NIST Biometric software. This executable can be "
    echo "found in the bin/ directory. This script takes 2 command line arguments, "
    echo "which are the filepath and name for the input .raw image to convert and the "
    echo "filepath of the directory to write the output jpeg file to. The output file "
    echo "will have the same name as the input file."
    echo ""
    echo "Usage:    cnvtWsq2Jpeg.sh inImage.wsq"
    echo "          cnvtWsq2Jpeg.sh inImage.wsq outDir"

    exit 3
fi

# Extract the image name from the input filepath
imageName="$(echo "$inputImagePath" | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)"

# Test if outputDirectory exists
if test ! -d $outDir
then
    echo "$outDir does not exist"
    exit 4
fi

# Decompress from .wsq to .raw and .ncm
./../../bin/dwsq raw "$inputImagePath" -r

# Extract the width, height, depth, and ppm from .ncm image producted
width="$(cat "$inDir$imageName.$ncmExt" | grep "PIX_WIDTH")"
width=${width##* }
height="$(cat "$inDir$imageName.$ncmExt" | grep "PIX_HEIGHT")"
height=${height##* }
depth="$(cat "$inDir$imageName.$ncmExt" | grep "PIX_DEPTH")"
depth=${depth##* }
ppi="$(cat "$inDir$imageName.$ncmExt" | grep "PPI")"
ppi=${ppi##* }

 
# Compress .raw image to .jpeg   
./../../bin/cjpegl jpl "$inDir$imageName.$rawExt" -r $width,$height,$depth,$ppi

# Copy .jpeg image from input directory to the output directory
#cp "$inDir$imageName.jpg" "$outDir$imageName.jpeg"

# Delete .raw, .ncm, and .jpeg files from input directory
#rm "$inDir$imageName.raw"
#rm "$inDir$imageName.ncm"
#rm "$inDir$imageName.jpeg"
