import tkinter as tk
import tkinter.font as tkFont

input_URL = ''
label_gamesList = ''
btn_grabComments = ''


class App:
    def __init__(self, root):
        # setting title
        root.title("Reddit Comment Grabber")
        # setting window size
        width = 551
        height = 223
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        global btn_grabComments
        btn_grabComments = tk.Button(root)
        btn_grabComments["bg"] = "#426eff"
        ft = tkFont.Font(family='Times', size=14)
        btn_grabComments["font"] = ft
        btn_grabComments["fg"] = "#ffffff"
        btn_grabComments["justify"] = "center"
        btn_grabComments["text"] = "Grab\nComments"
        btn_grabComments.place(x=400, y=110, width=101, height=50)
        btn_grabComments["activebackground"] = "#010680"
        btn_grabComments["activeforeground"] = "#ffffff"

        input_URL = tk.Entry(root)
        input_URL["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=14)
        input_URL["font"] = ft
        input_URL["fg"] = "#333333"
        input_URL["justify"] = "center"
        input_URL["text"] = "Entry"
        input_URL.place(x=80, y=60, width=422, height=30)

        label_URL = tk.Label(root)
        ft = tkFont.Font(family='Times', size=20)
        label_URL["font"] = ft
        label_URL["fg"] = "#333333"
        label_URL["justify"] = "center"
        label_URL["text"] = "URL:"
        label_URL.place(x=20, y=60, width=60, height=25)

        label_gamesList = tk.Label(root)
        ft = tkFont.Font(family='Times', size=16)
        label_gamesList["font"] = ft
        label_gamesList["fg"] = "#333333"
        label_gamesList["justify"] = "left"
        label_gamesList["text"] = "Games List:"
        label_gamesList.place(x=60, y=20, width=485, height=30)

        btn_addGamesList = tk.Button(root)
        btn_addGamesList["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=14)
        btn_addGamesList["font"] = ft
        btn_addGamesList["fg"] = "#000000"
        btn_addGamesList["justify"] = "center"
        btn_addGamesList["text"] = "Add\nGames List"
        btn_addGamesList.place(x=80, y=110, width=100, height=45)

        btn_addGamesList["command"] = ''

        chkbx_filterComments = tk.Checkbutton(root)
        ft = tkFont.Font(family='Times', size=14)
        chkbx_filterComments["font"] = ft
        chkbx_filterComments["fg"] = "#333333"
        chkbx_filterComments["justify"] = "left"
        chkbx_filterComments["text"] = "  Filter comments"
        chkbx_filterComments.place(x=190, y=110, width=180, height=30)
        chkbx_filterComments["offvalue"] = "0"
        chkbx_filterComments["onvalue"] = "1"

    def grabComments(self):
        print("command")

    def addGamesList(self):
        print("command")

    def setGetCommentsBtnText(self, text):
        btn_grabComments["text"] = text

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()