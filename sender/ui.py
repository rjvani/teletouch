from Tkinter import *


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
        else:
            self.array[row][col] += 1
            self.array[row][col] %= 4
            self.redraw()

    def send(self):
        print self.array

    ##################################################################
    # MAIN
    ##################################################################

    def init(self):
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