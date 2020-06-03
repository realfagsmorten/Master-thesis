"""
Created on Wed Apr 29 17:47:31 2020

@author: Morten Dramstad

Display the images of a certain class.

Example of use:
python showImagesOfClass.py C:\clog\trainingset_2\train Pallet_unknown

1) Argument 1: path to image folder.  

2) Argument 2: The class file, e.g. "classes.txt".
   NB! The file has to be located in folder of argument 1
   
3) The annotation files, in YOLO-format, must exist and be loacted in the same folder.



"""







#from PIL import Image
import os
#import pandas as pd
import sys
import cv2

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))


def main(argument):
  
  print(argument) 
  print("Len=" + str(len(argument)))
  if len(argument) != 2:
      return
  os.chdir((str(argument[0])))
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
  palletClass = str(argument[1])
  
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
  code = classDict[palletClass]
  

  print("Code: " + str(code))
  
  #return

  #os.chdir(os.path.join("train"))
  for filename in os.listdir(os.getcwd()):
      if (filename.endswith(".txt")) and (filename.split("_")[0] == "clog"):
          inFile = open(filename)
          line = inFile.readline()
          inFile.close()
          words = line.split()
          classIdx = int(words[0])
          if classIdx == code:
            print("\n Classfile #" + str(count)+": "+filename)
            print(words)    
            imgFileName, ext = os.path.splitext(filename)          # Split filename and extension
      
                        
            imgFileName = imgFileName +".jpg"   # Strip away \n
            #classList[classIdx][1] += 1                                 # Count this image
            print(imgFileName)
            image = cv2.imread(imgFileName)
            cv2.imshow(imgFileName, image)
            cv2.waitKey(0)
          
            count += 1
          #open 
  
          """
          with open(outFileName, "a") as outFile:
              outFile.write(filename + "\n")
              outFile.close()
          """
          
  print("Number of txt-files of type " + palletClass + " is: " + str(count))


"""
for className, count in classList:
    print(className, str(count)) 
    outFileName = className +".txt"   
    with open(outFileName, "r+") as outFile:
            lines = outFile.readlines()
            outFile.seek(0)
            outFile.write("No of images in this file: " + str(count)+"\n")
            outFile.writelines(lines)
            outFile.close()

"""



#def main(argv):
  



if __name__ == "__main__":
  main(sys.argv[1:])