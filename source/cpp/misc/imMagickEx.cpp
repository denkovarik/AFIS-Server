/*-----------------------------------------------------------------------------
 * File:    imMagickEx.cpp
 *
 * Author: Dennis Kovarik
 * Date: 10/8/2020
 * 
 * Purpose: Example code on how to manipulate images with Image Magick. 
 *
 * Compile  (must be in project root dir):
 *          make imMagickEx
 *   
 * Run (from project root dir):     
 *      ./bin/imMagickEx
 *      ./bin/imMagickEx inIMagePath outimagePath
 *
 *---------------------------------------------------------------------------*/
#include <Magick++.h>
#include <iostream>
#include <string> 

using namespace std; 
using namespace Magick; 


/**************************************************************************//**
* @author Dennis Kovarik
*
* @par Description:
* This is the main function which is the start of the program. It will read the
* command line arguments (if any), and read in the input image. It contains 
* example code for manipulating images using Image Magick. It will then write
* the image to file. 
*
* @param[in] argc - The number of commandl line arguments 
* @param[in] argc - Character array of command line arguments
*
* @returns 0 if the program executed correctly.
******************************************************************************/
int main(int argc,char **argv) 
{
    string imInPath = "testing/images/MOLF/jpg/100_1_1.jpg";
    string imOutPath = "testing/images/MOLF/png/100_1_1.png";
    
    // Read command line arguments
    if(argc == 3) 
    {
        imInPath = argv[1];
        imOutPath = argv[2];
    }
    
//InitializeMagick(*argv);

    // Construct the image object. Seperating image construction from the 
    // the read operation ensures that a failure to read the image file 
    // doesn't render the image object useless. 
    Image image;
    try { 
        // Read a file into image object 
        image.read( imInPath );

        //image.quantizeColorSpace( GRAYColorspace ); 
        //image.quantizeColors( 256 ); 
        //image.quantize( );

        image.type( GrayscaleType );

        // Complement the image
        image.negate();

        // Crop the image to specified size (width, height, xOffset, yOffset)
        //image.crop( Geometry(100,100, 100, 100) );

        image.display();

        // Resize the image
        image.resize("100x100");

        // Write the image to a file 
        image.write( imOutPath ); 
    } 
    catch( Exception &error_ ) 
    { 
      cout << "Caught exception: " << error_.what() << endl; 
      return 1; 
    }
 
    return 0; 
}
