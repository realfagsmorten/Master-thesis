"""
Created on Tue May 28 21:32 2020

@author: Morten Dramstad

Changes the class and moves the bounding box relatively according to
the programlines at:

          middle_x      = float(words[1])
          middle_y      = float(words[2]) - 0.05
          frame_width   = float(words[3]) #+ 0.05
          frame_height  = float(words[4]) + 0.05
        

Use:
python ChangeClassOfImages.py -c Pallet_part_foil

This script has to be placed in the same folder as the files to convert

1) Argument 1: The class name to be used.
2) The class file "classes.txt" has to be located in the same folder.  
3) The annotation files, in YOLO-format, must exist and be loacted in the same folder.

Example of the file name of an image and the corresponding annotation file:
clog_7_12_03_2020_11_21_45_Pi1_conv.jpg
clog_7_12_03_2020_11_21_45_Pi1_conv.txt

"""



#from PIL import Image
import argparse
import os
#import pandas as pd
import sys
import cv2

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))


#def main(argument):
 
def _main_(args):
  palletClass = args.className
    
  #print(argument) 
  #print("Len=" + str(len(argument)))
  #if len(argument) != 2:
  #    return
  
  #os.chdir((str(argument[0])))
  #print(os.listdir())
  #os.chdir(".")
  #print(os.listdir())

  #return

  #os.chdir(os.path.join("newdir"))
  #os.chdir(sys.argv[1])
  
  #image_files = []
  #os.chdir(os.path.join("test"))              # Set the correct path initially
  imgList = []                             # Make an empty list for the classes 
  count = 0                                    # Count number of image classifications
  
  #palletClass = "Pallet_stacked"
  #palletClass = str(argument[1])
  
  #os.chdir("train")
  
  classDict = {}
  
  # Loop trough the classes and make a dictionary where the class names
  # are the keys and the indices of the class are the values.
  with open("classes.txt", "r") as classFile:  
      # Pick the names, one by one, from each line in classes.txt  
      for idx, line in enumerate(classFile):           
          key = line.rstrip("\n")                      # Use the class name as key
          classDict[key] = idx                         # The index is the value  
        
  classFile.close()
  print(classDict)                                     # Display the dictionary
  
  
  # Find the class code, which is the index of the class. Example class is Pallet_stacked, code 4
  classCode = classDict[palletClass]
  
  print("Class code: " + str(classCode))
  
  #return

  #os.chdir(os.path.join("train"))
  for filename in os.listdir(os.getcwd()):
      if (filename.endswith(".txt")) and (filename.split("_")[0] == "clog"):
          txtFile = open(filename)
          line = txtFile.readline()
          txtFile.close()
          words = line.split()
          
          print("Prevoius classification: " + str(words))  
          
          words[0] = str(classCode)
          
          print('Future classification: ' + ' '.join(words))  
          
          
          middle_x      = float(words[1])
          middle_y      = float(words[2]) - 0.05
          frame_width   = float(words[3]) #+ 0.05
          frame_height  = float(words[4]) + 0.05
        
          
          # Make a string to be written to the TXT file and show this on the display
          tekst = "{0} {1:0.6} {2:0.6} {3:0.6} {4:0.6}".format(classCode, middle_x, middle_y, frame_width, frame_height)
          print(tekst)                                
          
          # Remove old contents
          #with open(filename, "w") as txtFile:
          #  txtFile.close()
          
          with open(filename, "w") as txtFile:
            #lines = txtFile.readlines()
            #outFile.seek(0)
            #txtFile.write(' '.join(words))
            txtFile.write(tekst)
            #txtFile.writelines(lines)
            txtFile.close()
          
 
  #print("Number of txt-files of type " + palletClass + " is: " + str(count))




#def main(argv):
  

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Change the classtype of all images in this folder')
    argparser.add_argument('-c', '--className', required=True, help='Select class by name')    
    #argparser.add_argument('-c', '--className', required=True, help='Select class by name')    
    
    
    args = argparser.parse_args()
    _main_(args)

"""
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
	help="path to file containing image URLs")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())

#if __name__ == "__main__":
#  main(sys.argv[1:])
"""





