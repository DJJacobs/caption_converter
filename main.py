# -*- coding: utf-8 -*-

import fileinput
import sys
import os
import re


filename = ''

def srt_to_txt(path,captions):
    strip_r = re.sub('\r','',captions) #strip our all /r's - some srt files have /r and /n.
    regex = r'\d+\n\d+\:\d+\:\d+\,\d+.+\n'
    substr = ''
    plainText = re.sub(regex, substr, strip_r)
    # print(plainText)
    with open(path[0:-4]+'.txt','w') as txt:
        txt.write(plainText)


def vtt_to_txt(path):
    print('converting to TXT...')
    with open(path, 'r') as myfile: #USE THIS ONCE UPGRADE TO PYTHON 3.x
        text = myfile.read()
        strip_r = re.sub('\r','',text) #strip our all /r's - some vtt files have /r and /n.
        strip_vtt = re.sub('WEBVTT\n','',strip_r) #remove WEBVTT heading
        strip_1st_line = re.sub('\n\n\n','',strip_vtt)
        regex = r'^\d+\:\d+\:\d+\.\d+.+\n' #vtt specific match pattern
        substr = ''
        plainText = re.sub(regex, substr, strip_1st_line,0, re.MULTILINE)
        with open(path[0:-4]+'.txt','w') as txt:
            txt.write(plainText)


def srt_to_vtt(path):
    print('converting SRT to VTT...')
    with open(path, 'r') as myfile: #USE THIS ONCE UPGRADE TO PYTHON 3.x

        text = myfile.read()
        srt_to_txt(path,text) #Call the converter function with the scrubbed text
        captions1 = re.sub(r'^\d{1,6}\n(\d)',r'\1',text, flags=re.MULTILINE) #Remove index numbers
        captions2 = re.sub(r'(^\d\d\:\d\d\:\d\d)\,(\d\d\d)( --> \d\d\:\d\d\:\d\d)\,(\d\d\d)',r'\1.\2\3.\4',captions1, flags=re.MULTILINE)
        captions3 = re.sub(r'\A',r'WEBVTT\n\n',captions2, flags=re.MULTILINE) #remove WEBVTT from beginning
        with open(path[0:-4]+'.vtt','w') as new_vtt_file:
            new_vtt_file.write(captions3)


'''
Run command and drop in SRT file to convert
Process input and send to appropriate function
'''
if len(sys.argv) > 1: #check that there's at least something for an arugment.
    file_path = sys.argv[1] #set variable to path/filename
    filename = os.path.basename(file_path) #set filename only variable
    if filename.lower().endswith('.srt'): #test if srt
        print("working on srt file: " + filename)
        # utf8_converter(file_path) #strips out BOM encoding, then calls converter function
        srt_to_vtt(file_path)
    elif filename.lower().endswith('.vtt'): #test if vtt
        print("\n******* coverting VTT to TXT *******")
        vtt_to_txt(file_path,)

    else:
        print("\n\n******* only accepts SRT *******\nfile provided: "+ filename + "\n\n") #if neither vtt or srt
else:
    print('\n\n******* No file provided. Try again. ******* \n') #if no file argument given
