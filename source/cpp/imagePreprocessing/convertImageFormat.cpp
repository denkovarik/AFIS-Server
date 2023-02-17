// to do: check that input file exists

#include <Magick++.h>
#include <iostream> 
#include <string>

using namespace std; 
using namespace Magick; 

int main(int argc,char **argv) 
{ 
    string inputFilepath, outputFilepath;
    InitializeMagick(*argv);

    // Read command line arguments
    if(argc > 1)
    {
        inputFilepath = argv[1];
    }
    else
    {
        cout << "No input filepath. Quitting..." << endl;
        return 1;
    }

    if(argc > 2)
        outputFilepath = argv[2];
    else 
        outputFilepath = "image.jpg";
    

    // Construct the image object. Seperating image construction from the 
    // the read operation ensures that a failure to read the image file 
    // doesn't render the image object useless. 
    Image image;
    try 
    {
        // Read a file into image object 
        image.read(inputFilepath);

        image.type( GrayscaleType );

        //image.negate();

        // Resize the image
        image.resize("333x500");

        // Write the image to a file 
        image.write(outputFilepath); 
    } 
    catch( Exception &error_ ) 
    { 
        cout << "Caught exception: " << error_.what() << endl; 
        return 1; 
    }
 
    return 0; 
}
