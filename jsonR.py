import praw
import xlwt
from xlwt import Workbook
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfilename
import RCG_GUI

# TODO: Make a way to easily ignore specific users' comments
# TODO: Make things prettier

def open_gameList_file():
    # Open Game List file
    gamesListFile: str = askopenfilename(filetypes=[("Text Documents", "*.txt")])
    if gamesListFile is not None:
        open(gamesListFile)
        # read_gamesList_file()
        gamesListFileName = gamesListFile.name

        global gamesListLabel
        app.set("Games List File: " + gamesListFileName)


def read_gamesList_file():
    print()
    # TODO: Read the text file and exclude any comment that does NOT have any game title in the list


def GrabAllCommentsFromURL():
    reddit = praw.Reddit(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        password="PASSWORD", # Optional for viewing public comments
        user_agent="USERAGENT",
        username="USERNAME", # Optional for viewing public comments
    )

    contestURL = ""  # TODO: Find out how to reference the input field's text from RCG_GUI
    submission = reddit.submission(url=contestURL)
    submission.comments.replace_more(limit=None)

    global wb
    wb = Workbook()

    # Create a sheet in that workbook
    sheet1 = wb.add_sheet('Comments')
    # Write headers
    sheet1.write(0, 0, "Random ID")
    sheet1.write(0, 1, "Redditor")
    sheet1.write(0, 2, "Game Requested") # Will be used with filtering comments
    sheet1.write(0, 3, "Full Comment")

    # TODO: Show user the file is being read/created
    index = 1
    for comment in submission.comments.list():
        # This is an Excel function to have a random number in the cell
        excelRandNum = xlwt.Formula("RAND()")

        # Write the Excel function to the first cell
        sheet1.write(index, 0, excelRandNum)

        author = comment.author.name
        # Write the Author of the comment in the next cell
        sheet1.write(index, 1, author)

        # Write the comment in the next cell
        sheet1.write(index, 3, comment.body)

        index += 1
    save_file()


def save_file():
    types = [("Excel Workbook", "*.xls")]
    saveFile = asksaveasfile(initialfile="Untitled.xlsx", filetypes=types,
                             defaultextension=".xls")
    wb.save(saveFile.name)

    # TODO: Error handling



if __name__ == "__main__":
    # --Initialize--
    window = Tk()
    app = RCG_GUI.App(window)

    #Uncomment below method call to use without GUI (after updating contestURL above)
    # GrabAllCommentsFromURL()

    window.mainloop() #Blocks the rest of code from running

