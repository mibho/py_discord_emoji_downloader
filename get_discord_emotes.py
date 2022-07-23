#|------------------------------------------------|
#|                 Imports                        |
#|------------------------------------------------|
import re
import ctypes
import sys
import os
import requests
from pathlib import Path

#|------------------------------------------------|
#|                 Constants                      |
#|------------------------------------------------|
FOLDER_NAME = "discord_emotes"

# matches /emojis/<img id>.<ext>; eg: /emojis/756572987699757107.webp
RE_PATTERN_ALL = r'\/([a-z]{6}|([a-z]{8}))\/\d{18}\.([gjpw][einp][bgfp])'
RE_PATTERN_EMOJIS = r'\/([a-z]{6}|)\/\d{18}\.([gjpw][einp][bgfp])'

DISC_EMOTE_START_URL = "https://cdn.discordapp.com/emojis/"
DISC_STICKER_START_URL = "https://media.discordapp.net/stickers/"
ORIG_QUALITY = "?quality=lossless"

EMOTE_OFFSET = 0
STICKER_OFFSET = 2

PNG_LIST = 1
GIF_LIST = 2
NO_MATCH = -1
SRC_STICKER = 11 
SRC_EMOJI = 99

HTTP_OK = 200
HTTP_NOT_MODIFIED = 304

ID_OFFSET_START = 8
ID_OFFSET_END   = 18


# windows messagebox constants; win32 imports not needed :)
MB_OK          = 0
MB_YESNOCANCEL = 3
MB_ICONWARNING = 48

IDCANCEL       = 2
IDYES          = 6
IDNO           = 7

#|------------------------------------------------|
#|                 fn defs                        |
#|------------------------------------------------|

# regex match contains index of last matched char; we look at that
def checkExt(strData, index):
    start = index - 3
    end   = index - 1
    firstChar = strData[start]
    lastChar = strData[end]

    if (firstChar == 'p' or firstChar == 'w') and (lastChar == 'b' or lastChar == 'g'):
        return PNG_LIST
    else:
        if ((firstChar == 'g') and (lastChar == 'f') ):
            return GIF_LIST
    
    return NO_MATCH

def makeFullURL(file_id_string, src_type):

    if src_type == SRC_STICKER:
        starturl = DISC_STICKER_START_URL
    elif src_type == SRC_EMOJI:
        starturl = DISC_EMOTE_START_URL
    else:
        return


    return starturl + file_id_string + ORIG_QUALITY

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


#|------------------------------------------------|
#|                 main stuff                     |
#|------------------------------------------------|

try:
    txt_file = sys.argv[1] 

    if txt_file:
        emote_urls = {}
        failedCount = 0

        with open(txt_file, errors="ignore") as f: # ignore 'unrecognizable' chars
            for line in f:
                match = re.search(RE_PATTERN_ALL, line)
                if match:
                    
                    spanVals = match.span()                    
                    extType = checkExt(line, spanVals[1])

                    if extType != NO_MATCH:
                        src_val = 0
                        
                        dictIndexStart = spanVals[0]
                        secondLetter = dictIndexStart + 1
                        dictIndexStart += ID_OFFSET_START # get to start of emote ID part; ie, need to move 8 chars (/emojis/)
                                                          # /stickers/ is 2 chars more than (/emojis/), hence the offset addition coming up
                        if line[secondLetter] == 'e': 
                            src_val = SRC_EMOJI
                            

                        elif line[secondLetter] == 's':
                            src_val = SRC_STICKER
                            dictIndexStart += STICKER_OFFSET
    
                        dictIndexEnd = dictIndexStart + ID_OFFSET_END
                        placeInDict(line, dictIndexStart, dictIndexEnd , extType, emote_urls, src_val)
        
        if len(emote_urls) != 0:
            result = ctypes.windll.user32.MessageBoxW(None, 'parsed emote links for a total of: ' + str(len(emote_urls)) + ' links' + '\n' + 'download?',  'Matches found!', MB_YESNOCANCEL)
        else:
            result = ctypes.windll.user32.MessageBoxW(None, 'no emote links parsed; check input .txt file data', 'Error: No matches found', MB_OK )

       
        
        if result == IDYES:
            
            Path(FOLDER_NAME).mkdir(parents=True, exist_ok=True)
            os.chdir(FOLDER_NAME)

            

            for item in emote_urls:
                downloadurl = emote_urls[item][1]
                fileType = emote_urls[item][0]

                requestedPage = requests.get(downloadurl, headers={'User-Agent': 'Mozilla/5.0'}, timeout= 2)


                if fileType == PNG_LIST:
                    createdFileName = item + ".png"
                elif fileType == GIF_LIST:
                    createdFileName = item + ".gif"
                
                if (requestedPage.status_code == HTTP_OK or requestedPage.status_code == HTTP_NOT_MODIFIED):
                    savePicFiles(createdFileName, requestedPage.content)
                else:
                    failedCount += 1
        
            if failedCount:
                ctypes.windll.user32.MessageBoxW(None, 'Failed to grab ' + str(failedCount) + ' emotes', 'Error: missed some data', MB_ICONWARNING )
            else:
                ctypes.windll.user32.MessageBoxW(None, 'all emotes obtained :)', 'thabk u', MB_OK )
        
        # 


except IndexError:
    ctypes.windll.user32.MessageBoxW(None, 'Please drag and drop a .txt file! Exiting...', 'Error: No input file', MB_ICONWARNING )
