#!/usr/bin/env python3

import os
import sys
import getopt
import ntpath
import xmltodict  # Need to be installed
from PIL import Image # Need to install "pillow"
from PIL.ExifTags import TAGS, GPSTAGS

_usage = 'gpx_report -g track.gpx\ngpx_report -p photo_folder'
opt_force = False
opt_dir = ''
opt_gpx = ''


def errexit(errmsg):
    print('ERROR! ' + errmsg, file=sys.stderr)
    sys.exit(1)


# Stolen: V
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# def rreplace(s, old, new, occurrence):
#     li = s.rsplit(old, occurrence)
#     return new.join(li)


def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    if 36867 in info:
        exif_data['time'] = info[36867]
    return exif_data


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available,
        from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')
        # gps_altitude = _get_if_exist(gps_info, 'GPSAltitude')
        # gps_altitude_ref = _get_if_exist(gps_info, 'GPSAltitudeRef')
        # print(gps_altitude)
        # print(gps_altitude_ref)

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon


# Stolen ^


def process_GPX(filename):
    wpts = []
    dirname = os.path.dirname(filename)

    def makeRow(id, wpt):
        rv = '<tr><td>' + str(id) + '</td><td>' + wpt['lat'] + '</td><td>' + wpt['lon'] + '</td>' + '<td>' + wpt['ele'] + '</td>'
        if wpt['name'] == 'Photo':
            rv += '<td><a href="' + wpt['link'] + '"><img src="' + wpt['link'] + '" height="32"></td></a>'
        else:
            auoname = os.path.join(dirname, wpt['link'])  # Audio Old Name
            aunname = auoname[:-4] + 'mp3'                # Audio New Name
            if not os.path.isfile(auoname):
                errexit('Audio file not found: "' + auoname + '"')
            os.system('ffmpeg -y -i ' + auoname + ' ' + aunname)
            rv += '<td><audio controls><source src="' + wpt['link'][:-4] + \
                  'mp3" type="audio/mpeg">Your browser does not support the audio element.</audio></td>'
        return rv + '</td>'

    if not filename.endswith('.gpx'):
        errexit('File with non-GPX extension given: "' + filename + '"')

    with open(filename, 'r') as pFile:
        od1 = xmltodict.parse(pFile.read())
        print(od1)
        # print()
        if 'gpx' in od1 and 'wpt' in od1['gpx']:
            print('Found some waypoints...')
            for wp in od1['gpx']['wpt']:
                if wp['name'] in ('Voice recording', 'Photo'):
                    wpts.append({'lat': wp['@lat'], 'lon': wp['@lon'], 'ele': wp['ele'],
                                 'name': wp['name'], 'link': wp['link']['text']})
    # print(wpts)
    if len(wpts) < 1:
        print('Looks like there where no suitable waypoints :(')
        sys.exit(0)

    # ofname = filename[:-4] + '.htm'
    ofname = os.path.join(os.path.dirname(filename), 'index.html')
    print('Will try to write index.html ...')
    if os.path.exists(ofname) and os.path.isfile(ofname):
        if opt_force:
            print('Overwriting...')
        else:
            errexit('Destination HTML file exists! -f to overwrite!')
    try:
        pFile = open(ofname, 'w')
    except OSError:
        errexit('Could not create file for writing: "' + ofname + '"')
    head = """
    <html><head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <!-- Latest compiled and minified CSS -->
    <title>GPX</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" 
    integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
    crossorigin="anonymous"></head>"""
    head += '<body>'
    head += '<div class="panel panel-default"><div class="panel-heading">Generated from file "' + \
            path_leaf(filename) + '"</div><table class="table">'
    pFile.write(head)
    pFile.write('<tr><td>No</td><td>Latitude</td><td>Longitude</td><td>Elevation</td><td>Media</td></tr>')

    for i in range(len(wpts)):
        pFile.write(makeRow(i, wpts[i]))
    pFile.write('</div></table></body></html>')


def process_folder(folder):
    wpts = []
    exts = ['jpg', 'JPG', 'jpeg', 'JPEG']

    def format_waypoint(wpt):
                                                                             # '\n\t\t<ele>227.0</ele>' + \ #TODO FIXME
        rv = '\t<wpt lat="' + str(wpt['lat']) + '" lon="' + str(wpt['lon']) + '">' + \
            '\n\t\t<time>' + wpt['time'] + '</time>' + \
            '\n\t\t<name><![CDATA[Photo]]></name>' + \
            '\n\t\t<link href="' + wpt['fname'] + '">' + \
            '\n\t\t\t<text>' + wpt['fname'] + '</text>' + \
            '\n\t\t</link>' + \
            '\n\t\t<sat>0</sat>' + \
            '\n\t</wpt>'
        return rv

    if not os.path.isdir(folder):
        errexit('Invalid foldername given: "' + folder + '"')
    for dirname, dirnames, filenames in os.walk(folder):
        for fname in filenames:
            if fname.split('.')[1] in exts:
                # print('Valid: ' + fname)
                with open(os.path.join(folder, fname), 'rb') as pFile:
                    img = Image.open(os.path.join(folder, fname))
                    exif_data = get_exif_data(img)
                    lat, lon = get_lat_lon(exif_data)

                    # print(lat, lon)
                    lat = round(lat, 7)
                    lon = round(lon, 7)
                    # print(lat, lon)
                    wpts.append({'lat': lat, 'lon': lon, 'time': exif_data['time'], 'fname': fname})
    if len(wpts) < 1:
        errexit('Could not found photos with GPS tags!')

    gpx_header = '<?xml version="1.0" encoding="UTF-8" ?>' + \
                 '\n<gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.1" creator="gpx_report" ' + \
                 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' + \
                 'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd ">'
    gpx_footer = '</gpx>'

    gpx_fname = os.path.join(folder, path_leaf(folder) + '.gpx')
    print('Destination filename: ' + gpx_fname)
    if os.path.exists(gpx_fname):
        if os.path.isfile(gpx_fname):
            if opt_force:
                print('Overwriting existing GPX file...')
            else:
                errexit('Target GPX file exists! -f to overwrite!')
        else:
            errexit('Will not create GPX file, probably folder with same name exists!')

    try:
        with open(gpx_fname, 'w') as pFile:
            pFile.write(gpx_header)
            for wpt in wpts:
                pFile.write(format_waypoint(wpt))
            pFile.write(gpx_footer)
    except OSError:
        errexit('Write error. Permission issue?')
    except:
        errexit('Something went wrong.')


try:
    opts, args = getopt.getopt(sys.argv[1:], 'hfg:d:', ['gpx=', 'dir=', 'help', 'force'])
except getopt.GetoptError:
    print(_usage)
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print('Help:\n' + _usage)
        sys.exit(0)
    elif opt in ('-d', '--dir'):
        opt_dir = arg
    elif opt in ('-g', '--gpx'):
        opt_gpx = arg
    elif opt in ('-f', '--force'):
        opt_force = True
        if len(sys.argv) < 4:
            errexit('Invalid input!')
    else:
        print(_usage)
        errexit('Invalid option given: "' + opt + '"')


if opt_gpx != '':
    if not os.path.isfile(opt_gpx):
        errexit('Invalid parameter! Not a file "' + opt_gpx + '"')
    try:
        pFile = open(opt_gpx, 'r')
        pFile.close()
    except OSError:
        errexit('Invalid parameter! Can not open "' + opt_gpx + '"')
    process_GPX(opt_gpx)

if opt_dir != '':
    if not os.path.isdir(opt_dir):
        errexit('Invalid parameter! Not a folder "' + opt_dir + '"')
    process_folder(opt_dir)
