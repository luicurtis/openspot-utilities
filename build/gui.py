
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

import os

from database import database
from bbox import DrawBBoxes
from pathlib import Path
from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, filedialog, messagebox


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
YAML_PATH = OUTPUT_PATH / Path("./yaml_upload")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def relative_to_yaml(path: str) -> Path:
    return YAML_PATH / Path(path)

# Initialize Database and fetch values
db = database()
parkingLots = list(db.get_parking_lot_names())

# Input Values
inputVals = {
    "parkingLotName" : "",
    "modNum": -1,
    "imgPath": ""
}

### Window Configuration for GUI
window = Tk()

window.geometry("1280x720")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

# background
canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    720.0,
    fill="#FFFFFF",
    outline="")

# OpenSpot Logo
openspot_logo = PhotoImage(
    file=relative_to_assets("openspot_logo.png"))
canvas.create_image(
    62, 
    40, 
    image=openspot_logo, 
    anchor=NW)

# Set up software title
canvas.create_text(
    539.0,
    65.0,
    anchor="nw",
    text="Module Set up Software",
    fill="#5A5959",
    font=("Roboto Medium", 58 * -1, 'bold')
)

# Parking Lot Selection Text Label
canvas.create_text(
    126,
    195,
    anchor="nw",
    text="Parking Lot:",
    fill="#5A5A5A",
    font=("Roboto", 52),
    justify=RIGHT,
)

# Module Number Input Text Label
canvas.create_text(
    126,
    285,
    anchor="nw",
    text="Module #:",
    fill="#5A5A5A",
    font=("Roboto", 52),
    justify=RIGHT
)

# Picture File Selection Text Label
canvas.create_text(
    126,
    376,
    anchor="nw",
    text="Picture File:",
    fill="#5A5A5A",
    font=("Roboto", 52),
    justify=RIGHT
)

# Bouding Box Button Text Label
canvas.create_text(
    126,
    467,
    anchor="nw",
    text="Bounding Boxes:",
    fill="#5A5A5A",
    font=("Roboto", 52),
    justify=RIGHT
)

inputBorder = PhotoImage(
    file=relative_to_assets("input_border.png"))

# Drop down menu for selecting parking lot
entry_bg_3 = canvas.create_image(
    856.5,
    229.5,
    image=inputBorder
)
pLotSelection = StringVar(window)
pLotSelection.set("Select a Parking Lot") # default value
pLotDropDown = OptionMenu(
    window, 
    pLotSelection, 
    *parkingLots,
)
pLotDropDown.config(
    direction='flush',
    font=("Roboto", 32),
    justify="center",
    width=585,
    height=67-5,
    bg='white',
    bd=0
)
pLotDropDown.place(
    x=564.0,
    y=195.0+5,
    width=585.0,
    height=67-5
)

def handle_focus_in(_):
    if len(modNum.get()) == 0 or modNum.get() == "Enter the Module Number":
        modNum.delete(0, END)
        modNum.config(fg='black')

def handle_focus_out(_):
    if len(modNum.get()) == 0:
        modNum.delete(0, END)
        modNum.config(fg='grey')
        modNum.insert(0, "Enter the Module Number")

def handle_enter(txt):
    print(modNum.get())
    handle_focus_out('dummy')

# Text Input for Mod Number
moduleNumberBorder = canvas.create_image(
    856.5,
    319.5,
    image=inputBorder
)
modNum = Entry(
    bd=0,
    font=("Roboto", 32),
    justify="center",
    # bg="#000000",
    fg='grey',
    highlightthickness=0
)
modNum.insert(
    0, 
    "Enter the Module Number"
)
modNum.bind("<FocusIn>", handle_focus_in)
modNum.bind("<FocusOut>", handle_focus_out)
modNum.bind("<Return>", handle_enter)
modNum.place(
    x=564.0,
    y=290.0,
    width=585.0,
    height=60.0
)

def open_file():
    file = filedialog.askopenfile(mode='r', filetypes=[('Image File', '*.jpg')])
    if file:
        inputVals['imgPath'] = os.path.abspath(file.name)
        imgFilelabel['text']= "Current File: %s" %(inputVals['imgPath'])
        # Label(window, text="The File is located at : " + str(inputVals['imgPath']), font=('Aerial 11')).pack()

# # Add a Label widget
imgFilelabel = Label(
    window, 
    text="Click Browse to select the reference image", 
    font=("Roboto", 18),
    fg='grey'
)
imgFilelabel.place(
    x=564.0,
    y=376.0+35,
    width=585.0,
    height=25
)
# Select image file
imgSelectionimg = canvas.create_image(
    856.5,
    410.5,
    image=inputBorder
)
imgFilebutton = Button(
    window, 
    text="Browse",
    font=("Roboto", 18),
    justify="center",
    command=open_file,
    bd=0,
    highlightthickness=0,
    borderwidth=0,
)
imgFilebutton.place(
    x=564.0,
    y=376.0+5,
    width=585.0,
    height=25
)

def drawBboxForm():
    inputVals['parkingLotName'] = pLotSelection.get()
    inputVals['modNum'] = modNum.get()
    exists = False
    # print(inputVals['parkingLotName'])
    # print(inputVals['modNum'])
    # print(inputVals['imgPath'])

    # error checking
    # invalid parking lot name
    if not inputVals['parkingLotName'] in parkingLots:
        messagebox.showerror("Invalid Parking Lot Selected", "ERROR:\n \"%s\" is not a valid parking lot.\n Select one from the drop down menu" %inputVals['parkingLotName'])
        return

    # check validity of module number
    try:
        int(inputVals['modNum'])
        if int(inputVals['modNum']) < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Module Number", "ERROR:\n \"%s\" is not a valid module number.\n Please enter a positive integer" %inputVals['modNum'],
                            icon='error')
        return

    # # check if module already exists
    # if int(inputVals['modNum']) in db.get_mod_ids(inputVals['parkingLotName']):
    #     print("ustoopid")
    #     popupAns = messagebox.askokcancel("Warning for Updating Module that Already Exists", 
    #                                     "!!! WARNING !!! \n \"%s\" is already registered in the database \n Click OK to continue" %inputVals['modNum'],
    #                                     icon='warning')
    #     if not popupAns:
    #         return
    #     exists = True

    # check if the mod number is greater than the max mod num
    # print(db.get_mod_ids(inputVals['parkingLotName']))
    if int(inputVals['modNum']) > max(db.get_mod_ids(inputVals['parkingLotName'])):
        messagebox.showerror("Unexpected Module Number", 
                                        "!!! WARNING !!! \n Mod ID \"%s\" is greater than what was expected.\n \
                                        \n Expected Value(s) in the range of: \n %s to %s "\
                                        %(inputVals['modNum'], min(db.get_mod_ids(inputVals['parkingLotName'])), max(db.get_mod_ids(inputVals['parkingLotName']))),
                                        icon='warning')
        return


    # check if there is a file indicated
    if inputVals['imgPath'] == "":
        messagebox.showerror("No File Selected", "ERROR: No file was selected. \n Please select a .jpg file.")
        return

    # TODO: Call bounding box stuff XD
    DrawBBoxes(inputVals['imgPath'])

# Draw BBox button
bboxButtonimg = PhotoImage(
    file=relative_to_assets("draw_bbox_button.png"))
bboxButton = Button(
    image=bboxButtonimg,
    borderwidth=0,
    highlightthickness=0,
    highlightbackground='white',
    command=drawBboxForm,
    relief="flat",
    bd=0
)
bboxButton.place(
    x=539.0,
    y=467.0,
    width=635.0,
    height=69.0
)

def submitForm():
    # send data to database
    # check if yml file exists
    if os.path.isfile(relative_to_yaml("coords.yml")):
        print("submitting form")
        # upload coords to db
        db.upload_bounding_boxes(relative_to_yaml("coords.yml"), inputVals['parkingLotName'], int(inputVals['modNum']))
        os.remove(relative_to_yaml("coords.yml"))
        messagebox.showerror("Submit Successful", "Success!\n Coordinates uploaded to database.",
                    icon='info')
        
    else:
        messagebox.showerror("No coordinates found", "ERROR: No bounding boxes found. \n \n Please click the button 'Draw Bounding Boxes' to create coordinates file",
                            icon='error')
# Submit Button
submitButtonimg = PhotoImage(
    file=relative_to_assets("submit_button.png"))
submitButton = Button(
    image=submitButtonimg,
    borderwidth=0,
    highlightthickness=0,
    command=submitForm,
    relief="flat"
)
submitButton.place(
    x=116.0,
    y=608.0,
    width=1058.0,
    height=60.0
)

window.resizable(False, False)
window.mainloop()
