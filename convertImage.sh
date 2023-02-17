#!/bin/bash
# This bash script copies .jpg images from on directory to the images directory.
# In addition, each image copied is converted from a .jpg image format to a 
# .wsq image format. 



outputDirectory='temp/'
jpgExt='.jpg'
rawExt='.raw'
ncmExt='.ncm'
wsqExt='.wsq'

if [ "$#" -eq 1 ] 
then
    outputDirectory=$1
fi

curDir=${PWD##*/}

# Test if outputDirectory exists
if test ! -d $outputDirectory
then
    echo "$outputDirectory does not exist"
    exit 4
fi

for entry in $outputDirectory*
do
    filename=${entry##*/}
    rootFilename="$(cut -d'.' -f 1 <<<"$filename")"

    ./bin/djpegb raw "$outputDirectory$rootFilename$jpgExt" -r

    width="$(cat "$outputDirectory$rootFilename$ncmExt" | grep "PIX_WIDTH")"
    width=${width##* }
    height="$(cat "$outputDirectory$rootFilename$ncmExt" | grep "PIX_HEIGHT")"
    height=${height##* }
    depth="$(cat "$outputDirectory$rootFilename$ncmExt" | grep "PIX_DEPTH")"
    depth=${depth##* }
    ppi="$(cat "$outputDirectory$rootFilename$ncmExt" | grep "PPI")"
    ppi=${ppi##* }
    
    ./bin/cwsq 0.75 wsq "$outputDirectory$rootFilename$rawExt" -r $width,$height,$depth,$ppi
done
