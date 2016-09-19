import os.path
import os;
import ID3;
#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

from ID3 import *;
from os import *;
from os import renames
import sys;
import logging;
from musicbrainz2.webservice import Query, TrackFilter, WebServiceError;


__author__="monster"
__date__ ="$1 Jan, 2011 5:24:09 PM$"

def returnContents(directory, output):
    try:
        print directory;
        mp3files = []
        for filename in listdir(directory):
            pathname = path.join(directory, filename)
            if path.isdir(pathname):
                returnContents(pathname, output)
            if path.isfile(pathname) and pathname.endswith('.mp3'):
                    # Change the tags
                    print filename
                    id3info = getID3info(pathname);
                    info = musicbrainz(pathname, filename);
                    if info != None:
                        id3info['TITLE'] = info.title;
                        id3info['ARTIST'] = info.artist.name;
                    if id3info.has_tag and len(id3info.title)>0:
                        newname = id3info.artist + " - " + id3info.title + ".mp3";
                        newdir = output + "/" + id3info.artist;
                        if path.isdir(newdir) == 0  and path.isfile(newdir) ==0:
                            os.makedirs(newdir, 0777);
                            dst = newdir + "/" + newname;
    #                            print newdir + '/'+ filename;
                        print newname;
    #                            copyfile(pathname, dst);
    #                            pathname.substitute(" ", "\ ")
    #                            newdir.substitute(" ", "\ ")
    #                    if path.isfile(newdir + '/'+ filename)== 0 and path.isfile(pathname)== 1:
                        os.system ("mv \"%s\" \"%s\"" % (pathname, newdir))
                        print "Method 1 file copied"
                        renames(newdir + '/'+ filename, newdir + '/'+newname)

                    else:
                        newdir = output + "/Misc"
                        if path.isdir(newdir) == 0 and path.isfile(newdir) == 0:
                            os.makedirs(newdir, 0777);
#                            if path.isfile(newdir + '/'+ filename)== 0 and path.isfile(pathname)== 1:
                        os.system ("mv \"%s\" \"%s\"" % (pathname, newdir))
                        print "Method 2 file copied"
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        return 1







def getID3info(filename):
    try:
        id3info = ID3(filename)
    except InvalidTagError, message:
        print "Invalid ID3 tag:", message
    return id3info;



def musicbrainz(filename, file):
    try:
        logging.basicConfig()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        q = Query()

        id3info = getID3info(filename);
        if id3info.has_tag and len(id3info.title)>0:
            try:
                f = TrackFilter(title=id3info.title, artistName=id3info.artist)
                results = q.getTracks(f)
            except WebServiceError, e:
                print 'Error:', e
                sys.exit(1)
        else:
            tags = file.split("-");
            title = tags[len(tags)-1].split(".")
            try:
                if len(tags)>=2:
                    f = TrackFilter(title=title[0], artistName=tags[0])
                    results = q.getTracks(f)
                else:
                    f= TrackFilter(title=title[0], artistName= None)
                    results = q.getTracks(f)
            except WebServiceError, e:
                print 'Error:', e
                sys.exit(1)
            except UnicodeDecodeError, e:
                print 'Error:',e
                return None

        for result in results:
            track = result.track;
            if result.score == 100:
                return track;

        return None;
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        return None



def copyfile(src, dst):
    """Copy data from src to dst"""
    if (src == dst):
        return 1
    if path.isfile(dst)== 0 and path.isfile(src)== 1:
        with  open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                while buf!=0 :
                    buf = fsrc.read(16*1024)
                    fdst.write(buf)

def main():
    if len(sys.argv) != 3:
	print "Usage: Input Directory Output Directory"
	sys.exit(1)

if len(sys.argv) == 3:
	directory = sys.argv[1]
        output = sys.argv[2]
        returnContents(directory, output)
else :
    directory = None;



if __name__ == "__main__":
    main();
