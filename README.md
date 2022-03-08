# openspot-utilities
![image](https://user-images.githubusercontent.com/30327342/157311721-1d177228-47af-4c70-a601-8705c5facc02.png)

Application used by technicians during the installation process of the module. 

# db_upload:

Uploads the bounding box coordinates used by the computer vision application

Takes the yaml file name and the parkinglot name in order to place the appropriate information
in the correct database

Activate Virtual Environment: source venv/bin/activate

Packaging build into exe: ``` pyinstaller --add-data 'assets/*.png:assets' --add-data 'yaml_upload/:yaml_upload' -F gui.py ```

# EXE packages downloaded
- tkinter
- pymongo
- pyyaml
- opencv-python

# Planning Software downloaded libraries
- pykml
