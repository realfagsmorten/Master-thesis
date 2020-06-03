"""
Created on Tue Apr 20 10:45:31 2020

@author: Morten Dramstad

NB! clog_6 and clog_24 are examples used in the workflow below, change these terms
    in the code as required.
    
    Images are stored on hard-disk D:\clog\, folder names clog_1 to 
    clog_24 and file names starting accordingly, clog_1 to clog_24.
    
    Location 1: clog_1 to clog_7
    Location 2: clog_8 to clog_24    
    
    Example file name:
    clog_7_12_03_2020_11_21_45_Pi1.jpg
	
	This script has to be placed in the same folder as the files to be converted.

1) Find the location of the image first by recognizing the file names.
   - clog_1 is the first part of the filname at location 1 and 2.
     - If the same filename ending is Pi1, the this is Camera 1 at Location 1.
     - Ending Pi2 is Camera 2 at Location 1.
   - clog_24 is the first part of the filename at location 2.
     - It is only one camera at this location.   

2) Crop the image of pallets from size 3280 x 2464 pixels into 2464 x 2464 pixels.
   The (x, y) start coordinates are set individually for the three locations.
   
3) Resize the image to 1024 x 1024 pixels.


Before resizing all images in a folder:
4) Make a test folder, with one sample image of each of the three types.
5) Adjust the coordinates in the code. 
6) Test the shape of the result files. Those files have the ending "_conv" at the 
   end of the file name (example):
   clog_7_12_03_2020_11_21_45_Pi1_conv.jpg
7) Redo 5) and 6) until OK.




"""

# Image size: 3280 x 2464

from PIL import Image                # For image handling, use the Pillow library
import glob, os                      # For file and folder handling

size = 1024, 1024                    # Target size for the images


# Loop trough all the JPG-files of the current folder 
for infile in glob.glob("./*.jpg"):  
    
    # Get the size of the original file and print it
    sizeOfFile = os.path.getsize(infile)    
    print("Size: " + str(sizeOfFile)) 
    
    # In case some images are empty, print the text "Small" and remove the file   
    if sizeOfFile < 100:
      print("Small")   
      relPath = os.path.relpath(infile)    
      os.remove(relPath)      
    
    # For all other images, do the processing described in the header
    else:
      file, ext = os.path.splitext(infile)          # Split filename and extension
      
      # Find the number next to clog and chose location. Then set (x, y). 
      fileNameSplit = file.split('_')                     
      if  fileNameSplit[1] == '24':                 # Location 3 
        xCorner = 570
        yCorner = 0
        
      elif fileNameSplit[1] == '1':                 
        if fileNameSplit[8] == 'Pi1':               # Location 1
          # 328 / 2 = 1640, 1640 + 300 = 1940
          xCorner = 300
          yCorner = 0
        elif fileNameSplit[8] == 'Pi2':             # Location 2
          xCorner = 700
          yCorner = 0
            
      # Open the image, print the original size, crop as specified      
      img1 = Image.open(infile)                     
      width, height = img1.size                     
      print("W: " + str(width) + " H: " + str(height))
      
      area = (xCorner, yCorner, xCorner+2464, yCorner+2464)   # (left upper, right lower)    
      img1 = img1.crop(area)                                                 
      img1.thumbnail(size)
      img1.save(file + "_conv.jpg", "JPEG")