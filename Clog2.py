###################################################################################
#  Raspberry Pi CAMERA 2 used at location 1
#######################################################################################
#
#  How it works:
#  1. Camera 1 is connected to a sensor.
#  2. Camera 1 waits for a pallet to be detected by the sensor. 
#  3. When a pallet is detected, camera 1 will wait for the pallet to leave the sensor.
#  4. As soon as the pallet has left the sensor:
#     a. Camera 1 is preparing for shooting the picture by making a filename that 
#        has the format clog_1_11_03_2020_12_56_04_Pi1.jpg for it's own picture,
#        and one with the format clog_1_11_03_2020_12_56_04_Pi2.jpg for the picture
#        of camera 2.
#     b. Camera 1 stores the filename for camera 2 in the Raspberry Pi 2's folder
#        /home/pi/commands/. Connection is done with camera 2 over Ethernet, using 
#        SSH to get access to camera 2's file system.
#  5. When a jpg-file is detected by camera 2 in /home/pi/commands/, a picture is taken 
#     and then stored in folder /home/pi/pic as a file with the same filename. This will ensure that both the 
#     picture shot by camera 1 and camera 2 will get the same filename except for the 
#     ending 1 or 2.
#  6. As soon as camera 1 has copied the picture from camera 2's disk and stored it in 
#     a safe place, it will command camera 2 to remove the local copy of the picture by 
#     storing the file "remove.txt" in the folder /home/pi/commands/.
#  7. When camera 2 detects the file "remove.txt", both the last shot picture and the 
#     file "remove.txt" are removed.
#
#######################################################################################


from gpiozero import Button, LED                # Library for the IO
from picamera import PiCamera                   # Library for using the rPi camera
from time import sleep                          # Library for time operations
import time, os                                 # Library for using command line instructions
#import subprocess
#button = Button(25, pull_up=False,)            # No button or sensor is used for camera 2
led    = LED(24)                                # Enable LED as output 24

camera = PiCamera(resolution=(3280,2464), framerate = 30) # Set camera resolution
camera.iso = 160                                          # For best possible resolution, use low iso setting
sleep(2)                                                  # Wait 2 seconds to let the camera adjust

# Fix the values so that all pictures will get the same focus and light setting
camera.shutter_speed = camera.exposure_speed      # Using the last registered exposure speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

while True:
    led.on()                                      # Turn the LED on

    fname = ""                                    # No filename initially
    directory = os.listdir("/home/pi/commands/")  # List the contents of the folder "commands"
    for item in directory:                        # Loop trough the files in the folder
      indeks = item.find(".jpg")                  # For each file, search for ".jpg" in the filename
      if indeks != -1:                            # If ".jpg" was found
        fname = item                              # ... store this as the filename for the current picture
      
      indeks = item.find("remove.txt")            # Do also search for the filename "remove.txt"
      if indeks != -1:                            # If found..
        cmd = "rm /home/pi/commands/remove.txt"   # ... this is a message from camera 1 to remove old pictures
        os.system(cmd)                            # ... so do remove the file "remove.txt" first
        cmd = "rm /home/pi/pic/*.jpg"             # ... then remove old pictures ind the pic-folder as well
        os.system(cmd)                            # Just execute the command "cmd"
    
    if fname != "":                               # If a jpg-filename existed in the test above
      cmd = "rm /home/pi/commands/*.jpg"          # ... then first remove the file created by camera 1
      os.system(cmd)                              # Just execute the command "cmd"
    
      led.off()                                   # Turn the LED off, which means that a picture is shot
      fname = "/home/pi/pic/" + fname             # Use "fname" to make the filename for this picture
   
      camera.capture(fname)                       # Shoot the picture, that will be stored at location "fname"  
      