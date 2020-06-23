# -*- coding: utf-8 -*-

import linecache
import fileinput
import sys
import os
import re
import io #this is to support python 2.x
import codecs
import chardet

filename = ''

def srt_to_txt(path,captions):
    strip_r = re.sub('\r','',captions) #strip our all /r's - some srt files have /r and /n.
    regex = r'\d+\n\d+\:\d+\:\d+\,\d+.+\n'
    substr = ''
    plainText = re.sub(regex, substr, strip_r)
    # print(plainText)
    txt = open(path[0:-4]+'.txt','w')
    txt.write(plainText)
    txt.close()


def srt_to_vtt(path):
    print('converting SRT to VTT...')
    with open(path, 'r') as myfile: #USE THIS ONCE UPGRADE TO PYTHON 3.x

        text = myfile.read()
        srt_to_txt(path,text) #Call the converter function with the scrubbed text
        captions1 = re.sub(r'^\d{1,6}\n(\d)',r'\1',text, flags=re.MULTILINE) #Remove index numbers
        captions2 = re.sub(r'(^\d\d\:\d\d\:\d\d)\,(\d\d\d)( --> \d\d\:\d\d\:\d\d)\,(\d\d\d)',r'\1.\2\3.\4',captions1, flags=re.MULTILINE)
        captions3 = re.sub(r'\A',r'WEBVTT\n\n',captions2, flags=re.MULTILINE) #remove WEBVTT from beginning
        new_vtt_file = open(path[0:-4]+'.vtt','w')
        new_vtt_file.write(captions3)
        new_vtt_file.close()
        new_vtt_file.close()




'''
Run command and drop in SRT file to convert
Process input and send to appropriate function
'''
if len(sys.argv) > 1: #check that there's at least something for an arugment.
    file_path = sys.argv[1] #set variable to path/filename
    print("file_path: " + file_path)
    filename = os.path.basename(file_path) #set filename only variable
    print("filename: " + filename)
    if filename.lower().endswith('.srt'): #test if srt
        print("working on srt file: " + filename)
        # utf8_converter(file_path) #strips out BOM encoding, then calls converter function
        srt_to_vtt(file_path)
    elif filename.lower().endswith('.vtt'): #test if vtt
        print("\n\n******* only accepts SRT *******\nfile provided: "+ filename + "\n\n")

    else:
        print("\n\n******* only accepts SRT *******\nfile provided: "+ filename + "\n\n") #if neither vtt or srt
else:
    print('\n\n******* No file provided. Try again. ******* \n') #if no file argument given
