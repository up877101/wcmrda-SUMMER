This is the final year project for up877101

The project title is:
    "Wireless Control of a Mobile Robot for Domestic Applications"

the project is structured under 3 seperate folders:

32u4 -      contains the code for the robots microcontroller based on the arduino
            platform, this microcontroller is slaved to the Rpi and controls
            low level sensing and actuation

desktop -   contains the code for a desktop application that is used to
            teleoperate the tobot over a local network

pi -        contains the code for an application that runs on the pi to control 
            the high level operations on the robot

To install the dependencies of this software (excluding opencv) on the pi and 
desktop, run the dependencies.sh file