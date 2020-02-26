import Tkinter as Tk
from Video_Process import *
from threading import Thread


class GUI:
    def __init__(self):
        # Main windows of the app
        self.root = Tk.Tk()
        self.root.title("Selfie Camera")
        self.root.geometry("1156x620")
        self.video_processor = VideoProcess()
        self.video_processor.parent = self
        self.create_left_frame()
        self.create_right_frame()
        # Output photo count
        self.photo_count = 0
        self.root.mainloop()

    # Left video frame initialization
    def create_left_frame(self):
        # Left panel of photo and snap button
        frame_left = Tk.Frame(self.root)
        # Label to display the graphic from carema
        self.video = Tk.Label(frame_left, width=1024, height=576)
        # Start the speech recognition and video thread separately
        camera_module = Thread(target=self.video_processor.show_frame)
        speech_module = Thread(target=self.video_processor.speech_module.speech_rec)
        camera_module.start()
        # Set speech recognition thread to daemon so that exit callback can work
        speech_module.daemon = True
        speech_module.start()
        self.video.pack()
        # Take picture button
        Tk.Button(frame_left, text='TAKE PICTURE', command=self.snap_call).pack(ipady=10, ipadx=465, expand=True)
        frame_left.pack(side=Tk.LEFT, fill=Tk.BOTH)

    # Right function frame initialization
    def create_right_frame(self):
        # Right panel of control functions
        frame_right = Tk.Frame(self.root)
        # Zoom functions button
        Tk.Label(frame_right, text="ZOOM").pack(fill=Tk.X, ipady=10)
        Tk.Button(frame_right, text='+', command=self.zoom1_callback).pack(fill=Tk.X, ipady=10)
        Tk.Button(frame_right, text='-', command=self.zoom2_callback).pack(fill=Tk.X, ipady=10)
        # Blur functions
        Tk.Label(frame_right, text="BLUR").pack(fill=Tk.X, ipady=10)
        Tk.Button(frame_right, text='+', command=self.blur1_callback).pack(fill=Tk.X, ipady=10)
        Tk.Button(frame_right, text='-', command=self.blur2_callback).pack(fill=Tk.X, ipady=10)
        # Brightness control
        self.gain = Tk.IntVar()
        Tk.Label(frame_right, text='BRIGHTNESS').pack(fill=Tk.X, ipady=10)
        Tk.Scale(frame_right, orient=Tk.HORIZONTAL, variable=self.gain, from_=-50, to=50).pack(fill=Tk.X)
        # Filter control buttons
        Tk.Button(frame_right, text="Country", command=self.country_callback).pack(fill=Tk.X, ipady=13)
        Tk.Button(frame_right, text="Desert", command=self.desert_callback).pack(fill=Tk.X, ipady=13)
        Tk.Button(frame_right, text="Lumo", command=self.lumo_callback).pack(fill=Tk.X, ipady=13)
        Tk.Button(frame_right, text="Nashville", command=self.nashville_callback).pack(fill=Tk.X, ipady=13)
        # Speech recognition enable
        self.speech_button = Tk.Button(frame_right, text="Voice Enable", command=self.speech_enable_callback)
        self.speech_button.pack(fill=Tk.X, ipady=13)
        # Exit button
        Tk.Button(frame_right, text="Exit", command=self.exit_callback).pack(fill=Tk.X, ipady=13)
        frame_right.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=True)

    # snap button
    def snap_call(self):
        file_name = 'photo_' + str(self.photo_count) + '.jpg'
        self.photo_count = self.photo_count + 1
        img = np.array(self.video_processor.img_f)
        cv2.imwrite(file_name, cv2.cvtColor(img,cv2.COLOR_RGBA2BGRA))

    # Zoom in callback
    def zoom1_callback(self):
        if self.video_processor.ratio < 2:
            self.video_processor.ratio += 0.1

    # Zoom out callback
    def zoom2_callback(self):
        if self.video_processor.ratio > 1:
            self.video_processor.ratio -= 0.1

    # Blur callback
    def blur1_callback(self):
        if self.video_processor.blur < 9:
            self.video_processor.blur += 2

    # Reduce blur callback
    def blur2_callback(self):
        if self.video_processor.blur > 3:
            self.video_processor.blur -= 2

    # Filter callback functions
    def country_callback(self):
        if self.video_processor.do_filter == 1:
            self.video_processor.do_filter = 0
        else:
            self.video_processor.do_filter = 1

    def desert_callback(self):
        if self.video_processor.do_filter == 2:
            self.video_processor.do_filter = 0
        else:
            self.video_processor.do_filter = 2

    def lumo_callback(self):
        if self.video_processor.do_filter == 3:
            self.video_processor.do_filter = 0
        else:
            self.video_processor.do_filter = 3

    def nashville_callback(self):
        if self.video_processor.do_filter == 4:
            self.video_processor.do_filter = 0
        else:
            self.video_processor.do_filter = 4

    # Speech recognition enable callback
    def speech_enable_callback(self):
        self.video_processor.speech_enable = not self.video_processor.speech_enable
        if self.video_processor.speech_enable:
            self.speech_button.config(text="Voice Disable")
        else:
            self.speech_button.config(text="Voice Enable")

    # Exit callback
    def exit_callback(self):
        exit(1)

    def get_video(self):
        return self.video


if __name__ == '__main__':
    Gui = GUI()
