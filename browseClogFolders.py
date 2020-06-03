"""
Created on Mon Apr 13 16:08 2020

@author: Morten Dramstad


Browse the current folder for the next _clog number to use.

Example, there exist folders:

clog_1
clog_2

then next folder to make is:
 
clog_3


"""

from PIL import  Image
import time, os     

def main(): 
  directory = os.listdir("./")  # Folder to search in is the USB-folder where the disk is connected
  
   # Startup checking the last used folder, make the next one
  usbFolderFunc = "clog_0"

  maxValue = 0                              # Set the highest detected folder # to 0
   
  for item in directory:                    # Run trough all the files in the folder1
    indeks = item.find("clog_")             # Search for folders beginning with "clog_"
    if indeks != -1:                        # If some folder is found
      value = item.split('_')               # ... split the name at the underscore
      number = int(value[1])                # ... then the right part is the number
      
      if maxValue <= number:                # Check if the lastest found file is the one with the highest value 
        maxValue = number                   # ... and if it is, update this as the greatest value so far
        usbFolderFunc = "clog_" + str(number+1)# Store the next value, one higher than the one found, as the folder name to create
  
  
  #if newFolder == True:
  #cmd = "mkdir /media/pi/USB/" + usbFolderFunc # Create a new, unique folder with the name that was created
  #os.system(cmd)                               # Execute "cmd"
  
  print("Next folder is '"+usbFolderFunc+"'.")
  
  return usbFolderFunc    
  
if __name__ == "__main__": 
  main() 