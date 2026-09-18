from PIL import Image
import os
from random import randint
import math
import json
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("settings.json", "r") as settings:
    settings=json.load(settings)

active_preview=settings["settings"]["active_preview"] #Turn this on to get jumpscared by a preview image every time you add a blind and once the file is saved.
scale=settings["settings"]["scalex"] #Change this if you want other resolutions(Will require changing the files in the Elements and Glyphs folders).
ask_to_center=settings["settings"]["center"] #Turn this on if you want the blind's symbol to be automatically centered. (Not sure why anyone would want this.)

def hexadec(x,default="ffffff"):
    if x=="":
        x=default
    if len(x)==6:
        x=x+"ff"
    hex=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    colors=[]
    color=0
    first=True
    for i in x:
        if len(x)!=8 or i not in hex:
            return "input error"
        num=-1
        for j in hex:
            num+=1
            if i==j:
                if first:
                    num*=16
                    color+=num
                    num=-1
                if not first:
                    color+=num
                    colors.append(color)
                    color=0
                first=not first
    return colors

def pallete(mode,name,image1,image2):
    if mode=="create":
        pixel=Image.new("RGBA",(1,1),image1)
        pixel.save(name+".png")
    if mode=="color":
        pixel1=Image.open(image1+".png")
        pixel2=Image.open(image2+".png")
        pixel1.alpha_composite(pixel2,(0,0))
        return pixel1.get_flattened_data()[0]

def decihex(x):
    if len(x)!=4:
        x+=255,
    if len(x)!=4:
        return "input error"
    hex=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    code=""
    for num1 in x:
        num2=0
        while num1>=16:
            num1-=16
            num2+=1
        code+=hex[num2]+hex[num1]
    return code

def coords(x):
    y=0
    while x>=scale:
        x-=scale
        y+=1
    return [x,y]

def save(image):
    files=os.listdir("Output")
    x=len(files)
    name=f"BlindChips({x+1}).png"
    if name in files:
        print(f'Attempting to save "{name}" in Output.\n"{name}" already present in Output.\nThis script counts the files in the output folder to name the generated images.\nDid you move or delete a file?\nPress enter to overwrite "{name}".')
        input()
    image.save("Output/"+name)
    if name in os.listdir("Output"):
        print(f"File saved ({name}).")

def set_style(style,preset):
    while True:
        if style=="":
            print("Styles",os.listdir("Elements"))
            style=input("Select the style you want to use.\nLeave blank for default. (default=default)\n:")
        if style=="":
            style="default"
        if style in os.listdir("Elements"):
            break
        print(f"Style ({style}) not found")
        style=""
        if preset:
            sys.exit("Fix your preset file before retrying.")
    return style

while True:
    mode=input("\nTo make blinds from scratch manually, type (A/a)\nTo shine preexisting blinds, type (B/b)\nTo use a preset file, type (C/c)\n: ").lower()
    if mode in ["a","b","c"]:
        break
    print(f"Invalid input, please retry. ({mode})")

if mode=="c":
    while True:
        preset=[]
        for i in os.listdir("Presets"):
            preset.append(i.replace(".json",""))
        print("Presets",preset)
        preset=input("Select the preset you want to use.\nLeave blank for default. (default=default)\n:")
        if preset=="":
            preset="default"
        if preset+".json" in os.listdir("Presets"):
            with open(f"Presets/{preset}.json", "r") as preset:
                preset=json.load(preset)
                preset_blinds=[]
                for i in preset:
                    preset_blinds.append(i)
            break
        print(f"Preset ({preset}) not found")

if mode in ["a","c"]:
    cycle=0
    faces=[]
    Output=Image.new("RGBA",(21*scale,scale*(cycle+1)))
    while True:
        print("Currently making blind number",cycle+1)
        if cycle>0:
            temp=Image.new("RGBA",(21*scale,scale*(cycle+1)))
            temp.paste(Output,(0,0))
            Output=temp

        style=""
        if mode=="c":
            style=preset[preset_blinds[cycle]]["style"]
        style=set_style(style,mode=="c")

        while True:
            if mode=="a":
                bgcol=hexadec(input("Input 6 or 8 digit hex code (RGB or RGBA) for background.\nLeave blank for default. (default=808080ff)\n: "),"808080ff")
            if mode=="c":
                bgcol=hexadec(preset[preset_blinds[cycle]]["bg"])
            if bgcol!="input error":
                pallete("create","Pallete/bgcol",tuple(bgcol),"")
                for num,i in enumerate(Image.open(f"Elements/{style}/BG.png").get_flattened_data()):
                    pixel=coords(num)
                    if i[3]>0:
                        Output.paste(Image.open("Pallete/bgcol.png"),(pixel[0],pixel[1]+scale*cycle))
                break
            print(f"Invalid input\n: {bgcol}")
            if mode=="c":
                sys.exit("Fix your preset file before retrying.")


        pallete("create","Pallete/dark",(0,0,0,123),"")
        autodark=decihex(pallete("color","","Pallete/bgcol","Pallete/dark"))

        while True:
            if mode=="a":
                darkcol=hexadec(input(f"Input 6 or 8 digit hex code (RGB or RGBA) for the dark pixels below.\nLeave blank for automatic mode(not recommended). (auto={autodark})\n: "),autodark)
            if mode=="c":
                darkcol=hexadec(preset[preset_blinds[cycle]]["dark"],autodark)
            if darkcol!="input error":
                pallete("create","Pallete/darkcol",tuple(darkcol),"")
                for num,i in enumerate(Image.open(f"Elements/{style}/dark.png").get_flattened_data()):
                    pixel=coords(num)
                    if i[3]>0:
                        Output.paste(Image.open("Pallete/darkcol.png"),(pixel[0],pixel[1]+scale*cycle))
                break
            print(f"Check your input and try again\n: {darkcol}")
            if mode=="c":
                sys.exit("Fix your preset file before retrying.")

        while True:
            for i in os.listdir("Glyphs"):
                if ".png" in i and mode!="c":
                    print(i.replace(".png",""))
            if mode=="a":
                face=input("Select glyph from list(Glyphs folder). (Supports transparency)\nLeave blank for default. (default=S_Small_Blind)\n:")
            if mode=="c":
                face=preset_blinds[cycle]
            if face=="":
                face="S_Small_Blind"
            if face+".png" in os.listdir("Glyphs"):
                faces.append(face)
                break
            print(f"Glyph not found\n: {face}\n")
            if mode=="c":
                sys.exit("Fix your preset file before retrying.")

        center=[0,0]
        if ask_to_center:
            left=up=right=down=0
            center=Image.open(f"Glyphs/{face}.png")
            for i in range(center.size[0]):
                for j in range(center.size[1]):
                    if center.getpixel((i,j))[3]>0:
                        if left==0:
                            left=i
                        right=center.size[0]-i-1
            for j in range(center.size[0]):
                for i in range(center.size[1]):
                    if center.getpixel((i,j))[3]>0:
                        if up==0:
                            up=i
                        down=center.size[0]-i-1
            print(up,down,left,right)
            center=[math.ceil((left+right)/2)-left,math.ceil((up+down)/2)-up]
            print(center)

        while True:
            if mode=="a":
                fgcol=hexadec(input(f"Input 6 digit hex code (RGB) for the glyph color.\nLeave blank for automatic mode(not recommended). (auto=000000)\n: "),"000000")
            if mode=="c":
                fgcol=hexadec(preset[preset_blinds[cycle]]["glyph"])
            if fgcol!="input error":
                for num,i in enumerate(Image.open(f"Glyphs/{face}.png").get_flattened_data()):
                    pixel=coords(num)
                    if i[3]>0:
                        pallete("create","Pallete/brush",(fgcol[0],fgcol[1],fgcol[2],i[3]),"")
                        Output.paste(Image.open("Pallete/brush.png"),(pixel[0]+center[0],pixel[1]+center[1]+scale*cycle))
                break
            print(f"Check your input and try again\n: {fgcol}\n")
            if mode=="c":
                sys.exit("Fix your preset file before retrying.")

        if active_preview:
            Output.show()
        if mode=="a":
            while True:
                x=input('To add one more blind, enter "(Y/y)"\nTo finish and proceed to adding shine animation, enter (N/n)\n: ').lower()
                if x in ["y","n"]:
                    break
                print("Wrong answer.\n")
        if mode=="c":
            x="n"
            if len(preset_blinds)-1>cycle:
                x="y"
        if x=="n":
            break
        cycle+=1

    temp=Output
    for i in range(20):
        Output.paste(temp,(scale*(i+1),0))

if mode=="b":
    print("")
    for i in os.listdir("Preexisting"):
        print(i)
    while True:
        Preexisting=input('Select a preexisting image from the "Preexisting" folder to apply shine to.\n: ')
        if Preexisting in os.listdir("Preexisting"):
            Output=Image.open(f"Preexisting/{Preexisting}")
            faces=[]
            print(Output.size[1],scale)
            for i in range(int(Output.size[1]/scale)):
                faces.append("???")
            break
    style=set_style("",mode=="c")

for cycle,i in enumerate(faces):
    nth="th"
    num2=cycle+1
    if num2 not in [11,12,13]:
        if num2%10==1:
            nth="st"
        if num2%10==2:
            nth="nd"
        if num2%10==3 or (num2%10==4 and randint(1,4)==1):
            nth="rd"
            if randint(1,4)==1:
                nth="st"
    print(f"Applying shine to {cycle+1}{nth} blind in list({i}).")
    while True:
        if mode in ["a","b"]:
            shinecol1=hexadec(input("Input 6 or 8 digit hex code (RGB or RGBA) for shine effect 1 (Will shine over blind background).\nLeave blank for default(not recommended). (default=ffffff4d)\n: "),"ffffff4d")
        if mode=="c":
            shinecol1=hexadec(preset[preset_blinds[cycle]]["shine1"])
        if shinecol1!="input error":
            break
        print(f"Check your input and try again\n: {shinecol1}")
        if mode=="c":
            sys.exit("Fix your preset file before retrying.")

    while True:
        if mode in ["a","b"]:
            shinecol2=hexadec(input(f"Input 6 or 8 digit hex code (RGB or RGBA) for shine effect 2 (Will shine over blind glyph).\nLeave blank for default(not recommended). (default={decihex(shinecol1)})\n: "),decihex(shinecol1))
        if mode=="c":
            shinecol2=hexadec(preset[preset_blinds[cycle]]["shine2"])
        if shinecol2!="input error":
            pallete("create","Pallete/shine1",tuple(shinecol1),"")
            if mode!="b":
                pallete("create","Pallete/shine2",tuple(shinecol2),"")
            for j in range(21):
                shape=f"shine{max(1,j-11)}.png"
                for num,k in enumerate(Image.open(f"Elements/{style}/{shape}").get_flattened_data()):
                    pixel=coords(num)
                    if k[3]>0:
                        shine=1
                        if mode!="b" and Image.open(f"Glyphs/{i}.png").get_flattened_data()[num][3]>0:
                            shine=2
                        Output.alpha_composite(Image.open(f"Pallete/shine{shine}.png"),(pixel[0]+scale*j,pixel[1]+scale*cycle))
            if active_preview:
                Output.show()
            break
        print(f"Check your input and try again\n: {shinecol2}")
        if mode=="c":
            sys.exit("Fix your preset file before retrying.")
save(Output)
if active_preview:
    Output.show()
