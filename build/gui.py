
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


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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

# Label
canvas.create_text(
    215.0,
    237.0,
    anchor="nw",
    text="Parking Lot:",
    fill="#000000",
    font=("Roboto", 64 * -1)
)

# Label
canvas.create_text(
    215.0,
    101.0,
    anchor="nw",
    text="OPENSPOT",
    fill="#000000",
    font=("Roboto", 64 * -1)
)

# Label
canvas.create_text(
    229.0,
    360.0,
    anchor="nw",
    text="Module #:",
    fill="#000000",
    font=("Roboto", 64 * -1)
)

# Label
canvas.create_text(
    215.0,
    483.0,
    anchor="nw",
    text="Picture File:",
    fill="#000000",
    font=("Roboto", 64 * -1)
)

# TODO: Drop down menu for selecting parking lot
pLotSelection = StringVar(window)
pLotSelection.set("Select a Parking Lot") # default value
pLotDropDown = OptionMenu(
    window, 
    pLotSelection, 
    *parkingLots
)
pLotDropDown.pack() # TODO: update with .place() to put it in correct place

# Text Input for Mod Number
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    963.0,
    397.5,
    image=entry_image_1
)
modNum = Entry(
    bd=0,
    bg="#B886EA",
    highlightthickness=0
)
modNum.place(
    x=718.0,
    y=360.0,
    width=490.0,
    height=73.0
)

# Select image file
def open_file():
    file = filedialog.askopenfile(mode='r', filetypes=[('Image File', '*.jpg')])
    if file:
        inputVals['imgPath'] = os.path.abspath(file.name)
        Label(window, text="The File is located at : " + str(inputVals['imgPath']), font=('Aerial 11')).pack()

# Add a Label widget
label = Label(window, text="Click the Button to browse the Files", font=('Georgia 13'))
label.pack(pady=10)

# Create a Button
imgFile = Button(window, text="Browse", command=open_file).pack(pady=20)


def submitForm():
    inputVals['parkingLotName'] = pLotSelection.get()
    inputVals['modNum'] = modNum.get()
    exists = False
    # print(inputVals['parkingLotName'])
    # print(inputVals['modNum'])
    # print(inputVals['imgPath'])

    # error checking
    # invalid parking lot name
    if not inputVals['parkingLotName'] in parkingLots:
        messagebox.showerror("Invalid Parking Lot Selected", "\"%s\" is not a valid parking lot, select one in the drop down menu :)" %inputVals['parkingLotName'])
        return

    # check validity of module number
    try:
        int(inputVals['modNum'])
        if int(inputVals['modNum']) < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Module Number", "ERROR: \"%s\" is not a valid module number\n Please enter a positive integer" %inputVals['modNum'],
                            icon='error')
        return

    # check if module already exists
    if int(inputVals['modNum']) in db.get_mod_ids(inputVals['parkingLotName']):
        print("ustoopid")
        popupAns = messagebox.askokcancel("Warning for Updating Module that Already Exists", 
                                        "!!! WARNING !!! \n \"%s\" is already registered in the database \n Click OK to continue" %inputVals['modNum'],
                                        icon='warning')
        if not popupAns:
            return
        exists = True

    # check if the mod number is greater than the max mod num
    # print(db.get_mod_ids(inputVals['parkingLotName']))
    if int(inputVals['modNum']) > max(db.get_mod_ids(inputVals['parkingLotName']))+1:
        popupAns = messagebox.askokcancel("Unexpected Module Number", 
                                        "!!! WARNING !!! \n \"%s\" Mod ID is greater than what was expected.\n \
                                        \n Expected Val: %s \n\n If you are installing modules out of order click OK to continue" \
                                        %(inputVals['modNum'], max(db.get_mod_ids(inputVals['parkingLotName']))+1),
                                        icon='warning')
        if not popupAns:
            return

    # check if there is a file indicated
    if inputVals['imgPath'] == "":
        messagebox.showerror("No File Selected", "ERROR: No file was selected. \n Please select a .jpg file.")
        return

    # TODO: Call bounding box stuff XD
    DrawBBoxes(inputVals['imgPath'])

    # upload coords to db
    db.upload_bounding_boxes("yaml_upload/coords.yml", inputVals['parkingLotName'], int(inputVals['modNum']), exists)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=submitForm,
    relief="flat"
)
button_1.place(
    x=922.0,
    y=610.0,
    width=286.0,
    height=80.0
)
window.resizable(False, False)

window.mainloop()
