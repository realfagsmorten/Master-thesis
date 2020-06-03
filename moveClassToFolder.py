"""
Created on Thu May 28 12:45:31 2020

@author: Morten Dramstad


Sort all images and the corresponding annotations by class by making a copy in folders  
named equally as the class names. Class names are read from the file classes.txt. A folder named 
"noCLass" is also created for sorting images that are not classified. Files are copied, not moved!

1) The folder path to the files must be inserted into the string variable "imageFolder"
2) The file classes.txt has to be placed in the same folder as the files to copy.
3) The annotation files, in YOLO-format, must exist and be loacted in the same folder. 

Example of the file name of an image and the corresponding annotation file:
clog_7_12_03_2020_11_21_45_Pi1_conv.jpg
clog_7_12_03_2020_11_21_45_Pi1_conv.txt

The number of objects in each class is counted and printed after the sorting.





"""

#from PIL import Image
import os
import shutil
#import pandas as pd

#image_files = []

imageFolder = "conv"                       # The folder where the files are stored

os.chdir(os.path.join(imageFolder))              # Set the correct path initially
classList = []                             # Make an empty list for the classes 
count = 0                                    # Count number of image classifications


# Loop trough the classes and make one folder for each of them
# Later on, the files will be sorted to thsoe different locations
with open("classes.txt", "r") as classFile:  
    for line in classFile:
        classList.append([line.rstrip("\n"), 0])
        #outFileName = classList +".txt"
        outFolderName = line.rstrip("\n")
        print(outFolderName)
        try:
          os.mkdir(outFolderName)
        except:
          print("Folder exist")
 
 # Just open all the files to clear old content initially            
outFolderName = "noClass"   
classList.append([outFolderName, 0])
try:
  os.mkdir(outFolderName)
except:
  print("Folder exist")

print(classList)

#noClassCnt = 0
"""
for idx, item in enumerate(classList):
    print(str(idx) + '  ' +item+ '\n')
"""


#os.chdir(os.path.join("train"))
for fileNameTxt in os.listdir(os.getcwd()):
    if (fileNameTxt.endswith(".txt")) and (fileNameTxt.split("_")[0] == "clog"):
        txtFile = open(fileNameTxt)
        line = txtFile.readline()
        txtFile.close() 
        
        words = line.split()
        print("\n Classfile #" + str(count)+": "+fileNameTxt)
        print(words)  
        if len(words) == 5:        
          classIdx = int(words[0])
          
          outFolderName = classList[classIdx][0]  # Name of folder
          classList[classIdx][1] += 1                                 # Count this image
          print(str(classList[classIdx][1]) + " items stored in: " + outFolderName )
        
        else:
          #noClassCnt += 1
          classList[len(classList)-1][1] += 1
          outFolderName = "noClass"
          print(str(classList[len(classList)-1][1]) + " items stored in: " + outFolderName )
          
        count += 1 
        
        file, ext = os.path.splitext(fileNameTxt)          # Split filename and extension
        fileNameImg = file + ".jpg"  
        
        print(fileNameTxt, fileNameImg)
        
        shutil.copy2(fileNameImg, outFolderName + "\\" + fileNameImg)
        shutil.copy2(fileNameTxt, outFolderName + "\\" + fileNameTxt)


       
print("Number of txt-files: " + str(count))

for className, count in classList:
    print(className, str(count)) 
            
#if noClassCnt != 0:
#    print("noClassName", str(noClassCnt)) 

