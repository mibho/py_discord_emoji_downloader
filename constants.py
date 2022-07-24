#|------------------------------------------------|
#|                 Constants                      |
#|------------------------------------------------|
# Project constants
FOLDER_NAME = "discord_emotes"
REQ_DELAY = 0.1
#|------------------------------------------------|
# Parsing/URL constants
RE_PATTERN_ALL         =  r'\/([a-z]{6}|([a-z]{8}))\/\d{18}\.([gjpw][einp][bgfp])'
RE_PATTERN_EMOJIS      =  r'\/([a-z]{6}|)\/\d{18}\.([gjpw][einp][bgfp])'
DISC_EMOTE_START_URL   =  "https://cdn.discordapp.com/emojis/"
DISC_STICKER_START_URL =  "https://media.discordapp.net/stickers/"
ORIG_QUALITY           =  "?quality=lossless"
#|------------------------------------------------|
# string position offsets
EMOTE_INDEX_OFFSET     =  0
STICKER_INDEX_OFFSET   =  2
OFFSET_FOR_START_ID    =  8
OFFSET_FOR_END_ID      = 18
OFFSET_FOR_EXT_START   =  3 
OFFSET_FOR_EXT_END     =  1
#|------------------------------------------------|
# Type/category constants
PNG_LIST               =  1
GIF_LIST               =  2
NO_MATCH               = -1
SRC_TYPE_ID_STICKER    = 11 
SRC_TYPE_ID_EMOJI      = 99
#|------------------------------------------------|

# Predefined constants 
#|------------------------------------------------|
# HTTP Response 
HTTP_OK                = 200
HTTP_NOT_MODIFIED      = 304
#|------------------------------------------------|
# Win 32 msgbox constants
W32_MB_OK              = 0
W32_MB_YESNOCANCEL     = 3
W32_MB_ICONWARNING     = 48

W32_IDCANCEL           = 2
W32_IDYES              = 6
W32_IDNO               = 7
#|------------------------------------------------|
