#!/bin/bash

# This bash script runs bozorth algorithm on all .xyt files listed in a 
# 'probeDataset' directory against all .xyt files listed in a 'gallaryDataset' file. 
# This script must be run with 2 additional argurments. The first arguments 
# specifies the directory containing the probe fingerpint .xyt files. The second
# argument is a file containing a list of gallary fingerprint .xyt files to 
# match the probe fingerprints against.
#
# Usage:
#       ./runBozorth probeDataset gallaryDataset 


# Check the number of command line arguments
if [ "$#" -eq 2 ]
then
    probeDataset=$1
    gallaryDataset=$2
else
    echo "This bash script runs bozorth algorithm on all .xyt files listed in a"
    echo "'probeDataset' directory against all .xyt files listed in a 'gallaryDataset' file."
    echo "This script must be run with 2 additional argurments. The first arguments" 
    echo "specifies the directory containing the probe fingerpint .xyt files. The second"
    echo "argument is a file containing a list of gallary fingerprint .xyt files to" 
    echo "match the probe fingerprints against."
    echo""
    echo "Usage:"
    echo "      ./runBozorth probeDataset gallaryDataset"
    
    exit 1 
fi

# Test if probeDataset exists
if test ! -f $probeDataset 
then
    echo "$probeDataset does not exist" 
    echo " "
    echo "Usage:"
    echo "      ./runBozorth probeDataset gallaryDataset" 
    exit 2
fi

# Test if gallaryDataset exists
if test ! -f $gallaryDataset
then
    echo "$gallaryDataset does not exist"
    echo " "
    echo "Usage:"
    echo "      ./runBozorth probeDataset gallaryDataset" 
    exit 3
fi

while read line; 
do
	#echo "$line"
    #./bin/bozorth3 -T 40 -A outfmt=spg -p $line -G $gallaryDataset >> results.txt

    # Match a single fingerprint against a database
    ./bin/bozorth3 -T 40 -A outfmt=spg -p "$line" -G $gallaryDataset
done < $probeDataset
