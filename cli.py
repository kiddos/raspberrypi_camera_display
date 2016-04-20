import picamera
import io
import time
from PIL import Image, ImageTk
import Tkinter
import socket

# server info
cmd_port = 3001
name_port = 3002
data_port = 3003
# host = '140.127.205.169'
host = '192.168.0.109'

timeout = 0.066
display_size = (320, 240)


class Application(Tkinter.Frame):
    def create_widgets(self):
        self.quit_button = Tkinter.Button(self)
        self.quit_button['text'] = 'QUIT'
        self.quit_button['fg'] = 'red'
        self.quit_button['command'] = self.quit
        self.quit_button.pack({'side': 'left'})

        self.name_entry = Tkinter.Entry(self)
        self.name_entry.config(width=20)
        self.name_entry.pack({'side': 'left'})

        self.take_pic = Tkinter.Button(self)
        self.take_pic['text'] = 'Take Picture'
        self.take_pic['command'] = self.take_picture
        self.take_pic.pack({'side': 'left'})

        img = Image.open('black.png')
        img = img.resize(display_size, Image.ANTIALIAS)
        self.init_display = ImageTk.PhotoImage(img)
        self.display = Tkinter.Label(image=self.init_display)
        self.display.pack({'side': 'left'})

    def take_picture(self):
        print 'taking picture'
        self.capture_image()

        name = self.name_entry.get()
        if len(name) > 0:
            print 'sending data...'
            # send command
            cmd_socket.send('take')

            # send name
            print name
            name_socket.send(name)


            self.stream.seek(0)
            image_data = self.stream.getvalue()
            print 'sending image data size: ', len(image_data)

            # sending image size
            data_socket.send(str(len(image_data)))
            # sending data
            data_socket.send(image_data)
            # buf = self.stream.read(512)
            # while len(buf) > 0:
                # data_socket.send(buf)
                # buf = self.stream.read(512)

            print 'data sent.'

    def capture_image(self):
        self.stream = io.BytesIO()

        # capture data
        camera.capture(self.stream, format='jpeg')
        # move to front
        self.stream.seek(0)

        # display image
        img = Image.open(self.stream)
        img = img.resize(display_size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.display.config(image=self.image)
        self.display.image = self.image

    def __init__(self, master=Tkinter.NONE):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.mainloop()


### main ###
# init sockets
data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

data_socket.connect((host, data_port))
cmd_socket.connect((host, cmd_port))
name_socket.connect((host, name_port))
print 'all ports connected'

# start camera
camera = picamera.PiCamera()
camera.preview_fullscreen = False
camera.preview_window = (620, 320, 640, 480)
camera.resolution = (640, 480)
camera.sharpness = 10
camera.contrast = 30
camera.start_preview()

root = Tkinter.Tk()
app = Application(master=root)


root.destroy()

name_socket.close()
cmd_socket.close()
data_socket.close()

camera.stop_preview()
