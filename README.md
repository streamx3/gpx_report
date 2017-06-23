# gpx_report
Tool to create GPX files from photos and HTML reports from GPX files


This program can:
- create .GPX file from a photo folder
- create HTML report from the .GPX file

#### Dependencies:
- ntpath
- xmltodict
- PIL
- ffmpeg

##### Satisfying dependencies on Linux:
```
sudo -i
aptitude install -y python3 python3-pip ffmpeg
^D
```

##### Satisfying dependencies on Mac:
- Install Python 3 from official website
```
brew install ffmpeg
```

##### Satisfying dependencies on Windows:
- Install Python 3 from official website
- Install ffmpeg from official website
- add ffmpeg, python3 and pip3 to $PATH

##### Common part
Go to console and:
```
pip3 install ntpath xmltodict pillow
```

### Folder to GPX
Just try:
```
gpx_report -d folder
```

Lazy way:
```
python3 gpx_report.py -d folder
```

Added new photos? Need to overwrite .GPX?
```
python3 gpx_report.py -d folder -f
```

this will create `folder/folder.gpx` file. You can open it with JOSM or any software you like to view photos on map.


### GPX to HTML
Just try:
```
gpx_report -g folder/folder.gpx
```

Lazy way:
```
python3 gpx_report.py -g folder/folder.gpx
```

this will create `folder/index.html` file. You can open it with any browser.
Note, that if you have .GPX with that links to .3gpp audio notes, those notes will be converted to .mp3 and inserted into the page.


