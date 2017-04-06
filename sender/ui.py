## interact with UI to send signals to actuators
from Tkinter import *
import socket, time

class App:

    ##################################################################
    # MOUSE / BUTTON EVENTS
    ##################################################################

    def leftClick(self, event):
        if event.x > 360 and event.y > 380 and event.y < 420:
            self.printArr()
        elif event.x < 750 and event.x > 675:
            if event.y < 130 and event.y > 100:
                self.runPreset(1, 0)
            elif event.y < 180 and event.y > 150:
                self.runPreset(2, 0)
            elif event.y < 230 and event.y > 200:
                self.runPreset(3, 0)
        else:
            node = self.findNode(event.x, event.y)

            if node == None:
                return
            elif node < 2:
                self.thumb_f[node] += 1
                self.thumb_f[node] %= 4
            elif node < 14:
                r = (node - 2) / 3
                c = (node - 2) % 3
                self.fingers_f[r][c] += 1
                self.fingers_f[r][c] %= 4
            elif node < 20:
                r = (node - 14) / 3
                c = (node - 14) % 3
                self.palm_f[r][c] += 1
                self.palm_f[r][c] %= 4
            elif node < 22:
                self.thumb_b[node-20] += 1
                self.thumb_b[node-20] %= 4
            elif node < 34:
                r = (node - 22) / 3
                c = (node - 22) % 3
                self.fingers_b[r][c] += 1
                self.fingers_b[r][c] %= 4
            elif node < 40:
                r = (node - 34) / 3
                c = (node - 34) % 3
                self.palm_b[r][c] += 1
                self.palm_b[r][c] %= 4

            self.redraw()

    def printArr(self):
        print self.array

    def findNode(self, x, y):
        for key in self.map:
            v = self.map[key]
            if x < v[2] and x > v[0] and y < v[3] and y > v[1]:
                return key
        return None

    def constructDict(self):
        self.dict = dict()
        self.dict['A'] = self.thumb_f + self.fingers_f[0]
        self.dict['B'] = self.fingers_f[1] + self.fingers_f[2][:2]
        self.dict['C'] = self.fingers_f[2][2:] + self.fingers_f[3] + self.palm_f[0][:1]
        self.dict['D'] = self.palm_f[0][1:] + self.palm_f[1]
        self.dict['E'] = self.thumb_b + self.fingers_b[0]
        self.dict['F'] = self.fingers_b[1] + self.fingers_b[2][:2]
        self.dict['G'] = self.fingers_b[2][2:] + self.fingers_b[3] + self.palm_b[0][:1]
        self.dict['H'] = self.palm_b[0][1:] + self.palm_b[1]

    def send(self):
        UDP_IP = "128.237.195.168" #receiver's IP
        UDP_Port = 5005
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.constructDict()
        # print 'Sending (100ms): '+str(self.dict)
        sock.sendto(str(self.dict), (UDP_IP, UDP_Port))

    ##################################################################
    # MAIN
    ##################################################################

    def runPreset(self, n, i):
        preset = self.preset[n-1]

        if i >= len(preset):
            return

        self.array = preset[i]
        self.redraw()
        self.canvas.after(1000, self.runPreset, n, i+1)

    def init(self):
        self.preset = [
        
        ]

        self.grid_size = 30
        self.fingers_f = [[0,0,0] for i in xrange(4)]
        self.thumb_f = [0,0]
        self.palm_f = [[0,0,0] for i in xrange(2)]
        self.fingers_b = [[0,0,0] for i in xrange(4)]
        self.thumb_b = [0,0]
        self.palm_b = [[0,0,0] for i in xrange(2)]
        self.map = dict()

        self.canvas = Canvas(self.root, width=800, height=450, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack()
        
        self.redraw()

	self.timerFiredWrapper()

    def timerFired(self):
	   self.send()

    def timerFiredWrapper(self):
    	self.timerFired()
    	delay = 100 # ms
    	self.canvas.after(delay, self.timerFiredWrapper)

    def drawUI(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(-5,-5,805,455,fill='light gray')

        self.canvas.create_rectangle(5,5,25,25,fill='firebrick2')
        self.canvas.create_rectangle(5,35,25,55,fill='green2')
        self.canvas.create_rectangle(5,65,25,85,fill='green3')
        self.canvas.create_rectangle(5,95,25,115,fill='green4')

        self.canvas.create_text(30,15, anchor=W, text='Off')
        self.canvas.create_text(30,45, anchor=W, text='Low')
        self.canvas.create_text(30,75, anchor=W, text='Medium')
        self.canvas.create_text(30,105, anchor=W, text='High')

        self.canvas.create_rectangle(675, 100, 750, 130, fill='slate gray')
        self.canvas.create_rectangle(675, 150, 750, 180, fill='slate gray')
        self.canvas.create_rectangle(675, 200, 750, 230, fill='slate gray')

        self.canvas.create_text(690, 115, anchor=W, text='Preset 1')
        self.canvas.create_text(690, 165, anchor=W, text='Preset 2')
        self.canvas.create_text(690, 215, anchor=W, text='Preset 3')

        self.canvas.create_text(275, 300, anchor=W, text='Front')
        self.canvas.create_text(475, 300, anchor=W, text='Back')

    def redraw(self):
        self.drawUI() # hide the shit storm

        m = 0

        # FRONT

        for t in xrange(len(self.thumb_f)):
            x1 = 180
            x2 = 180 + self.grid_size
            y1 = 150 + 1.25*self.grid_size * t
            y2 = 150 + 1.25*self.grid_size * (t+1)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.getColor(self.thumb_f[t]))
            self.map[m] = [x1, y1, x2, y2]
            m += 1

        for i in xrange(len(self.fingers_f)):
            for j in xrange(len(self.fingers_f[i])):
                x1 = 220 + self.grid_size * i + 10*i
                x2 = 220 + self.grid_size * (i+1) + 10*i
                y1 = 65 + 1.25*self.grid_size * j
                y2 = 65 + 1.25*self.grid_size * (j+1)
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.getColor(self.fingers_f[i][j]))
                self.map[m] = [x1, y1, x2, y2]
                m += 1
                
        for p in xrange(len(self.palm_f)):
            for p_r in xrange(len(self.palm_f[p])):
                x1 = 220 + 1.65*self.grid_size * p_r
                x2 = 220 + 1.65*self.grid_size * (p_r+1)
                y1 = 190 + 1.65*self.grid_size * p
                y2 = 190 + 1.65*self.grid_size * (p+1)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.getColor(self.palm_f[p][p_r]))
                self.map[m] = [x1, y1, x2, y2]
                m += 1

        # BACK

        for t in xrange(len(self.thumb_f)):
            x1 = 580
            x2 = 580 + self.grid_size
            y1 = 150 + 1.25*self.grid_size * t
            y2 = 150 + 1.25*self.grid_size * (t+1)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.getColor(self.thumb_b[t]))
            self.map[m] = [x1, y1, x2, y2]
            m += 1

        for i in xrange(len(self.fingers_f)):
            for j in xrange(len(self.fingers_f[i])):
                x1 = 421 + self.grid_size * i + 10*i
                x2 = 421 + self.grid_size * (i+1) + 10*i
                y1 = 65 + 1.25*self.grid_size * j
                y2 = 65 + 1.25*self.grid_size * (j+1)
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.getColor(self.fingers_b[i][j]))
                self.map[m] = [x1, y1, x2, y2]
                m += 1
                
        for p in xrange(len(self.palm_f)):
            for p_r in xrange(len(self.palm_f[p])):
                x1 = 421 + 1.65*self.grid_size * p_r
                x2 = 421 + 1.65*self.grid_size * (p_r+1)
                y1 = 190 + 1.65*self.grid_size * p
                y2 = 190 + 1.65*self.grid_size * (p+1)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.getColor(self.palm_b[p][p_r]))
                self.map[m] = [x1, y1, x2, y2]
                m += 1

    def getColor(self, n):
        if n == 0:
            return 'firebrick2'
        elif n == 1:
            return 'green2'
        elif n == 2:
            return 'green3'
        elif n == 3: 
            return 'green4'        


    def run(self):
        self.root = Tk()
        self.root.title("Teletouch")
        self.root.geometry("800x450")
        self.root.resizable(width=0, height=0)

        self.init()
        self.root.bind("<Button-1>", lambda event: self.leftClick(event))
        self.root.mainloop()

def main():
    App().run()

main()
