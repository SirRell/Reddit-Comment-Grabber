import praw
import xlwt
from xlwt import Workbook
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfilename
from tkinter import messagebox
from RCG_GUI import GUI
import json
import traceback

# TODO: Make a way to easily ignore specific users' comments
# TODO: Make things prettier

def open_gameList_file():
    # Open Game List file
    gamesListFile: str = askopenfilename(filetypes=[("Text Documents", "*.txt")])
    if gamesListFile is not None:
        open(gamesListFile)
        # read_gamesList_file()
        gamesListFileName = gamesListFile

        global gamesListLabel
        app.gameListLabel["text"] = f"Games List File: {gamesListFileName}"


def read_gamesList_file():
    print()
    # TODO: Read the text file and exclude any comment that does NOT have any game title in the list


def ShowLoadingWindow(window):
    label = Label(window, text="PLEASE WAIT\nGetting all of the comments!")
    label.pack(fill='x', padx=50, pady=30)
    window.geometry(app.alignstr)
    window.resizable(width=False, height=False)


def GrabAllCommentsFromURL():
    try:
        loadingWindow = Toplevel()
        ShowLoadingWindow(loadingWindow)
        window.update()

        contestURL = app.uRL_Input.get()
        submission = reddit.submission(url=contestURL)
        submission.comments.replace_more(limit=None)

        global wb
        wb = Workbook()

        # Create a sheet in that workbook
        sheet1 = wb.add_sheet('Comments')
        # Write headers
        sheet1.write(0, 0, "Random ID")
        sheet1.write(0, 1, "Redditor")
        sheet1.write(0, 2, "Game Requested")  # Will be used with filtering comments
        sheet1.write(0, 3, "Full Comment")

        # TODO: Show user the file is being read/created
        for index, comment in enumerate(submission.comments.list(), start = 1):
            # This is an Excel function to have a random number in the cell
            excelRandNum = xlwt.Formula("RAND()")

            # Write the Excel function to the first cell
            sheet1.write(index, 0, excelRandNum)

            author = comment.author.name
            # Write the Author of the comment in the next cell
            sheet1.write(index, 1, author)

            # Write the comment in the next cell
            sheet1.write(index, 3, comment.body)

        loadingWindow.destroy
        window.update()

        save_file()

    except praw.exceptions.InvalidURL as e:
        messagebox.showerror("Error", f"{e} is not a reddit post link!")
    except Exception as e:
        traceback.print_exc()
        print(e)
        loadingWindow.destroy()


def save_file():
    types = [("Excel Workbook", "*.xls")]
    saveFile = asksaveasfile(initialfile="Untitled.xlsx", filetypes=types,
                             defaultextension=".xls")
    wb.save(saveFile.name)

    # TODO: Error handling


if __name__ == "__main__":
    # --Initialize--
    creds = "client credentials.txt"
    with open(creds, 'r') as file:
        credFile = json.load(file)

        # Create a new praw Object
        global reddit
        reddit = praw.Reddit(
            client_id = credFile["client_id"],
            client_secret = credFile["client_secret"],
            password = credFile["password"],  # Optional for viewing public comments
            user_agent = credFile["user_agent"],
            username = credFile["username"],  # Optional for viewing public comments
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

    # Create a new tkinter window object
    window = Tk()
    window.iconbitmap("icon_transparent.ico")

    # Fill the window with the GUI in other script
    app = GUI(window)

    # Set button commands
    app.grabCommentButton["command"] = lambda: GrabAllCommentsFromURL()
    app.addGameListBtn["command"] = lambda: open_gameList_file()

    # Show the window
    window.mainloop()  # Blocks the rest of code from running
