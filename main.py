

import linecache
import fileinput
import sys
import os
import re
import io #this is to support python 2.x
import codecs
import chardet

filename = ''


def utf8_converter(file_path, universal_endline=True):
    '''
    Convert any type of file to UTF-8 without BOM
    and using universal endline by default.

    Parameters
    ----------
    file_path : string, file path.
    universal_endline : boolean (True),
                        by default convert endlines to universal format.
    '''

    # Fix file path
    file_path = os.path.realpath(os.path.expanduser(file_path))

    # Read from file
    file_open = open(file_path)
    raw = file_open.read()
    file_open.close()

    # Decode
    # raw = raw.decode(chardet.detect(raw)['encoding'])
    # Remove windows end line
    if universal_endline:
        raw = raw.replace('\r\n', '\n')
    # Encode to UTF-8
    raw = raw.encode('utf8')
    # Remove BOM
    if raw.startswith(codecs.BOM_UTF8):
        raw = raw.replace(codecs.BOM_UTF8, '', 1)

    # Write to file
    file_open = open(file_path, 'w')
    file_open.write(str(raw))
    file_open.close()
    srt_to_vtt(file_path)
    return 0


def srt_to_vtt(path):
    with open(path, 'r') as myfile: #USE THIS ONCE UPGRADE TO PYTHON 3.x
        text = myfile.read()
        captions1 = re.sub(r'(^\d\d\:\d\d\:\d\d)\,(\d\d\d)( --> \d\d\:\d\d\:\d\d)\,(\d\d\d)',r'\1.\2\3.\4',text, flags=re.MULTILINE)
        captions2 = re.sub(r'^\d{1,6}\n(\d)',r'\1',captions1, flags=re.MULTILINE) #Remove index numbers
        captions3 = re.sub(r'\A',r'WEBVTT\n\n',captions2, flags=re.MULTILINE) #remove WEBVTT from beginning
        newfile = open(path[0:-4]+'.vtt','w')
        newfile.write(captions3)
        myfile.close()
        newfile.close()

if len(sys.argv) > 1: #check that there's at least something for an arugment.
    file_path = sys.argv[1] #set variable to path/filename
    print("file_path: " + file_path)
    filename = os.path.basename(file_path) #set filename only variable
    print("filename: " + filename)
    if filename.lower().endswith('.srt'): #test if srt
        print("working on srt file: " + filename)
        utf8_converter(file_path) #strips out BOM encoding, then calls converter function
    elif filename.lower().endswith('.vtt'): #test if vtt
        print("\n\n******* only accepts SRT *******\nfile provided: "+ filename + "\n\n")

    else:
        print("\n\n******* only accepts SRT *******\nfile provided: "+ filename + "\n\n") #if neither vtt or srt
else:
    print('\n\n******* No file provided. Try again. ******* \n') #if no file argument given
