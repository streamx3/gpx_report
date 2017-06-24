# gpx_report

[Читати Солов'їною](https://github.com/streamx3/gpx_report/blob/master/README_UA.md)

This program can:
- create a .GPX file from a photo folder
- create an HTML report from the .GPX file

#### Dependencies:
- ntpath
- xmltodict
- PIL
- ffmpeg

##### Satisfying dependencies on Linux:
```
sudo -i
apt-get install -y python3 python3-pip ffmpeg
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

##### Common part:
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


