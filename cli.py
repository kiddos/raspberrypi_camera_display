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
host = '140.127.205.169'

timeout = 0.066
display_size = (320, 240)


class Application(Tkinter.Frame):
    def create_widgets(self):
        self.quit = Tkinter.Button(self)
        self.quit['text'] = 'QUIT'
        self.quit['fg'] = 'red'
        self.quit['command'] = self.quit
        self.quit.pack({'side': 'left'})

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
        name = self.name_entry.get()
        if len(name) > 0:
            print 'sending data...'
            # send command
            cmd_socket.send('take')

            # send name
            print name
            name_socket.send(name)

            # send image data over
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.connect((host, data_port))

            self.stream.seek(0)
            image_data = self.stream.getvalue()
            print 'sending image data size: ', len(image_data)
            data_socket.sendall(image_data)
            data_socket.close()
            print 'data sent.'

    def update_display(self):
        with picamera.PiCamera() as camera:
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

        root.after(66, self.update_display)


    def __init__(self, master=Tkinter.NONE):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.update_display()
        self.mainloop()

cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cmd_socket.connect((host, cmd_port))
name_socket.connect((host, name_port))
print 'connected'

root = Tkinter.Tk()
app = Application(master=root)

root.destroy()
name_socket.close()

