# This script simple converts the file type for an image. This script requires 
# two arguments, which are the filepath and filename of the image to convert 
# and the filepath and filename (with the new filetype appended to the end) for
# the converted output file.
#
# This script was written for converting wsq images to jpg, but it should be 
# able to convert an image to whatever filetpes that the python PIL module 
# supports in addition to converting images from or to the .wsq filetype. This
# script has minimal error checking and has only been minimally tested.
#
# Usage: 
#   python3 convertImgType.py inputImgToCnvrt cnvrtedOutputImg
 
#import io
import os
import sys
import PIL.Image as Image
import wsq

def cnvrtImgType(inImg, outImg):
    # Open the image
    IM = Image.open(inImg)

    # Resize the Image
    width, height = IM.size
    aspectRatio = float(width) / height
    newHeight = 500
    newWidth = newHeight * aspectRatio
    IM = IM.resize((int(newWidth), int(newHeight)))

    # Display for debugging
    IM.show()

    # Save the image
    IM = IM.save(outImg)


# Check the number of command line arguments
if len(sys.argv) != 3:
    print("Invalid number of command line arguments")
    print()
    print("This script simple converts the file type for an image. This ")
    print("script requires two arguments, which are the filepath and filename ")
    print("of the image to convert and the filepath and filename (with the ")
    print("new filetype appended to the end) for the converted output file.")
    print()
    print("Usage:") 
    print("\tpython3 convertImgType.py inputImgToCnvrt cnvrtedOutputImg")
    exit()

inImg = sys.argv[1]
outImg = sys.argv[2]

# Check that input image exists
if not os.path.isfile(inImg):
    print ("Image '" + inImg + "' does not exist. Quitting")
    exit()

cnvrtImgType(inImg, outImg)
