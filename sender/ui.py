## interact with UI to send signals to actuators
from Tkinter import *
import socket, time

class App:

    off = 0
    low = 1
    med = 2
    high = 3

    ##################################################################
    # MOUSE / BUTTON EVENTS
    ##################################################################

    def leftClick(self, event):
        col = (event.x - 180)/80
        row = (event.y - 100)/80

        if row < 0 or row > 2 or col < 0 or col > 2:
            if event.x > 240 and event.x < 360 and event.y > 380 and event.y < 420:
                self.send()
            elif event.x > 360 and event.y > 380 and event.y < 420:
                self.printArr()
            elif event.x < 550 and event.x > 475:
                if event.y < 130 and event.y > 100:
                    self.runPreset(1, 0)
                elif event.y < 180 and event.y > 150:
                    self.runPreset(2, 0)
                elif event.y < 230 and event.y > 200:
                    self.runPreset(3, 0)

        else:
            self.array[row][col] += 1
            self.array[row][col] %= 4
            self.redraw()

    def printArr(self):
        print self.array

    def send(self):
        UDP_IP = "128.237.208.146" #receiver's IP
        UDP_Port = 5005
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        newDict = {'A': self.array[0], 'B': self.array[1], 'C': self.array[2]}
        print 'Sending (1000ms): '+str(newDict)
        sock.sendto(str(newDict), (UDP_IP, UDP_Port))

    ##################################################################
    # MAIN
    ##################################################################

    def runPreset(self, n, i):
        preset = self.preset[n-1]

        if i >= len(preset):
            return

        self.array = preset[i]
        self.redraw()
        self.send()
        self.canvas.after(1000, self.runPreset, n, i+1)

    def init(self):
        self.preset = [
            [[[3, 0, 0], [3, 0, 0], [3, 0, 0]],
            [[0, 3, 0], [0, 3, 0], [0, 3, 0]],
            [[0, 0, 3], [0, 0, 3], [0, 0, 3]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
            [[[0, 0, 0], [0, 0, 0], [1, 0, 0]],
            [[0, 0, 0], [1, 0, 0], [2, 1, 0]],
            [[1, 0, 0], [2, 1, 0], [3, 2, 1]],
            [[2, 1, 0], [3, 2, 1], [2, 3, 2]],
            [[3, 2, 1], [2, 3, 2], [1, 2, 3]],
            [[2, 3, 2], [1, 2, 3], [0, 1, 2]],
            [[1, 2, 3], [0, 1, 2], [0, 0, 1]],
            [[0, 1, 2], [0, 0, 1], [0, 0, 0]],
            [[0, 0, 1], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
            [[[3, 0, 3], [0, 0, 0], [3, 0, 3]],
            [[0, 0, 0], [0, 3, 0], [0, 0, 0]],
            [[0, 3, 0], [3, 0, 3], [0, 3, 0]],
            [[3, 1, 3], [1, 0, 1], [3, 1, 3]],
            [[1, 1, 1], [1, 3, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
]
        ]

        self.canvas = Canvas(self.root, width=600, height=450, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack()
        self.array = [[0,0,0] for i in xrange(3)]
        self.redraw()

    def redraw(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(-5,-5,605,455,fill='light gray')

        self.canvas.create_rectangle(5,5,25,25,fill='firebrick2')
        self.canvas.create_rectangle(5,35,25,55,fill='green2')
        self.canvas.create_rectangle(5,65,25,85,fill='green3')
        self.canvas.create_rectangle(5,95,25,115,fill='green4')

        self.canvas.create_text(30,15, anchor=W, text='Off')
        self.canvas.create_text(30,45, anchor=W, text='Low')
        self.canvas.create_text(30,75, anchor=W, text='Medium')
        self.canvas.create_text(30,105, anchor=W, text='High')

        self.canvas.create_rectangle(475, 100, 550, 130, fill='slate gray')
        self.canvas.create_rectangle(475, 150, 550, 180, fill='slate gray')
        self.canvas.create_rectangle(475, 200, 550, 230, fill='slate gray')

        self.canvas.create_text(490, 115, anchor=W, text='Preset 1')
        self.canvas.create_text(490, 165, anchor=W, text='Preset 2')
        self.canvas.create_text(490, 215, anchor=W, text='Preset 3')

        self.canvas.create_rectangle(240, 380, 360, 420, fill='blue2')
        self.canvas.create_text(280, 400, anchor=W, text='Send')

        f = ''

        for i in xrange(len(self.array)):
            for j in xrange(len(self.array[i])):
                if self.array[i][j] == 0:
                    f = 'firebrick2'
                elif self.array[i][j] == 1:
                    f = 'green2'
                elif self.array[i][j] == 2:
                    f = 'green3'
                elif self.array[i][j] == 3: 
                    f = 'green4'
                self.canvas.create_rectangle(180+80*j, 100+80*i, 180+80*(j+1), 100+80*(i+1), fill=f)

    def run(self):
        self.root = Tk()
        self.root.title("Teletouch")
        self.root.geometry("600x450")
        self.root.resizable(width=0, height=0)

        self.init()
        self.root.bind("<Button-1>", lambda event: self.leftClick(event))
        self.root.mainloop()

def main():
    App().run()

main()
