import json
import xlwt
from xlwt import Workbook
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

#--Initialize--
window = Tk()
window.geometry("420x240")
window.title("Reddit Comment Grabber")

#Create a button to open the JSON file
jsonButton = Button(window, text="Select JSON File", command= lambda:open_JSON_file())
#Create a button to open the Games List file
gameListButton = Button(window, text="Select Game List File", command= lambda:open_gameList_file())
gamesListFileName = ""
#Create Games List Input File Label
labelText = tkinter.StringVar()
labelText.set("Games List File:" + gamesListFileName)
gamesListLabel = Label(window, textvariable = labelText)

#Show the UI
gamesListLabel.grid(column=0, columnspan=3, pady=10, padx=10, sticky=W)
gameListButton.grid(column=1, row=1, pady=10, padx=10, sticky=E)
jsonButton.grid(column=1, row=2, pady=10, padx=10, sticky=E)

#TODO: Insert a text field for the URL
#TODO: Make a way to easily ignore specific users' comments
#TODO: Make things prettier
    
def open_gameList_file():
    #Open Game List file
    global gamesListFile
    gamesListFile = open(filedialog.askopenfilename(filetypes=[("Text Documents","*.txt")]))
    if gamesListFile is not None:
        #read_gamesList_file()
        gamesListFileName = gamesListFile.name
        #labelText = "Games List File:" + gamesListFileName
        global gamesListLabel
        labelText.set("Games List File: " + gamesListFileName)
        
        
def read_gamesList_file():
    print()
    #TODO: Read the text file and exclude any comment that does NOT have any game title in the list


def open_JSON_file():
    #Open JSON file
    global jsonFile
    jsonFile = open(filedialog.askopenfilename())
    if jsonFile is not None:
        read_JSON_file()


def read_JSON_file():
    #Create a workbook object
    global wb
    wb = Workbook()

    #Create a sheet in that workbook
    sheet1 = wb.add_sheet('Comments')
    sheet1.write(0, 0, "Random ID")
    sheet1.write(0, 1, "Redditor")
    sheet1.write(0, 2, "Game Requested")
    sheet1.write(0, 3, "Full Comment")
    
    #Returns JSON object as a dictionary
    siteJSON = json.load(jsonFile)

    #Iterate through JSON list
    index = 1
    allComments = siteJSON[1]["data"]["children"] #All comment children

    #Get "data" from each child
    for commentData in allComments:
        try:
            #Get data child
            data = commentData["data"]

            #Get the author of this comment
            author = data["author"]

            #This is an Excel function to have a random number in the cell
            excelRandNum = xlwt.Formula("RAND()")

            #Write the Excel function to the first cell
            sheet1.write(index, 0, excelRandNum)

            #Write the Author of the comment in the next cell
            sheet1.write(index, 1, author)
            #First post doesn't have a comment body

            comment = data["body"]
            #Write the comment in the next cell
            sheet1.write(index, 3, comment)
        except:
            pass
        finally:
            index += 1
            
    #Close the file!
    jsonFile.close()
    save_file()

def save_file():
    print("Saving file")
    #TODO: Show user the file is being read/created
    types = [("Excel Workbook","*.xls")]
    saveFile = asksaveasfile(initialfile = "Untitled.xlsx", filetypes = types,
                defaultextension=".xls")
    wb.save(saveFile.name)

    #TODO: Error handling
    
