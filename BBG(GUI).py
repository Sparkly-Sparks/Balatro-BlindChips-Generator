from cProfile import label
from tkinter import *
from math import floor
import json
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import colorchooser
from tkinter import ttk
from turtle import back, bgcolor, left
from PIL import Image
from PIL import ImageTk
import os
from random import randint

#main window
window = Tk()
window.title("Balatro BlindChips Generator - By Sparklz")
window.geometry("800x600+"+str(floor((window.winfo_screenwidth()-800)/2))+"+"+str(floor((window.winfo_screenheight()-600)/2)))
window.resizable(False,False)
winicon=ImageTk.PhotoImage(Image.open("Icon.png"))
window.iconphoto(True,winicon)
window.columnconfigure(0)
window.columnconfigure(1)

#settings
def controlsettings(mode,key):
    with open("settings.json", "r") as settingsfile:
        settings=json.load(settingsfile)
    if mode=="r":
        return settings["settings"][key]
    else:
        msg=["settings.json updated"]
        if isinstance(settings["settings"][key],bool):
            settings["settings"][key]=not settings["settings"][key]
        if key=="center":
            msg.append("Changed automatically center glyph to "+str(settings["settings"][key]))
        if key=="frames":
            frames=21
            try:
                frames=int(simpledialog.askstring(title="Updating settings.json",prompt="Enter a new value(int) for animation length\t\t",initialvalue=21))
            except:
                messagebox.showerror(title="Typeerror",message="Please enter a number\nAnimation length set to 21")
            msg.append("Set animation lenght to "+str(frames)+" frames\t")
            settings["settings"][key]=frames
        if key=="scale":
            scale=[]
            num=""
            text=simpledialog.askstring(title="Updating settings.json",prompt="Enter two new values(int) for width and height\t\n(ex: \"34x34\")",initialvalue="34x34").lower()
            for i in text:
                if len(scale)>1:
                    break
                try:
                    if i=="x" and len(num)>0:
                        scale.append(int(num))
                        num=""
                    else:
                        if int(i) in range(10):
                            num+=i
                except:
                    continue
            scale.append(int(num))
            if len(scale)<2:
                messagebox.showerror(title="Inputerror",message="Please enter two numbers with an \"x\" in the middle\nResolution set to 34x34")
                scale=[34,34]
            msg.append(f"Set resolution to {scale[0]}x{scale[1]}\t\t\t")
            settings["settings"][key]=scale
        with open("settings.json", "w") as settingsfile:
            json.dump(settings,settingsfile,indent=2)
        centerstate()
        messagebox.showinfo(title=msg[0],message=msg[1])

def toggle(mode):
    for i in range(3):
        settingbuttons.entryconfig(i,state=mode)

#variables
hexdigits=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

def centerstate():
    if controlsettings("r","center"):
        name="Automatically center glyph [o]"
    else:
        name="Automatically center glyph [x]"
    settingbuttons.entryconfig(2,label=name)

def decihex(x):
    if str(type(x))=="<class 'int'>":
        code=""
        num2=0
        while x>=16:
            x-=16
            num2+=1
        code+=hexdigits[num2]+hexdigits[x]
    else:
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

def hexcheck(Var):
    Var.set(checkhex(Var.get()))

def checkhex(Var):
    checked=""
    for i in Var:
        if i in hexdigits and len(checked)<8:
            checked+=i
    return checked

def coords(x):
    y=0
    scale=controlsettings("r","scale")
    while x>=scale[0]:
        x-=scale[0]
        y+=1
    return [x,y]

def hexadec(x):
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

def nth(num):
    nth="th"
    if num not in [11,12,13]:
        if num%10==1:
            nth="st"
        if num%10==2:
            nth="nd"
        if num%10==3 or (num%10==4 and randint(1,4)==1):
            nth="rd"
            if randint(1,4)==1:
                nth="st"
    return nth

#settings menu
menubar=Menu(window)
window.config(menu=menubar)
settingbuttons=Menu(menubar)
settingbuttons.add_command(label="Change resolution",command=lambda: controlsettings("w","scale"))
settingbuttons.add_command(label="Change length of animation",command=lambda: controlsettings("w","frames"))
settingbuttons.add_command(label="",command=lambda: controlsettings("w","center"))
centerstate()
menubar.add_cascade(label="Settings",menu=settingbuttons)

#pictures
def preview(mode,frame=None):
    if mode=="picker":
        Image.new("RGBA",(32,32),"#"+hex.get()).save("Pallete/ghost.png")
        demo=PhotoImage(file="Pallete/ghost.png")
        ghost.config(image=demo)
        ghost.image=demo

def pallete(mode,name="",image1="",image2=""):
    if mode=="create":
        pixel=Image.new("RGBA",(1,1),image1)
        pixel.save(name+".png")
    if mode=="color":
        pixel1=Image.open(image1+".png")
        pixel2=Image.open(image2+".png")
        pixel1.alpha_composite(pixel2,(0,0))
        return pixel1.get_flattened_data()[0]
    if mode=="darken":
        efill(bgcol_var)
        pixel1=Image.new("RGBA",(1,1),"#"+image1.get())
        pixel2=Image.new("RGBA",(1,1),(0,0,0,123))
        pixel1.alpha_composite(pixel2,(0,0))
        darkcol_var.set(decihex(pixel1.get_flattened_data()[0]))
    if mode=="glaze":
        efill(shine1_var)
        shine2_var.set(shine1_var.get())

def drawpreview(mode):
    if mode=="save":
        blindchips=Image.open("Pallete/blindchips.png")
        save(blindchips)
        amount.set(0)
        toggle("active")
        savebutt.config(state="disabled")
        status_var.set("Creating "+str(amount.get()+1)+nth(amount.get()+1)+" blind")
    else:
        scalex=controlsettings("r","scale")[0]
        frames=controlsettings("r","frames")
        scaley=controlsettings("r","scale")[1]
        if amount.get()==0:
            blindchips=Image.new("RGBA",(frames*scalex,scaley))
        else:
            temp=Image.open("Pallete/blindchips.png")
            blindchips=Image.new("RGBA",(frames*scalex,scaley*(amount.get()+1)))
            blindchips.paste(temp,(0,0))
        Output=Image.new("RGBA",(scalex*frames,scaley))
        style=style_var.get()
        efill(bgcol_var)
        pallete("create","Pallete/bgcol","#"+bgcol_var.get(),"")
        for num,i in enumerate(Image.open(f"Elements/{style}/BG.png").get_flattened_data()):
            pixel=coords(num)
            if i[3]>0:
                Output.paste(Image.open("Pallete/bgcol.png"),(pixel[0],pixel[1]))
        efill(darkcol_var)
        pallete("create","Pallete/darkcol","#"+darkcol_var.get(),"")
        for num,i in enumerate(Image.open(f"Elements/{style}/dark.png").get_flattened_data()):
            pixel=coords(num)
            if i[3]>0:
                Output.paste(Image.open("Pallete/darkcol.png"),(pixel[0],pixel[1]))
        face=glyph_var.get()
        center=[0,0]
        if controlsettings("r","center"):
            left=up=right=down=0
            center=Image.open(f"Glyphs/{face}")
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
            center=[math.ceil((left+right)/2)-left,math.ceil((up+down)/2)-up]

        efill(fgcol_var)
        fgcol=hexadec(fgcol_var.get())
        for num,i in enumerate(Image.open(f"Glyphs/{face}").get_flattened_data()):
            pixel=coords(num)
            if i[3]>0:
                pallete("create","Pallete/brush",(fgcol[0],fgcol[1],fgcol[2],i[3]),"")
                Output.paste(Image.open("Pallete/brush.png"),(pixel[0]+center[0],pixel[1]+center[1]))

        temp=Output
        for i in range(frames-1):
            Output.paste(temp,(scalex*(i+1),0))

        efill(shine1_var)
        efill(shine2_var)
        pallete("create","Pallete/shine1","#"+shine1_var.get(),"")
        pallete("create","Pallete/shine2","#"+shine2_var.get(),"")
        for j in range(frames):
            shape=f"Shine/shine{j+1}.png"
            for num,k in enumerate(Image.open(f"Elements/{style}/{shape}").get_flattened_data()):
                pixel=coords(num)
                if k[3]>0:
                    shine=1
                    if Image.open(f"Glyphs/{glyph_var.get()}").get_flattened_data()[num][3]>0:
                        shine+=1
                    Output.alpha_composite(Image.open(f"Pallete/shine{shine}.png"),(pixel[0]+scalex*j,pixel[1]))
        if mode=="preview":
            Output.save("Pallete/preview1.png")
            previewgened.set(True)
            previewframes(prototype,"up")
        if mode=="add":
            blindchips.paste(Output,(0,amount.get()*scaley))
            blindchips.save("Pallete/blindchips.png")
            messagebox.showinfo(title="Blind added",message="Blind added to current file\nEditing next blind")
            amount.set(amount.get()+1)
            toggle("disabled")
            savebutt.config(state="active")
            status_var.set("Creating "+str(amount.get()+1)+nth(amount.get()+1)+" blind")

def save(image):
    while True:
        text=simpledialog.askstring(title="Saving to Output folder",prompt="Enter filename\t\t\t\t\t",initialvalue="BlindChips.png").lower()
        ext=[".","p","n","g"]
        if (ext[0]!=text[len(text)-4]) or (ext[1]!=text[len(text)-3]) or (ext[2]!=text[len(text)-2]) or (ext[3]!=text[len(text)-1]):
            text+=".png"
        if not (text in os.listdir("Output")) or messagebox.askyesno(title=f"\"{text}\" exists",message=f"File \"{text}\" already in Output\nOverwrite?"):
            image.save("Output/"+text)
            break

def previewframes(prototype,direction):
    frames=controlsettings("r","frames")
    frame=framenum_var.get()
    if direction=="left":
        frame-=1
    if direction=="right":
        frame+=1
    if frame==0:
        frame=frames
    if frame>frames:
        frame=1
    framenum_var.set(frame)
    scale=controlsettings("r","scale")
    frame-=1
    image=0
    if previewgened.get():
        image+=1
    prototype_image=Image.open(f"Pallete/preview{image}.png").crop((scale[0]*frame,0,scale[0]*(frame+1),scale[1])).resize((250,250),Image.Resampling.BOX)
    prototype_image=ImageTk.PhotoImage(prototype_image)
    prototype.config(image=prototype_image)
    prototype.image=prototype_image

#color picker
def pick():
    picker=colorchooser.askcolor(color="#ffffff")
    efill(hex)
    if picker[1]!=None:
        hex.set(picker[1].replace("#","")+hex.get()[6]+hex.get()[7])
        preview("picker")

def opacity(alpha):
    a=decihex(int(alpha))
    efill(hex)
    code=hex.get()
    rgb=""
    for i in range(6):
       rgb+=code[i]
    hex.set(rgb+a)

def choose(Var):
    efill(hex)
    Var.set(hex.get())

def efill(Var):
    code=Var.get()
    if len(code)!=8:
        while len(code)<6:
            code+="0"
        code+=decihex(alpha_var.get())
    Var.set(code)
    preview("picker")

style = ttk.Style()
style.configure("frame.TFrame", background="#808080")
frame=ttk.Frame(window,relief="raised",style="frame.TFrame")
frame.columnconfigure(0,weight=4)
frame.columnconfigure(1,weight=1)
hex=StringVar(value="ffffffff")
rgba=Entry(frame,textvariable=hex,width=8,background="#f5f5f5",font=("",35),relief="sunken").grid(column=0,row=0,padx=15,pady=15)
hex.trace_add("write",lambda *args: hexcheck(hex))
butticon=ImageTk.PhotoImage(Image.open("Colorpicker.png"))
button=Button(frame,image=butticon,command=pick,relief="raised",background="#ffffff").grid(column=1,row=0,padx=15,pady=15)
alpha_var=IntVar()
slider=Scale(frame,variable=alpha_var,from_=0,to=255,orient="horizontal",relief="sunken",width=10,length=206,command=opacity,font=("",16))
slider.bind("<ButtonRelease>", lambda event: preview("picker"))
slider.set("255")
slider.grid(column=0,row=1,padx=20,pady=20)
ghost=Label(frame,background="#ffffff",image=PhotoImage(file="Pallete/ghost.png"),relief="raised")
ghost.grid(column=1,row=1)

#blindconfig
fontsize=10
frame2=ttk.Frame(window,relief="raised",style="frame.TFrame")
frame2.columnconfigure(0,weight=4)
frame2.columnconfigure(1,weight=1)
style_var=StringVar()
style=ttk.Combobox(frame2,values=os.listdir("Elements"),background="#f5f5f5",state="readonly",textvariable=style_var,font=("",fontsize)).grid(column=0,row=1)
if "default" in os.listdir("Elements"):
    style_var.set("default")
else:
    style_var.set(os.listdir("Elements")[0])
glyph_var=StringVar()
glyphs=[]
for i in os.listdir("Glyphs"):
    if ".png" in i:
        glyphs.append(i)
glyph=ttk.Combobox(frame2,values=glyphs,state="readonly",textvariable=glyph_var,font=("",fontsize)).grid(column=0,row=3,padx=5)
if "S_Small_Blind.png" in glyphs:
    glyph_var.set("S_Small_Blind.png")
else:
    glyph_var.set(glyphs[0])
labels=["Style:","Glyph:","Background color:","Shading color:","Glyph color:","Shine color 1:","Shine color 2:"]
for i in range(len(labels)):
    Label(frame2,text=labels[i],background="#ffffff",font=("",12)).grid(column=0,row=i*2,sticky="w",padx=5,pady=5)
bgcol_var=StringVar(value="808080ff")
darkcol_var=StringVar(value="424242ff")
fgcol_var=StringVar(value="000000ff")
shine1_var=StringVar(value="ffffff4d")
shine2_var=StringVar(value="ffffff4d")
butticonsmall=Image.open("Colorpicker.png").resize((16,16))
butticonsmall=ImageTk.PhotoImage(butticonsmall)
autoiconsmall=Image.open("Auto.png").resize((16,16))
autoiconsmall=ImageTk.PhotoImage(autoiconsmall)
bgcol=Entry(frame2,textvariable=bgcol_var,foreground="#000000",background="#f5f5f5",font=("",fontsize))
bgcol.grid(column=0,row=5)
bgget=Button(frame2,image=butticonsmall,command=lambda: choose(bgcol_var)).grid(column=1,row=5)
darkcol=Entry(frame2,textvariable=darkcol_var,background="#f5f5f5",font=("",fontsize)).grid(column=0,row=7)
darkget=Button(frame2,image=butticonsmall,command=lambda: choose(darkcol_var)).grid(column=1,row=7)
autodark=Button(frame2,image=autoiconsmall,command=lambda: pallete("darken","",bgcol_var)).grid(column=2,row=7,padx=18)
fgcol=Entry(frame2,textvariable=fgcol_var,background="#f5f5f5",font=("",fontsize)).grid(column=0,row=9)
fgget=Button(frame2,image=butticonsmall,command=lambda: choose(fgcol_var)).grid(column=1,row=9)
shinecol1=Entry(frame2,textvariable=shine1_var,background="#f5f5f5",font=("",fontsize)).grid(column=0,row=11)
shine1get=Button(frame2,image=butticonsmall,command=lambda: choose(shine1_var)).grid(column=1,row=11)
shinecol2=Entry(frame2,textvariable=shine2_var,background="#f5f5f5",font=("",fontsize)).grid(column=0,row=13)
shine2get=Button(frame2,image=butticonsmall,command=lambda: choose(shine2_var)).grid(column=1,row=13)
autoshine=Button(frame2,image=autoiconsmall,command=lambda: pallete("glaze")).grid(column=2,row=13,padx=18,pady=5)
bgcol_var.trace_add("write",lambda *args: hexcheck(bgcol_var))
darkcol_var.trace_add("write",lambda *args: hexcheck(darkcol_var))
fgcol_var.trace_add("write",lambda *args: hexcheck(fgcol_var))
shine1_var.trace_add("write",lambda *args: hexcheck(shine1_var))
shine2_var.trace_add("write",lambda *args: hexcheck(shine2_var))

#generator
frame3=ttk.Frame(window,relief="raised",style="frame.TFrame")
frame3.columnconfigure(0,weight=4)
frame3.columnconfigure(1,weight=1)
scale=controlsettings("r","scale")
amount=IntVar(value=0)
status_var=StringVar(value="Creating "+str(amount.get()+1)+nth(amount.get()+1)+" blind")
status=Label(frame3,textvariable=status_var,font=("",20)).grid(column=0,row=0,pady=5)
prototype_image=Image.open("Pallete/preview0.png").crop((0,0,scale[0],scale[1])).resize((250,250),Image.Resampling.BOX)
prototype_image=ImageTk.PhotoImage(prototype_image)
prototype=Label(frame3,background="#808080",image=prototype_image)
prototype.grid(column=0,row=1,columnspan=3,padx=20,pady=3)
previewgened=BooleanVar(value=False)
genprototype=Button(frame3,text="Refresh Preview",font=("",16),command=lambda: drawpreview("preview"))
genprototype.grid(column=0,row=2,pady=10)
frameleft=Button(frame3,text="<",font=("",16),command=lambda: previewframes(prototype,"left")).grid(column=1,row=2)
framenum_var=IntVar(value=1)
framenum=Label(frame3,textvariable=framenum_var,font=("",16),width=2).grid(column=2,row=2)
frameright=Button(frame3,text=">",font=("",16),command=lambda: previewframes(prototype,"right")).grid(column=3,row=2,padx=4)
addbutt=Button(frame3,text="Add blind to file",font=("",16),command=lambda: drawpreview("add")).grid(column=0,row=3)
savebutt=Button(frame3,text="Save file to Output",font=("",16),command=lambda: drawpreview("save"))
savebutt.grid(column=0,row=4,pady=10)
savebutt.config(state="disabled")

#contents
window.config(background="#404040")
frame.grid(column=0,row=0,padx=20,pady=10)
frame2.grid(column=0,row=1,padx=20,pady=5)
frame3.grid(column=1,row=0,rowspan=2,padx=70,pady=10)
window.mainloop()
