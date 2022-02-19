import json
import xlwt
from xlwt import Workbook
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

window = Tk()
window.geometry("750x250")

#Create a button
btn = Button(window, text="Select JSON File", command= lambda:open_file())

#Show the button
btn.pack(pady=10)

def open_file():
    #Open JSON file
    global file
    file = open(filedialog.askopenfilename())
    if file is not None:
        read_file()
        


def read_file():
    #Create a workbook object
    global wb
    wb = Workbook()

    #Create a sheet in that workbook
    sheet1 = wb.add_sheet('Comments')
    sheet1.write(0, 0, "Random ID")
    sheet1.write(0, 1, "Redditor")
    sheet1.write(0, 2, "Comment")
    print("Wrote headers")
    #Returns JSON object as a dictionary
    siteJSON = json.load(file)

    #Iterate through JSON list
    index = 1
    for siteData in range(len(siteJSON)):
        dataChildren = siteJSON[siteData]["data"]["children"]
        
        for commentData in dataChildren:
            print("Index number: ", index);
            #Get data child
            data = commentData["data"]
            #Get the author of this comment
            author = data["author"]
            #This is an Excel function to have a random number in the cell
            excelRandNum = xlwt.Formula("RAND()")
            #Write the Excel function to the first cell
            sheet1.write(index, 0, excelRandNum)
            print("Wrote random num")
            #Write the Author of the comment in the next cell
            sheet1.write(index, 1, author)
            print("Wrote Author: ", author)
            #First post doesn't have a comment body
            try:
                print("Trying to write comment")
                comment = data["body"]
                #Write the comment in the next cell
                sheet1.write(index, 2, comment)
                print("Wrote comment")
            except:
                pass
            finally:
                print("index is incrimented")
                index += 1
            
    #Close the file!
    file.close()
    save_file()

def save_file():
    print("Saving file")
    types = [("Excel Workbook","*.xls")]
    saveFile = asksaveasfile(initialfile = "Untitled.xlsx", filetypes = types,
                defaultextension=".xls")
    wb.save(saveFile.name)
    print("File, ", saveFile.name, " saved!")
