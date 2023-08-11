# Nerf-turret
Nerf Turret is a versatile project that brings the excitement of automated target shooting to life. The turret features two distinctive modes: Manual mode, where you have full control, and Auto mode, which employs advanced object detection to automatically track and engage moving targets. This project combines hardware and software components to create an engaging and interactive experience.

## Modes
1. Manual Mode
In this mode, you are in command! You control the turret's movements and firing manually, giving you precise control over your shooting experience. It's a great way to practice your aiming skills or have fun with friends.

2. Auto Mode
The Auto mode takes Nerf Turret to the next level. Equipped with object detection capabilities, the turret can autonomously identify and track moving targets. This advanced feature adds an element of challenge and excitement as the turret locks onto and eliminates targets with impressive accuracy.

## Getting Started
To set up Nerf Turret on your own system, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies:
- pySerial
- PyQt5
- open-cv
- urllib.request
- numpy
- sys
- os

### You can install them using pip:
- pip install pyserial pyqt5 opencv-python-headless numpy

3. If you encounter an error related to "source = open(source, 'rb')", make sure to parse the filename as mentioned in this Stack Overflow thread.
   https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
4. Connect your Nerf turret hardware to your computer.

### Run the main application script:
- python Nerf_turret.py

## Credits
This project stands on the shoulders of giants. Special thanks to the following:

#### Turret inspiration and hardware setup: https://www.youtube.com/watch?v=3Ma5ZCZVQRs 
#### Object detection implementation: https://www.youtube.com/watch?v=_FNfRtXEbr4
