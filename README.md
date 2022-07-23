# py_discord_emoji_downloader

-----
scuffed .py script to download all emojis from a server you're a member of (with a few steps)

drag and drop text file (.har, .txt, ...) w/ browser traffic and get emojis in bulk :)

parses text file of URLs, gets sticker/emoji IDs, then downloads them (no duplicates). 

also works for stickers. same exact steps except you click stickers box instead of the emojis box

made on python 3.10.5; refer to 'guide' below please.

# **Only for Windows** ![lol](https://i.imgur.com/Maa234i.png)

Example run [recording from step 7 to end]: https://i.gyazo.com/29e0bb295c894de5bd56be05396a6645.mp4

## NOTE: IF YOU ALREADY KNOW HOW TO GET A .har OR .txt FILE VIA FIREFOX/CHROME OR SOME OTHER TOOL, [SKIP TO STEP 4](#step-4-let-the-emojis-that-you-want-to-download-fully-load)

## How to use (for Firefox) 

### Step 1: open web developer tools.
![step1_web_tools](https://user-images.githubusercontent.com/86342821/180592651-0b57c1f8-baa3-4a3f-bf99-f5a378e97d1d.png)

### Step 2: go to the network tab in the tool. [it starts logging by itself so dont worry]
![step2_web_tools](https://user-images.githubusercontent.com/86342821/180592900-28d785bc-2496-4bc0-aa11-1a0819089a93.png)

### Step 3: open your emotes.
![step3_web_tools](https://user-images.githubusercontent.com/86342821/180592951-926bba92-1bd4-4a69-b45d-d61811452742.png)

### Step 4: let the emojis that you want to download ***FULLY LOAD***
![step4_web_tools](https://user-images.githubusercontent.com/86342821/180593074-f4003b2f-3347-41d7-8845-eea838daee6d.png)

> all of the emojis enclosed in the green box are visible/not buffering; ie, fully loaded.

-----
#### another example: if you want <insert server>'s emojis, go to that server's emotes. 
-----
![step4b_web_tools](https://user-images.githubusercontent.com/86342821/180593308-da54123b-d9e2-4b09-ab0c-5ee17007215c.png)

### Step 5: click the tiny gear in the top right corner of the network tool and click 'Save All as HAR'
![step5_web_tools](https://user-images.githubusercontent.com/86342821/180593564-978ab31d-77a2-4d0e-9eac-b92ab4a891d3.png)

### Step 6: save the file in the same folder as the script (or .exe if no python) 
![step_6_web_tools](https://user-images.githubusercontent.com/86342821/180593672-a5937778-c765-40d8-b873-5eb806406d4a.png)

### Step 7: drag and drop the .har onto the script or .exe 
![step6_web_tools](https://user-images.githubusercontent.com/86342821/180593722-d0738a29-68fb-48fc-9ec5-736a4f880da1.png)

### Step 8: a console window will pop up and you'll see something like this when the file is all processed
![step_7_web_tools](https://user-images.githubusercontent.com/86342821/180593775-2a6ce725-d850-41b5-b536-d6dcf1e21346.png)

### Step 9: wait and a message box will pop up (if it fails, it'll display # of emotes it failed to get)
![step8_web_tools](https://user-images.githubusercontent.com/86342821/180593791-94f0917b-6374-4713-867d-dd795a85f26d.png)

-----
#### Step 10: look for a folder named 'discord_emotes' 
-----

![step9_web_tools](https://user-images.githubusercontent.com/86342821/180593910-1be79ade-e967-45fa-8923-28d1b3c45491.png)

![step10_web_tools](https://user-images.githubusercontent.com/86342821/180593921-ca0d7e27-6691-43b5-87b0-a331a6c9cbd2.png)


p.s. this wasnt meant for release and won't be maintained but i will make README more coherent when time permits.
