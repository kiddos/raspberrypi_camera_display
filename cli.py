import picamera
import io
import time
from PIL import Image, ImageTk
import Tkinter
import socket

#sock = socket.socket()
#host = '140.127.205.169'
#port = 3001
#sock.connect((host, port))
#print 'connected'
#sock.close()

timeout = 0.066
display_size = (320, 240)

class Application(Tkinter.Frame):
    def create_widgets(self):
        self.quit = Tkinter.Button(self)
        self.quit['text'] = 'QUIT'
        self.quit['fg'] = 'red'
        self.quit['command'] = self.quit
        self.quit.pack({'side': 'left'})

        img = Image.open('black.png')
        img = img.resize(display_size, Image.ANTIALIAS)
        self.init_display = ImageTk.PhotoImage(img)
        self.display = Tkinter.Label(image=self.init_display)
        self.display.pack({'side': 'left'})

    def update_display(self):
        with picamera.PiCamera() as camera:
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg')

            stream.seek(0)
            #sock.sendall(image_data)
            img = Image.open(stream)
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

root = Tkinter.Tk()
app = Application(master=root)

root.destroy()

