/*****************************************************************************
* This program finds the number of true positives and false positives from a 
* file containing the matching results from using the BOZORTH3 tool. This 
* program will analyze the matching result for either the MOLF dataset or the
* nanopartiles datase, but a flag must be passed into the program so it can 
* determine the true matching prints. To analyze the matching results for
* images from the Nanopartiles dataset pass in the '-NanoParticles' flag into
* the program. To analyze matching results from the MOL dataset, pass in the
* '-MOLF' flag into the program.
* 
* compile: g++ analyzeResults.cpp utilities.cpp -o bin/analyzeResults
*
* Usage: 
*   ./bin/analyzeResults -Nanoparticles <nanoparticle Matching Results File.txt>
*   ./bin/analyzeResults -MOLF <MOLF matching Results File.txt>
*   ./bin/analyzeResults -match_by_same_name <results file>
*
*****************************************************************************/
#include "utilities.h"

using namespace std;


/**************************************************************************//**
* @author Dennis Kovarik
*
* @par Description:
* This is the main function which is the start of the program. 
*
* @param[in] argc - Int of of the number of command line arguments
* @param[in] argv - Character array of the command line arguments
*
* @returns 0 if no errors occured
* @returns 1 if file could not be opened
*
******************************************************************************/
int main(int argc, char **argv)
{
    ifstream fin;
    string filename, probeSub, probeFinger, galleySub, galleyFinger, match_criteria;
    vector<vector<string>> matches;
    int truePos = 0, falsePos = 0;

    // Read in command line arguments
    if(argc != 3)
    {
        cout << "Invalid number of command line arguments" << endl << endl;
        cout << "Usage:" << endl;
        cout << "\t./analyze -Nanoparticles <nanoparticle Matching Results File.txt>" << endl;
        cout << "\t./analyze -MOLF <MOLF matching Results File.txt>" << endl;
        return 1;
    }

    match_criteria = argv[1];
    filename = argv[2];

    if(!(match_criteria == "-Nanoparticles" || match_criteria == "-MOLF" 
    || match_criteria == "-match_by_same_name"))
    {
        cout << "Invalid dataset" << endl << endl;
        cout << "Usage:" << endl;
        cout << "\t./analyze -Nanoparticles <nanoparticle Matching Results File.txt>" << endl;
        cout << "\t./analyze -MOLF <MOLF matching Results File.txt>" << endl;
        return 2;
    }

    openFile(filename, fin);

    readFile(matches, fin);

    for(int i = 0; i < matches.size(); i++)
    {
        if(isMatch(matches[i], match_criteria))
        {
            truePos++;
        }
        else
        {
            falsePos++;
        }
    }

    cout << "True Positives: " << truePos << endl;
    cout << "False Positives: " << falsePos << endl;

    return 0;
}
