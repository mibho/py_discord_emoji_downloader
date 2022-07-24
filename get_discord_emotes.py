#|------------------------------------------------|
#|                 Imports                        |
#|------------------------------------------------|
#--------------------------------------
# standard imports  
#--------------------------------------
import re
import ctypes
import sys
import os
import requests
import time
#--------------------------------------
# project specific imports  
#--------------------------------------
import constants as const

#--------------------------------------
# public/3rd party imports  
#--------------------------------------
from pathlib import Path


#|------------------------------------------------|
#|                 fn defs                        |
#|------------------------------------------------|

# regex match contains index of last matched char; we look at that
def checkExt(strData, index):
    start = index - const.OFFSET_FOR_EXT_START
    end   = index - const.OFFSET_FOR_EXT_END
    firstChar = strData[start]
    lastChar = strData[end]

    if (firstChar == 'p' or firstChar == 'w') and (lastChar == 'b' or lastChar == 'g'):
        return const.PNG_LIST
    else:
        if ((firstChar == 'g') and (lastChar == 'f') ):
            return const.GIF_LIST
    
    return const.NO_MATCH

def makeFullURL(file_id_string, src_type):

    if src_type == const.SRC_TYPE_ID_STICKER:
        starturl = const.DISC_STICKER_START_URL
    
    elif src_type == const.SRC_TYPE_ID_EMOJI:
        starturl = const.DISC_EMOTE_START_URL
    
    else:
        return

    return starturl + file_id_string + const.ORIG_QUALITY

def getSubString(strData, id_pos_start, id_pos_end):

    if (id_pos_start < 0) or (id_pos_end > len(strData)): 
        return

    return strData[id_pos_start:id_pos_end]

def placeInDict(strData, id_pos_start, id_pos_end, dType, ourDict, src_type):

    emote_ID = getSubString(strData, id_pos_start, id_pos_end)

    if emote_ID not in ourDict:
        link = makeFullURL(emote_ID, src_type)
        ourDict[emote_ID] = (dType, link)

def savePicFiles(fileName, fileData):

    with open(fileName, 'wb') as f:
        f.write(fileData)

def moveToFolder(folderName):
    if not os.path.isdir(folderName):
        Path(folderName).mkdir(parents=True, exist_ok=True)

    os.chdir(folderName)


def filterDuplicates(ourDict):

    for item in os.scandir('.'):
        if item.is_file():
            fileName = Path(item.name).stem
            if fileName in ourDict:
                del ourDict[fileName]

def createMessageBox(msg, title_name, flag):
    return ctypes.windll.user32.MessageBoxW(None, msg, title_name, flag)

#|------------------------------------------------|
#|                 main stuff                     |
#|------------------------------------------------|
def run():
    try:

        txt_file = sys.argv[1] 

        if txt_file:
            emote_urls = {}
            failedCount = 0

            with open(txt_file, errors="ignore") as f: # ignore 'unrecognizable' chars
                for line in f:
                    match = re.search(const.RE_PATTERN_ALL, line)
                    if match:
                        
                        spanVals = match.span()                    
                        extType = checkExt(line, spanVals[1])

                        if extType != const.NO_MATCH:
                            src_val = 0
                            
                            dictIndexStart = spanVals[0]
                            secondLetter = dictIndexStart + 1
                            dictIndexStart += const.OFFSET_FOR_START_ID # get to start of emote ID part; ie, need to move 8 chars (/emojis/)
                                                            # /stickers/ is 2 chars more than (/emojis/), hence the offset addition coming up
                            if line[secondLetter] == 'e': 
                                src_val = const.SRC_TYPE_ID_EMOJI
                                

                            elif line[secondLetter] == 's':
                                src_val = const.SRC_TYPE_ID_STICKER
                                dictIndexStart += const.STICKER_INDEX_OFFSET
        
                            dictIndexEnd = dictIndexStart + const.OFFSET_FOR_END_ID
                            placeInDict(line, dictIndexStart, dictIndexEnd , extType, emote_urls, src_val)
            
            orig_len = len(emote_urls)

            if orig_len != 0:
                result = createMessageBox('parsed emote links for a total of: ' + str(orig_len) + ' links' + '\n' + 'download?',  'Matches found!', const.W32_MB_YESNOCANCEL)
            else:
                result = createMessageBox('no emote links parsed; check input .txt file data', 'Error: No matches found', const.W32_MB_OK )

        
            
            if result == const.W32_IDYES:                
                
                moveToFolder(const.FOLDER_NAME)

                filterDuplicates(emote_urls)
                number = 1
                filteredListLen = len(emote_urls)
                diff = orig_len - filteredListLen

                createMessageBox(str(diff) + ' have already been downloaded. \n' + 'downloading remaining ' + str(filteredListLen) + ' links', 'Matches found!', const.W32_MB_OK )

                for item in emote_urls:
                    downloadurl = emote_urls[item][1]
                    fileType = emote_urls[item][0]
                    
                    time.sleep(const.REQ_DELAY)
                    requestedPage = requests.get(downloadurl, headers={'User-Agent': 'Mozilla/5.0'}, timeout= None)
                    if requestedPage:
                        
                        if fileType == const.PNG_LIST:
                            createdFileName = item + ".png"
                        elif fileType == const.GIF_LIST:
                            createdFileName = item + ".gif"
                        
                    

                        if (requestedPage.status_code == const.HTTP_OK or requestedPage.status_code == const.HTTP_NOT_MODIFIED):
                            savePicFiles(createdFileName, requestedPage.content)
                            status = "success!"
                        else:
                            failedCount += 1
                            status = "fail w/ HTTP Error: " + str(requestedPage.status_code)

                        print(str(number) + "/" + str(filteredListLen) + ": " + status)

                        number += 1

                if failedCount:
                    createMessageBox('Failed to grab ' + str(failedCount) + ' emotes', 'Error: missed some data', const.W32_MB_ICONWARNING )
                else:
                    createMessageBox('all emotes obtained :)', 'thabk u', const.W32_MB_OK )
            
            # 


    except IndexError:
        createMessageBox('Please drag and drop a .txt file! Exiting...', 'Error: No input file', const.W32_MB_ICONWARNING )


run()
