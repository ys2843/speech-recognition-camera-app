# Selfie-Camera-with-Speech-Recognition

This project is designed to implement a laptop camera application in python, used to take selfie photos with different choices of filters and operations. Combining both real time audio and video processing, this interactive camera can do zoom in/out, blur and clear, taking photo by listening to users’ voice commands, while all functions can also be realized by buttons on the user interface.

This project is implemented object-oriented and there are four classes in it. Speech recognition, video processing, filter object and GUI are implemented separately as a class. Because the loop of speech recognition and the main loop of Tkinter need to run at the same time, threading is used to achieve it. 

## Getting Started
To run the app, first install all packages by enter `pip install requirements.txt`.

Then go to root directiory and type ```python GUI.py```

## Implementation 

### Speech Recognition
Pocketsphinx website: https://cmusphinx.github.io/
Pocketsphinx API is used to implement speech recognition. When speech module heard a certain word that is in its dictionary, it changes the value of a flag in order to inform video processor to apply a corresponding filter or make an action. To let the machine understands the commands from users, a dictionary is needed to look up which phrase the user is saying. The dictionary is created by uploading a text file containing the commands words to sphinx website. In the future, we will add more words to our dictionary in order to make the program more interactive. But now in our dictionary, the magic words are shown below.

+ ‘BLUR’ --- Blur the photo
+ ‘CLEAR’ --- Clear the photo
+ ‘BIGGER’ --- Zoom in
+ ‘SMALLER’ --- Zoom out
+ ‘DARKER’ --- Make photo darker
+ ‘BRIGHTER’ --- Make photo brighter
+ ‘CHEESE’ --- Take a photo

To achieve speech recognition step by step, we implement the following functions. First we import pocketsphinx library and then initialize a decoder object with a Pyaudio stream. And then we implement the function of decoding by opening the pyaudio input stream from microphone which read one block of length 1024 at a time, and decode the block. After decoding, run the corresponding callback function according to the result.

### Filters
This filter module is cloned from a github repository (https://github.com/vbalnt/filterizer) and modified by ourselves. This code can read ‘.acv’ files, which are sample curve files from Photoshop, as numpy array and apply the filters to image captured from camera. When a filter is applied to the camera, the image displayed on the screen will have a specific color modification.
The filter class read all the ‘acv’ files in the repository and generate the filters. By now, we have 4 filters. In the future, we will add more filters to the project.

### Video Processor
This module is designed to do all the image processing tricks to the input image. In the project, image is captured and read in frame by frame by cv2.VideoCapture function. We do the processing to each input frame and display it on the label on the user interface.
When initializing, video processor creates its own speech recognition instance, for speech recognition module controls the real time processing simultaneously. And then video processor also creates its filter manager instance to read and generate filters for future use. After that, video processor module enters the recursive function show_frame to continuously capture images from camera and do the processing. 
The following functions are implemented in video processor, as shown below.

+ `bright_process(self, img)`
 This function is for brightness control, it reads in an image object, and add or subtract an int number to each of the RGB layer of that image.
+ `filter_process(self, img)`
 This function read an image, and call functions from filter manager to apply filter to the image.
+ `zoom_process(self, img)`
 To do zoom in and zoom out, this function read an image and do crop and down sampling to create the zooming effect. 
+ `show_frame(self)`
 This function calls all processing functions in this class to implement the real time video processing. It read one frame from the camera at a time, flip and resize the frame to fit the window. After applying all the processing on the input image, it display the output to the label on its parent GUI.

### GUI
This class contains the GUI class with callback functions of each buttons, and a main method.
The user interface is implemented using Tkinter. There are 2 parts of the user interface. Left frame contains a label used to display video images and a button to take photo, the right frame contains all the functional buttons including 4 filters, zoom in/out, brightness control, blur/clear and speech enable button used to turn on/off the speech recognition. Initially, speech recognition is turned off.
When initializing, in the constructor a daemon thread is created for speech recognition module, for on one hand speech recognition can run at the same time while Tkinter updates the UI, on the other hand, when click exit button both threads can exit simultaneously. 
The detailed function of each button is shown below.
+  Zoom in/out --- Zoom in/out the image by 1. Max is 5, min is 1.
+ Blur/Clear --- Blur/Clear the image, max level is 5, min is 1
+ Brightness scale --- Control the brightness, levels from -50 to +50. Original level is 0.
+ Filters --- Click once the filter is applied while click twice the filter is removed.
+ Voice Enable --- Enable speech recognition. Initially turned off.
+ Take Picture --- Save the image to local repository. Photo name start from ‘photo_0’.

## Test

### Functional Test

After implementing all the functions of the camera, we test each of the filters and functions. The photos are shown in table 5 with the first one is original without any processing. All the functional requirements are satisfied, but some part of the code could be modified in the future. For example, after applying filter there is a apparently latency of the display of the video.


### Speech Recognition Module Test

Then we test the speech recognition module. The result is the program can understand the command correctly in most cases. But in noisy environment, the performance is not as good as in silent environment.  We will figure out a dynamic threshold which could adapt to different environments for the decoder in the future.
