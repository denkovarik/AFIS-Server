#include <iostream>
#include <string>
#include <vector>
#include <fstream>

// Function prototypes
bool isMatch(std::vector<std::string> match, std::string database);
bool matchBySameName(std::vector<std::string> match);
bool openFile(std::string filename, std::ifstream &fin);
bool readFile(std::vector<std::vector<std::string>> &matches, std::ifstream &fin);
