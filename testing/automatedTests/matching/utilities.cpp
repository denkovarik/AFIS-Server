#include "utilities.h"

using namespace std;


bool isMatch(std::vector<std::string> match, std::string match_criteria)
{
    if(match_criteria == "-Nanoparticles")
    {
        if(match[0] == "1532_1")
        {
            if(match[1] == "1532_1" || match[1] == "1532_12")
                return true;
        }
        else if(match[0] == "1532_2")
        {
            if(match[1] == "1532_13" || match[1] == "1532_2")
                return true;
        }
        else if(match[0] == "1532_3")
        {
            if(match[1] == "1532_14" || match[1] == "1532_3")
                return true;
        }
        else if(match[0] == "1532_4")
        {
            if(match[1] == "1532_5" || match[1] == "1532_4")
                return true;
        }
        else if(match[0] == "1532_5")
        {
            if(match[1] == "1532_4" || match[1] == "1532_5")
                return true;
        }
        else if(match[0] == "1532_6")
        {
            if(match[1] == "1532_10" || match[1] == "1532_6")
                return true;
        }
        else if(match[0] == "1532_7")
        {
            if(match[1] == "1532_8" || match[1] == "1532_9" || match[1] == "1532_7")
                return true;
        }
        else if(match[0] == "1532_8")
        {
            if(match[1] == "1532_8" || match[1] == "1532_9" || match[1] == "1532_7")
                return true;
        }
        else if(match[0] == "1532_9")
        {
            if(match[1] == "1532_8" || match[1] == "1532_9" || match[1] == "1532_7")
                return true;
        }
        else if(match[0] == "1532_10")
        {
            if(match[1] == "1532_10" || match[1] == "1532_6")
                return true;
        }
        else if(match[0] == "1532_11")
        {
            if(match[1] == "1532_11")
                return true;
        }
        else if(match[0] == "1532_12")
        {
            if(match[1] == "1532_12" || match[1] == "1532_1")
                return true;
        }
        else if(match[0] == "1532_13")
        {
            if(match[1] == "1532_13" || match[1] == "1532_2")
                return true;
        }
        else if(match[0] == "1532_14")
        {
            if(match[1] == "1532_14" || match[1] == "1532_3")
                return true;
        }
        else if(match[0] == "1533_1")
        {
            if(match[1] == "1533_1")
                return true;
        }
        else if(match[0] == "1533_2")
        {
            if(match[1] == "1533_6" || match[1] == "1533_3" || match[1] == "1533_2")
                return true;
        }
        else if(match[0] == "1533_3")
        {
            if(match[1] == "1533_6" || match[1] == "1533_3" || match[1] == "1533_2")
                return true;
        }
        else if(match[0] == "1533_4")
        {
            if(match[1] == "1533_4")
                return true;
        }
        else if(match[0] == "1533_5")
        {
            if(match[1] == "1533_5")
                return true;
        }
        else if(match[0] == "1533_6")
        {
            if(match[1] == "1533_6" || match[1] == "1533_3" || match[1] == "1533_2")
                return true;
        }
        else if(match[0] == "Coke Label NIR 200")
        {
            if(match[1] == "Coke Label NIR 200" || match[1] == "Coke Label NIR 250" 
            || match[1] == "Coke Label NIR 300")
                return true;
        }
        else if(match[0] == "Coke Label NIR 250")
        {
            if(match[1] == "Coke Label NIR 200" || match[1] == "Coke Label NIR 250" 
            || match[1] == "Coke Label NIR 300")
                return true;
        }
        else if(match[0] == "Coke Label NIR 300")
        {
            if(match[1] == "Coke Label NIR 200" || match[1] == "Coke Label NIR 250" 
            || match[1] == "Coke Label NIR 300")
                return true;
        }
    }
    else if(match_criteria == "-MOLF")
    {
        string probeSub = match[0].substr(0, match[0].find("_"));
        string probeFinger = match[0].substr(match[0].rfind("_") + 1);
        string galleySub = match[1].substr(0, match[1].find("_"));
        string galleyFinger = match[1].substr(match[1].rfind("_") + 1);

        if(probeSub == galleySub && probeFinger == galleyFinger)
        {
            return true;
        }
    }
    else if(match_criteria == "-match_by_same_name")
    {
        return matchBySameName(match);
    }
    

    return false; 
}


/**************************************************************************//**
* @author Dennis Kovarik
*
* @par Description:
* This function determines matching fingerprints by if they have the same name or not.
*
* @param[in] match - Vector of strings contiaining the strings of the potential 
*                    fingerprint matches
*
* @returns true if fingerprints names are the same
* @returns false otherwise
*
******************************************************************************/
bool matchBySameName(std::vector<std::string> match)
{
    if(match[0] == match[1])
        return true;
    cout << match[0] << " -- " << match[1] << endl;
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
bool openFile(string filename, ifstream &fin)
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
bool readFile(vector<vector<string>> &matches, ifstream &fin)
{
    string probe, galley, match;
    int score;
    size_t endpos;
    size_t startpos;
    size_t len;
    vector<string> row;

    while(getline(fin, match))
    {
        startpos = match.find(" ") + 1;
        endpos = match.find(".");
        len = endpos - startpos - 1;
        probe = match.substr(startpos + 1, len);
        startpos = probe.rfind("/") + 1;
        len = probe.length() - startpos;
        probe = probe.substr(startpos, len);

        startpos = match.rfind("/") + 1;
        endpos = match.rfind(".");
        len = endpos - startpos;
        galley = match.substr(startpos, len);

        row.push_back(probe);
        row.push_back(galley);

        matches.push_back(row);

        row.clear();
    }

    return true;
}
