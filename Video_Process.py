import cv2
import ImageTk
import Image
import numpy as np
from Filter import *
import os
from Speech_Recognition import *


class VideoProcess:
    global imgf, speech_enable, do_filter, ratio, blur
    parent = None

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.create_filter_manager()
        self.speech_module = SpeechRecognition()
        self.speech_module.parent = self
        self.imgf = None
        self.speech_enable = False
        self.do_filter = 0
        self.ratio = 1
        self.blur = 3

    # create filter management
    def create_filter_manager(self):
        # Filter class initialization
        path = '/Users/shiyang/PycharmProjects/DSP_LAB_Final_project/curves/'
        self.filter_manager = FilterManager()
        # Load filters from .acv file
        for files in os.listdir(path):
            file_path = path + files
            img_filter = Filter(file_path, files)
            self.filter_manager.add_filter(img_filter)

    # Brightness control function
    def bright_process(self, img):
        ratio = self.parent.gain.get()
        if ratio > 0:
            img[:, :, 0] = np.where((255 - img[:, :, 0]) < ratio, 255, img[:, :, 0] + ratio)
            img[:, :, 1] = np.where((255 - img[:, :, 1]) < ratio, 255, img[:, :, 1] + ratio)
            img[:, :, 2] = np.where((255 - img[:, :, 2]) < ratio, 255, img[:, :, 2] + ratio)
        elif ratio < 0:
            img[:, :, 0] = np.where((img[:, :, 0] + ratio) < 0, 0, img[:, :, 0] + ratio)
            img[:, :, 1] = np.where((img[:, :, 1] + ratio) < 0, 0, img[:, :, 1] + ratio)
            img[:, :, 2] = np.where((img[:, :, 2] + ratio) < 0, 0, img[:, :, 2] + ratio)
        return img

    # Add filter function
    def filter_process(self, img):
        global do_filter
        image_array = np.array(img)
        if self.do_filter == 1:
            return Image.fromarray(self.filter_manager.apply_filter('country.acv', image_array))
        elif self.do_filter == 2:
            return Image.fromarray(self.filter_manager.apply_filter('desert.acv', image_array))
        elif self.do_filter == 3:
            return Image.fromarray(self.filter_manager.apply_filter('lumo.acv', image_array))
        elif self.do_filter == 4:
            return Image.fromarray(self.filter_manager.apply_filter('nashville.acv', image_array))
        return img

    # Zoom function
    def zoom_process(self, img):
        w = int(1024 * self.ratio)
        h = int(576 * self.ratio)
        dimension = (w, h)
        img_r = cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)
        new_y = h / 2 - 288
        new_x = w / 2 - 512
        img_c = cv2.blur(img_r, (self.blur, self.blur))
        img_c = Image.fromarray(img_c)
        img_c = img_c.crop((new_x, new_y, new_x + 1024, new_y + 576))
        return img_c

    # Recursive run video capture
    def show_frame(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (1024, 576))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.speech_module.do_speech_rec()
        cv2image_b = self.bright_process(cv2image)
        img = self.zoom_process(cv2image_b)
        self.img_f = self.filter_process(img)
        imgtk = ImageTk.PhotoImage(image=self.img_f)
        self.parent.get_video().imgtk = imgtk
        self.parent.get_video().configure(image=imgtk)
        self.parent.get_video().after(15, self.show_frame)
