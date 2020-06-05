"""
Created on Fri Jun 05 12:48 2020

@author: Morten Dramstad

Count all image annotation files in folders and subfolders, two levels down. 

Makes a sorted list of all the annotation files and store those in a text 
file named "listOfFilesInFolders.txt". The first line of the file is the count. 

This file must be placed in the same folder as the folders on the top level.

Example of the file name of an image and the corresponding annotation file:
clog_7_12_03_2020_11_21_45_Pi1_conv.jpg
clog_7_12_03_2020_11_21_45_Pi1_conv.txt

Printouts:
The folders are printed initially
Each filename is printed.
The number of objects are counted and printed.

"""







#from PIL import Image
import os
#import pandas as pd

#image_files = []
#os.chdir(os.path.join("conv"))              # Set the correct path initially

fileList = []
folderList = []
fileCnt = 0

folder = os.getcwd()

subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
#subfolders = [ f.name for f in os.scandir(folder) if f.is_dir() ]

# Find all folders in this folder and one level below
for folders in subfolders:
  #print (folders)
  folderList.append(folders)
  subsubfolders = [ f.path for f in os.scandir(folders) if f.is_dir() ]
  for folders2 in subsubfolders:
    folderList.append(folders2)
    #print (folders2)

for item in folderList:
  print(item)

for item in folderList:
  for filename in os.listdir(item):
    if (filename.endswith(".txt")) and (filename.split("_")[0] == "clog"):
      fileList.append(filename)
      print(filename)
      fileCnt += 1
    
fileList.sort()    


for item in fileList:
  print(filename)
   
print("No of filenames in this file: " + str(fileCnt))
   
    
fileName = "listOfFilesInFolders.txt"    
with open(fileName, "w") as outFile:
  outFile.write("No of filenames in this file: " + str(fileCnt)+"\n")
  for item in fileList:    
    outFile.write(item+"\n")
  outFile.close()
    

 



"""

classList = []                             # Make an empty list for the classes 
count = 0                                    # Count number of image classifications

# Loop trough the classes and make one file for each of them
# Later on, these files will contain all the names of the images in this folder
with open("classes.txt", "r") as classFile:  
    for line in classFile:
        classList.append([line.rstrip("\n"), 0])
        #outFileName = classList +".txt"
        outFileName = line.rstrip("\n") +".txt"
        print(outFileName)
        with open(outFileName, "w") as outFile:  # Just open all the files to clear old content initially
            #outFile.write("1")
            outFile.close()        
 
 # Just open all the files to clear old content initially            
outFileName = "noClass.txt"   
with open(outFileName, "w") as outFile:
    #outFile.write("1")
    outFile.close()        
 
classFile.close()
print(classList)

noClassCnt = 0

"""



"""
for idx, item in enumerate(classList):
    print(str(idx) + '  ' +item+ '\n')
"""


"""
#os.chdir(os.path.join("train"))
for filename in os.listdir(os.getcwd()):
    if (filename.endswith(".txt")) and (filename.split("_")[0] == "clog"):
        inFile = open(filename)
        line = inFile.readline()
        
        inFile.close() 
        
        words = line.split()
        print("\n Classfile #" + str(count)+": "+filename)
        print(words)  
        if len(words) == 5:        
          classIdx = int(words[0])
          
          outFileName = classList[classIdx][0] +".txt"   # Strip away \n
          classList[classIdx][1] += 1                                 # Count this image
          print(str(classList[classIdx][1]) + " items stored in: " + outFileName )
        
        else:
          noClassCnt += 1
          outFileName = "noClass.txt"
          print(str(str(noClassCnt) + " items stored in: " + outFileName ))
          
        count += 1 
        

        with open(outFileName, "a") as outFile:
            outFile.write(filename + "\n")
            outFile.close()

print("Number of txt-files: " + str(count))

for className, count in classList:
    print(className, str(count)) 
    outFileName = className +".txt"   
    with open(outFileName, "r+") as outFile:
            lines = outFile.readlines()
            outFile.seek(0)
            outFile.write("No of images in this file: " + str(count)+"\n")
            outFile.writelines(lines)
            outFile.close()
            
if noClassCnt != 0:
    print("noClassName", str(noClassCnt)) 
    outFileName = "noClass.txt"   
    with open(outFileName, "r+") as outFile:
            lines = outFile.readlines()
            outFile.seek(0)
            outFile.write("No of images in this file: " + str(noClassCnt)+"\n")
            outFile.writelines(lines)
            outFile.close()
    

"""