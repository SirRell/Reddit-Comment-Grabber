#### Script code needed to include the icon and client credentials file when the EXE is created. ####
import os
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
################################################################

import praw
import xlwt
from xlwt import Workbook
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfilename
from tkinter import messagebox, font
from RCG_GUI import GUI
import json
import re  # Delimiter separation

# TODO: Make a way to easily ignore specific users' comments
# TODO: Make things prettier

def open_gameList_file():
    try:
        # Open Game List file
        gamesListTitle: str = askopenfilename(filetypes=[("Text Documents", "*.txt")])
        if gamesListTitle != '':
            with(open(gamesListTitle, 'r')) as gamesListFile:
                app.gameListLabel["text"] = f"Games List File: {gamesListTitle}"
                read_gamesList_file(gamesListFile)
            app.chkbx_filterComments.select()

    except FileNotFoundError:
        messagebox.showerror("Error", "The file entered cannot be found!")


gameList = None


def read_gamesList_file(file):
    global gameList
    gameList = []
    splitFile = re.split("\n|,", file.read())
    for text in splitFile:
        if text == "":
            continue
        gameList.append(text.strip())
    gameList = set(gameList)


def ShowLoadingWindow(window):
    myFont = font.Font(family='Times', size=24)
    label = Label(window, text="PLEASE WAIT\nGetting all of the comments!", font=myFont)
    label.pack(fill='both', padx=50, pady=50)
    window.geometry(app.alignstr)
    window.resizable(width=False, height=False)


def GrabAllCommentsFromURL():
    # Check to see if "Filter comments" is checked and there is a file
    if app.filterGamesChckbxVar.get() and gameList is None:
        messagebox.showerror("Error", "Cannot filter comments.\nThere is no game list provided.")
        return

    try:
        loadingWindow = Toplevel()
        ShowLoadingWindow(loadingWindow)
        window.update()

        contestURL = app.uRL_Input.get()
        submission = reddit.submission(url=contestURL)
        submission.comments.replace_more(limit=None)

        # Create global workbook object
        global wb
        wb = Workbook()

        # Create a sheet in that workbook
        sheet1 = wb.add_sheet('Comments')
        # Write headers
        sheet1.write(0, 0, "Random ID")
        sheet1.write(0, 1, "Redditor")
        sheet1.write(0, 2, "Game Requested")  # Will be used with filtering comments
        sheet1.write(0, 3, "Full Comment")
        excelRandNum = xlwt.Formula("RAND()")

        # Moved iterable out of the for loop code-line so it can be altered inside the addComment method
        index = 1
        for comment in submission.comments.list():
            def addComment(game=""):
                nonlocal index

                # This is an Excel function to have a random number in the cell
                # Write the Excel function to the first cell
                sheet1.write(index, 0, excelRandNum)

                author = comment.author.name
                # Write the Author of the comment in the next cell
                sheet1.write(index, 1, author)

                # Write the comment in the next cell
                sheet1.write(index, 3, comment.body)

                if game != "":
                    sheet1.write(index, 2, game)
                    index += 1
                else:
                    index += 1

            if app.filterGamesChckbxVar.get():
                for gameName in gameList:
                    if gameName in comment.body:
                        addComment(gameName)
            else:
                addComment()

        loadingWindow.destroy()
        window.update()

        save_file()
    except ValueError:
        messagebox.showerror("Error", "There is not a reddit post link provided!")
        loadingWindow.destroy()
    except praw.exceptions.InvalidURL as e:
        messagebox.showerror("Error", f"{e} is not a reddit post link!")
        loadingWindow.destroy()
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error has ocurred:\n{e}\nPlease report bug at https://github.com/SirRell/Reddit-Comment-Grabber/issues")
        loadingWindow.destroy()


def save_file():
    types = [("Excel Workbook", "*.xls")]
    try:
        saveFile = asksaveasfile(initialfile="Untitled.xls", filetypes=types,
                                 defaultextension=".xls")
        # Saving global workbook
        wb.save(saveFile.name)
    except AttributeError:
        if messagebox.askyesno("Question", "Are you sure you do NOT want to save the file?") == False:
            save_file()
    except NameError:
        messagebox.askyesno("Question", "Are you sure you do NOT want to save the file?")
    except PermissionError:
        messagebox.showerror("Error", "Cannot save to file. Make sure it is not currently in use and try again.")


if __name__ == "__main__":
    # --Initialize--
    creds = resource_path("client credentials.txt")
    with open(creds, 'r') as credsFile:
        clientCreds = json.load(credsFile)

        # Create a new praw Object
        reddit = praw.Reddit(
            client_id=clientCreds["client_id"],
            client_secret=clientCreds["client_secret"],
            password=clientCreds["password"],
            user_agent=clientCreds["user_agent"],
            username=clientCreds["username"],
        )

        # --- TO GET AUTHORIZATION LINK ---
        # reddit = praw.Reddit(
        #     client_id=credFile["client_id"],
        #     client_secret = credFile["client_secret"],
        #     redirect_uri="http://localhost:8080",
        #     user_agent=credFile["user_agent"],
        # )
        # reddit.read_only = True
        # print(reddit.auth.url(["identity"], "false", "permanent"))
        # -----------------------------------
    # Create a new tkinter window object
    window = Tk()
    window.iconbitmap(resource_path("icon_transparent.ico"))

    # Fill the window with the GUI in other script
    app = GUI(window)

    # Set button commands
    app.grabCommentButton["command"] = lambda: GrabAllCommentsFromURL()
    app.addGameListBtn["command"] = lambda: open_gameList_file()

    # Show the window
    window.mainloop()  # Blocks the rest of code from running
