###################################################################################
#  Raspberry Pi CAMERA 1 as standalone at location 2
#######################################################################################
#
#  How it works:
#  1. Camera 1 is connected to a sensor.
#  2. Camera 1 waits for a pallet to be detected by the sensor. 
#  3. When a pallet is detected, camera 1 will wait for the pallet to leave the sensor.
#  4. As soon as the pallet has left the sensor:
#     a. Camera 1 is preparing for shooting the picture by making a filename that 
#        has the format clog_1_11_03_2020_12_56_04_Pi1.jpg.
#     b. Wait 3 seconds to let the pallet be moved into place.  
#  5. Take the picture.
#  6. Store it at the USB-harddisk.
#
#######################################################################################


from gpiozero import Button, LED                # Library for the IO
from picamera import PiCamera                   # Library for using the rPi camera
from time import sleep                          # Library for time operations
import time, os                                 # Library for using command line instructions


# Function for initializing the USB
def init_usb():

  # Startup checking the last used folder, make the next one
  usbFolderFunc = "clog_0"


  maxValue = 0                                # Set the highest detected folder # to 0                 
  try:                                        # try, in case of the USB-harddisk not being present             
    # Folder to search in is the USB-folder where the disk is connected
    directory = os.listdir("/media/pi/USB/")        
                                                    
    for item in directory:                          # Run trough all the files in the folder1
      indeks = item.find("clog_")                   # Search for folders beginning with "clog_"
      if indeks != -1:                              # If some folder is found
        value = item.split('_')                     # ... split the name at the underscore
        number = int(value[1])                      # ... then the right part is the number
                                                   
		# Check if the lastest found file is the one with the highest value 
        if maxValue <= number:
          
		  # ... and if it is, update this as the greatest value so far		
          maxValue = number                         
		  
		  # Store the next value, one higher than the one found, as the folder name to create
          usbFolderFunc = "clog_" + str(number+1)   
                                                    
    # Create a new, unique folder with the name that was created
    cmd = "mkdir /media/pi/USB/" + usbFolderFunc    
    os.system(cmd)                                  # Execute "cmd"
                                                    
    return usbFolderFunc                            # Return the folder name
                                                    
  except:                                           # exception, the harddisk was not found  
    # ... then return the folder name "noUsb" as an indication of just that   
    return "noUsb"     


# main program
sensor = Button(25, pull_up=False,)   # Setup pin 25 as input, pull down
led    = LED(24)                      # Setup pin 24 as output for the LED

usbFolder = init_usb()
#cmd = "touch /home/pi/remove.txt"                # touch will make an empty file
#os.system(cmd)                                   # Execute command touch

camera = PiCamera(resolution=(3280,2464), framerate = 30) # Set camera resolution
camera.iso = 200                                          # For best possible resolution, use low iso setting
sleep(2)                                                  # Wait 2 seconds to let the camera adjust

# Fix the values so that all pictures will get the same focus and light setting
camera.shutter_speed = camera.exposure_speed    # Using the last registered exposure speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

# Forever
while True:
      led.on()                          # Turn the LED on initially and always when idling
      sensor.wait_for_release()         # Pallet is detected by the sensor

      sleep(0.5)                        # Wait half a second
        
      sensor.wait_for_press()           # Pallet leaves the sensor
      led.off()                         # LED off indicates that picture will be shot
    
       
      name = usbFolder + "_" + (time.strftime("%d_%m_%Y_%H_%M_%S")) # Filename is time
      fname = "/home/pi/pic/" + name + "_Pi1" + ".jpg"              # Store in folder pic
          
      # Take the picture
      sleep(3)                                      # Wait 3 seconds to let the pallet be moved into place
      camera.capture(fname)                         # Shoot the picture, that will be stored at location "fname"
      if usbFolder != "noUsb":                                    # Usb is present if this test is successful
        cmd = "mv /home/pi/pic/*.jpg /media/pi/USB/" + usbFolder  # Move all present jpg-files to the hard disk
        rc = os.system(cmd)                                       # Execute command move files
        if rc != 0:                                               # Test if the moving was successful
          usbFolder = init_usb()                                  # ... if not, try to initialize USB 
                  
      else:                                                     # USB was not present
        usbFolder = init_usb()                                  # ... then try to initalize USB-harddisk 