import tkinter


class GUI:
    def __init__(self, accumulator):
        self.accumulator = accumulator

    def generateGUI(self):
        def quit():
            top.quit()

        def generate():
            result.config(state=tkinter.NORMAL)
            result.delete(0.0, tkinter.END)
            try:
                result.insert(0.0, str(bytes(self.accumulator.randomdata(n.get())))[1:])
            except tkinter.TclError as e:
                result.insert(0.0, e)
            except AssertionError as e:
                result.insert(0.0, e)
            result.config(state=tkinter.DISABLED)

        top = tkinter.Tk()
        top.title('Fortuna')
        input = tkinter.Label(top, text='How many bytes random data do you want to generate?')
        input.pack()
        n = tkinter.IntVar()
        size = tkinter.Entry(top, width=20, bg='green', fg='black', textvariable=n)
        size.pack()
        get = tkinter.Button(top, text='Generate random data', command=generate)
        get.pack()
        sv = tkinter.Scrollbar(top, orient=tkinter.VERTICAL)
        result = tkinter.Text(top, width=32, yscrollcommand=sv, wrap=tkinter.CHAR)
        result.config(state=tkinter.DISABLED)
        result.pack()
        quit = tkinter.Button(top, text='Quit', command=quit)
        quit.pack()
        top.mainloop()
