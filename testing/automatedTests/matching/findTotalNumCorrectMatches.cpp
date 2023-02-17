/*****************************************************************************
* This program determines the total number of matching prints based on a 
* nameing scheme. This program expects 2 other arguments passed into it on the 
* command line which includes the file paths for a list of probe fingerprints 
* and a list of gallery fingerprints to match against. These two lists are 
* both have the extension of '.lis'. Each list is composed of a set of 
* fingerprints for matching, where each line in this file represents a 
* fingerprint, and each fingerprint is represented as the 
* filepath to its respective .xyt file. This program will work with either
* the MOLF or the Nanoparticles dataset.
* 
* compile: g++ findTotalNumCorrectMatches.cpp -o countMatches
*
* Usage: 
*   ./countMatches -MOLF probeDataset.lis galleryDataset.lis
*   ./countMatches -Nanoparticles probeDataset.lis galleryDataset.lis
*
*****************************************************************************/

#include <iostream>
#include <string>
#include <vector>
#include <fstream>

using namespace std;


bool isMatch(std::string probe, std::string galley, std::string database)
{
    if(database == "-Nanoparticles")
    {
        if(probe == "1532_1")
        {
            if(galley == "1532_1" || galley == "1532_12")
                return true;
        }
        else if(probe == "1532_2")
        {
            if(galley == "1532_13" || galley == "1532_2")
                return true;
        }
        else if(probe == "1532_3")
        {
            if(galley == "1532_14" || galley == "1532_3")
                return true;
        }
        else if(probe == "1532_4")
        {
            if(galley == "1532_5" || galley == "1532_4")
                return true;
        }
        else if(probe == "1532_5")
        {
            if(galley == "1532_4" || galley == "1532_5")
                return true;
        }
        else if(probe == "1532_6")
        {
            if(galley == "1532_10" || galley == "1532_6")
                return true;
        }
        else if(probe == "1532_7")
        {
            if(galley == "1532_8" || galley == "1532_9" || galley == "1532_7")
                return true;
        }
        else if(probe == "1532_8")
        {
            if(galley == "1532_8" || galley == "1532_9" || galley == "1532_7")
                return true;
        }
        else if(probe == "1532_9")
        {
            if(galley == "1532_8" || galley == "1532_9" || galley == "1532_7")
                return true;
        }
        else if(probe == "1532_10")
        {
            if(galley == "1532_10" || galley == "1532_6")
                return true;
        }
        else if(probe == "1532_11")
        {
            if(galley == "1532_11")
                return true;
        }
        else if(probe == "1532_12")
        {
            if(galley == "1532_12" || galley == "1532_1")
                return true;
        }
        else if(probe == "1532_13")
        {
            if(galley == "1532_13" || galley == "1532_2")
                return true;
        }
        else if(probe == "1532_14")
        {
            if(galley == "1532_14" || galley == "1532_3")
                return true;
        }
        else if(probe == "1533_1")
        {
            if(galley == "1533_1")
                return true;
        }
        else if(probe == "1533_2")
        {
            if(galley == "1533_6" || galley == "1533_3" || galley == "1533_2")
                return true;
        }
        else if(probe == "1533_3")
        {
            if(galley == "1533_6" || galley == "1533_3" || galley == "1533_2")
                return true;
        }
        else if(probe == "1533_4")
        {
            if(galley == "1533_4")
                return true;
        }
        else if(probe == "1533_5")
        {
            if(galley == "1533_5")
                return true;
        }
        else if(probe == "1533_6")
        {
            if(galley == "1533_6" || galley == "1533_3" || galley == "1533_2")
                return true;
        }
        else if(probe == "Coke Label NIR 200")
        {
            if(galley == "Coke Label NIR 200" || galley == "Coke Label NIR 250" 
            || galley == "Coke Label NIR 300")
                return true;
        }
        else if(probe == "Coke Label NIR 250")
        {
            if(galley == "Coke Label NIR 200" || galley == "Coke Label NIR 250" 
            || galley == "Coke Label NIR 300")
                return true;
        }
        else if(probe == "Coke Label NIR 300")
        {
            if(galley == "Coke Label NIR 200" || galley == "Coke Label NIR 250" 
            || galley == "Coke Label NIR 300")
                return true;
        }
    }
    else if(database == "-MOLF")
    {
        string probeSub = probe.substr(0, probe.find("_"));
        string probeFinger = probe.substr(probe.rfind("_") + 1);
        string galleySub = galley.substr(0, galley.find("_"));
        string galleyFinger = galley.substr(galley.rfind("_") + 1);

        if(probeSub == galleySub && probeFinger == galleyFinger)
        {
            return true;
        }
    }
    return false; 
}


/**************************************************************************//**
* @author Dennis Kovarik
*
* @par Description:
* This function opens a file with a given filename passed into the function
*
* @param[in] filename - String of the filename for the file to open
* @param[in,out] fin - Ifstream object for the file to open
*
* @returns true if the file was successfully opened
* @returns false otherwise
*
******************************************************************************/
bool openFile(ifstream &fin, string filename)
{
    fin.open(filename.c_str());

    if(!fin.is_open())
    {
        cout << "Could not open file reader" << endl;
        return false;
    }

    return true;
}


/**************************************************************************//**
* @author Dennis Kovarik
*
* @par Description:
* This function will read the file and compile the matches.
*
* @param[in,out] - matches - Vector of vector of strings to hold the matches 
*                            indicated in the files.
* @param[in] fin - Ifstream object for the file to open
*
* @returns true if the file was successfully read
* @returns false otherwise
*
******************************************************************************/
void readFile(vector<string> &list, ifstream &fin)
{
    string line;
    size_t startpos;
    size_t endpos;
    size_t len;
    string fileID, path, img;
    vector<string> row;

    while(getline(fin, path))
    {
        startpos = path.rfind("/") + 1;
        endpos = path.rfind(".");
        len = endpos - startpos;
        img = path.substr(startpos, len);
        list.push_back(img);
    }
}


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
    string probeFilename, galleryFilename, database;
    vector<string> probeFingerprints, galleryFingerprints;
    int numMatches = 0;

    if(argc != 4)
    {
        cout << "Invalid number of command line arguments" << endl;
        cout << "Usage:" << endl;
        cout << "\t./countMatches -MOLF probeDataset.lis galleryDataset.lis" << endl;
        cout << "\t./countMatches -Nanoparticles probeDataset.lis galleryDataset.lis" << endl;
        return 1;
    }

    database = argv[1];
    probeFilename = argv[2];
    galleryFilename = argv[3];
    
    if(!(database == "-MOLF" || database == "-Nanoparticles"))
    {
        cout << "Invalid database" << endl;
        cout << "Usage:" << endl;
        cout << "\t./countMatches -MOLF probeDataset.lis galleryDataset.lis" << endl;
        cout << "\t./countMatches -Nanoparticles probeDataset.lis galleryDataset.lis" << endl;
        return 1;
    }

    if(!openFile(fin, probeFilename))
    {
        return 1;
    }

    readFile(probeFingerprints, fin);

    fin.close();

    if(!openFile(fin, galleryFilename))
    {
        return 1;
    }

    readFile(galleryFingerprints, fin);

    fin.close();



    for(int i = 0; i < probeFingerprints.size(); i++)
    {
        for(int j = 0; j < galleryFingerprints.size(); j++)
        {
            if(isMatch(probeFingerprints[i], galleryFingerprints[j], database))
            {
                numMatches++;
            }
        }
    }

    cout << "There are a total of " << numMatches << " correct matches!" << endl;

    return 0;
}
