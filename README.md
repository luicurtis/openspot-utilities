# openspot-utilities

Repository used by technicians during the installation process of the module. 

# db_upload:

Uploads the bounding box coordinates used by the computer vision application

Takes the yaml file name and the parkinglot name in order to place the appropriate information
in the correct database

Activate Virtual Environment: source venv/bin/activate

Packaging into exe: ``` pyinstaller --add-data 'assets/*.png:assets' --add-data 'yaml_upload/:yaml_upload' -F gui.py ```

# packages downloaded
- tkinter
- pymongo
- pyyaml
- opencv-python