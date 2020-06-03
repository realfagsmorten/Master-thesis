"""
Created on Mon Apr 27 14:00:31 2020

@author: Morten Dramstad

This file converts VOC XML annotation files into YOLO TXT annotation files for use by
the annotation application LabelImg. 

Example XML file:

<annotation>
	<folder>test</folder>
	<filename>clog_6_11_03_2020_23_00_02_Pi1_conv.jpg</filename>
	<path>C:\clog\trainingSet_3\test\clog_6_11_03_2020_23_00_02_Pi1_conv.jpg</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>1024</width>
		<height>1024</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name>Pallet_stacked</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>224</xmin>
			<ymin>104</ymin>
			<xmax>712</xmax>
			<ymax>837</ymax>
		</bndbox>
	</object>
</annotation> 

Example claases.txt, with indices added in front of each class:

0 Pallet_uni_foil
1 Pallet_mix_foil
2 Pallet_no_foil
3 Pallet_part_foil
4 Pallet_stacked
5 Pallet_box

  <----- XML-width ----->        
  _______________________
 |
 |    (x,y) XML upper left corner 
 |      ___________
 |     |           |
 |     |   YOLO    |   The YOLO TXT file (x,y) coordinates are in the middle
 |     1   (x,y)   |   of the rectangle around the object. The frame width   
 |     |           |   and height are then half on each side of the (x,y)
 |     |___________|
 |                (x,y) XML lower right corner
 |_______________________
"""


import xml.etree.ElementTree as ET
import os
import sys

def main(argument):
  
  #print(argument) 
  print("# of Arguments=" + str(len(argument)))
  if len(argument) < 1:
      print("Use \'Folder\' as argument")      
  elif len(argument) > 1:
      print("Too many arguments")
      return
  os.chdir((str(argument[0])))

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
  
  # Picks all the file names in the folder, one by one
  for xmlFileName in os.listdir(os.getcwd()):          
      #tekst = ""                                      # Not necessary ????
      # If the file is an xml-file, then go further with it
      if (xmlFileName.endswith(".xml")):               
          tree = ET.parse(xmlFileName)                 # Opens the xml-file
          
          # Get the root of the file, this is <annotation> (see xml example in the header)
          root = tree.getroot()                        
          
          # Capture all the values needed
          # The width of the picture, example shows 1024 px
          img_width = int(root[4][0].text)             
          # The height of the picture, example shows 1024 px
          img_height = int(root[4][1].text)            
  
          # Find the class code, which is the index of the class. Example class is Pallet_stacked, code 4
          code = classDict[root[6][0].text]            
          x_min = int(root[6][4][0].text)        # x and y coordinates, upper left corner
          y_min = int(root[6][4][1].text)            
          x_max = int(root[6][4][2].text)        # x and y coordinates, lower right corner
          y_max = int(root[6][4][3].text)
  
          #xmlFileName should never be closed?
  
          # Calculate the YOLO values (see illustration in header)
          middle_x = (x_min + x_max)/(2 * img_width)   
          middle_y = (y_min + y_max)/(2 * img_height)
          frame_width = (x_max - x_min) / img_width
          frame_height = (y_max - y_min) / img_height
  
          # Make a string to be written to the TXT file and show this on the display
          tekst = "{0} {1:0.6} {2:0.6} {3:0.6} {4:0.6}".format(code, middle_x, middle_y, frame_width, frame_height)
          print(tekst)                                
             
          # Use the same filename as for the XML file, but change extension to TXT. Display file name.   
          outFileName, ext = os.path.splitext(xmlFileName)  
          outFileName += '.txt'
          print(outFileName)
  
          # Make the new file and write the text into it
          with open(outFileName, "w") as outFile:
              outFile.write(tekst)
              outFile.close()
  
if __name__ == "__main__":
  main(sys.argv[1:])  
  
       