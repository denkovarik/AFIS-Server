#!/bin/bash
# This bash script runs bozorth algorithm on all .xyt files listed in a 
# 'probeDataset' file against all .xyt files listed in a 'gallaryDataset' file. 
# You can also pass in the filename of the matches for the fingerprints in the 
# above file. This script can be run with 0, 2, or 3 argurments. If 0 arguments 
# are provided, then the default parameters will be used. If 2 arguments are 
# provided, then those parameters will be used to specify the files listing the 
# fingerprint images to match and the file of fingerprint images to match 
# against. If 3 arguments are provided, then in addition to what happens when 
# you provide 2 arguments, the third argument specifies which file to use to 
# specify which fingerprint images match.
#
# Usage:
#       ./runBozorth 
#       ./runBozorth probeDataset gallaryDataset 
#       ./runBozorth probeDataset gallaryDataset matches.txt



# Check the number of command line arguments
if [ "$#" -eq 2 ]
then
    probeDataset=$1
    gallaryDataset=$2
else
    echo "Invalid number of command line arguments provided. This script can"
    echo "be run with 0, 2, or 3 command line arguments. The first argument is"
    echo "the filename and path of a list of fingerprint images to match, while"
    echo "the second command line argument is a list of fingerprint images to"
    echo "match against. The third argument is a file specifying which"
    echo "fingerprint images from the first to arguments match with each other."
    echo "If 0 arguments are provided, then the default parameters will be used."
    echo "If 2 arguments are provided, then those parameters will be used to"
    echo "specify the files listing the fingerprint images to match and the file"
    echo "of fingerprint images to match against. If 3 arguments are provided,"
    echo "then in addition to what happens when you provide 2 arguments, the"
    echo "third argument specifies which file to use to specify which"
    echo "fingerprint images match."
    echo " "
    echo "Usage:"
    echo "      ./runBozorth" 
    echo "      ./runBozorth probeDataset gallaryDataset" 
    echo "      ./runBozorth probeDataset gallaryDataset matches.txt"
    
    exit 1 
fi

# Test if probeDataset exists
if test ! -d $probeDataset 
then
    echo "$probeDataset does not exist" 
    echo " "
    echo "Usage:"
    echo "      ./runBozorth" 
    echo "      ./runBozorth probeDataset gallaryDataset" 
    echo "      ./runBozorth probeDataset gallaryDataset matches.txt"
    exit 2
fi

# Test if gallaryDataset exists
if test ! -f $gallaryDataset
then
    echo "$gallaryDataset does not exist"
    echo " "
    echo "Usage:"
    echo "      ./runBozorth" 
    echo "      ./runBozorth probeDataset gallaryDataset" 
    echo "      ./runBozorth probeDataset gallaryDataset matches.txt"
    exit 3
fi

for entry in $probeDataset*
do
    #./bin/bozorth3 -T 40 -A outfmt=spg -p $line -G $gallaryDataset >> results.txt
    echo $entry
    # Match a single fingerprint against a database
    filename=${entry##*/}
    ext="$(cut -d'.' -f 2 <<<"$filename")"
    if [ $ext == "xyt" ]
    then
        ./bin/bozorth3 -T 40 -A outfmt=spg -p "temp/"$filename -G $gallaryDataset
    fi
done
