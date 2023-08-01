import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
import pyttsx3
import pytesseract as tsrct
import pytesseract  as tsrct
tsrct.pytesseract.tesseract_cmd=r'C:\Users\Mayureshwar Shinde\AppData\Local\Tesseract-OCR\tesseract.exe'
poppler_path=r'C:\Program Files\poppler-0.67.0_x86\poppler-0.67.0\bin'
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image

speaker = pyttsx3.init()
sourcePath=""
text=""
saveText=""
status=False

'''Image to Text'''
def imgtxt():
    img = Image.open(sourcePath)
    imgtext = tsrct.image_to_string(img)
    return imgtext


'''PDF to Text'''
def pdftxt():
    pdfpath=sourcePath
    global text
    status=messagebox.askyesno(title='Question',message='Is it a Scanned PDF?')
    book = open(pdfpath,'rb')
    pdfReader = PyPDF2.PdfFileReader(book)

    if(fromTxt.get(1.0, END)=="\n" and toTxt.get(1.0, END)=="\n"):
        start_pgno=0
        end_pgno=pdfReader.numPages
    else:
        start_pgno=int(fromTxt.get(1.0, END))-1 #0
        end_pgno=int(toTxt.get(1.0, END))
    
    if(status==False):
        for i in range(start_pgno, end_pgno):
            currPage=pdfReader.getPage(i)
            text=text+currPage.extractText()
    else:
        pages=convert_from_path(pdf_path=pdfpath,poppler_path=poppler_path)
        for i in range(start_pgno,end_pgno):
            currPage=tsrct.image_to_string(pages[i])
            text=text+currPage
    return text


'''TXT to Text'''
def txttxt():
    fo=open(sourcePath,"r")
    ip=fo.read()
    fo.close()
    return ip


'''Any path to Text'''
def getText():
    l=sourcePath[len(sourcePath) - 1]
    if(l=='f'):
        text=pdftxt()
    elif(l=='g'):
        text=imgtxt()
    else:
        text=txttxt()
    return text


'''Get Destination/Storage path'''
def destPath():
    str=""
    idx=0
    for i in range(len(sourcePath)-1,0,-1):
        if(sourcePath[i]=='/'): break
        idx=idx+1
    for j in range(len(sourcePath)-(idx+1),len(sourcePath)-4):
        str=str+sourcePath[j]
    destination = filedialog.askdirectory()
    return destination+str+".mp3"


'''Say text'''
def say():
    global sourcePath
    global text
    text=text_area.get(1.0, END)
    gender=gender_combobox.get()
    speed=speed_combobox.get()
    voices = speaker.getProperty('voices')

    if(gender=='Male'): speaker.setProperty('voice',voices[0].id)
    else: speaker.setProperty('voice', voices[1].id)

    if(speed=="Fast"): speaker.setProperty('rate',250)
    elif(speed=="Normal"): speaker.setProperty('rate', 150)
    else: speaker.setProperty('rate', 60)

    speaker.say(text)
    speaker.runAndWait()
    sourcePath=""


'''Create and Save Audiobook'''
def save():
    global sourcePath
    global saveText
    text=saveText
    if(sourcePath==""): 
        text=text_area.get(1.0, END)
        sourcePath=filedialog.askdirectory()
        sourcePath=sourcePath+"/text.mp3"
    else: 
        sourcePath=destPath()

    gender=gender_combobox.get()
    speed=speed_combobox.get()
    voices = speaker.getProperty('voices')

    if(gender=='Male'): speaker.setProperty('voice',voices[0].id)
    else: speaker.setProperty('voice', voices[1].id)

    if(speed=="Fast"): speaker.setProperty('rate',250)
    elif(speed=="Normal"): speaker.setProperty('rate', 150)
    else: speaker.setProperty('rate', 60)
    
    speaker.save_to_file(text,sourcePath)
    speaker.runAndWait()
    saveText=""
    sourcePath=""
    text=""


'''set Source Path of the file'''
def setSourcePath():
    global sourcePath
    global text
    global saveText
    sourcePath=filedialog.askopenfilename()
    text=getText()
    text_area.delete(1.0,"end")
    text_area.insert(1.0,text)
    saveText=text
    text=""





'''==========================================================================================================='''
'''---------------------------------------------App Layout----------------------------------------------------'''
'''___________________________________________________________________________________________________________'''

root=Tk()
root.title("IMG/PDF/TXT to Audiobook")
root.geometry("768x500")
root.resizable(False,False)
root.configure(bg="#292929")

#icon
image_icon=PhotoImage(file="bin/speaker logo.png")
root.iconphoto(False,image_icon)

#Top Frame
Top_frame=Frame(root,bg="#D7D7D7",width=999,height=100)
Top_frame.place(x=0,y=0)

#Mike Logo
Logo=PhotoImage(file="bin/speaker logo.png")
Label(Top_frame,image=Logo,bg="#D7D7D7").place(x=14,y=7)

#Main header/Title
Label(Top_frame,text="Speech",font="arial 25 bold", bg="#DCDCDC", fg="black").place(x=115,y=32)
Label(Top_frame,text="ify",font="arial 25 bold", bg="#DCDCDC", fg="#FF6D3F").place(x=234,y=32)

#White TextBox
text_area=Text(root,font="Robote 20", bg="white",relief=GROOVE,wrap=WORD)
text_area.place(x=19,y=119,width=500,height=250)

#Voice Selector
Label(root,text="VOICE",font="arial 15 bold",bg='#292929',fg="white").place(x=599,y=120)
#Voice Combobox
gender_combobox=Combobox(root,values=['Male','Female'],font="arial 14",state='r',width=10)
gender_combobox.place(x =569,y=160)
gender_combobox.set('Male')

#Speed Selector
Label(root,text="SPEED",font="arial 15 bold",bg='#292929',fg="white").place(x=597,y=220)
#Speed Combobox
speed_combobox=Combobox(root,values=['Fast', 'Normal', 'Slow'],font="arial 14",state='r',width=10)
speed_combobox.place(x=569,y=260)
speed_combobox.set('Normal')

#Speak button
imageicon=PhotoImage(file="bin/speak.png")
btn=Button(root,text="Speak",compound=LEFT,image=imageicon,width=130,bg="#ffeed7",font="arial 14 bold",command=say)
btn.place(x=50,y=400)

#Save button
imageicon2=PhotoImage(file="bin/download.png")
save=Button(root,text="Save",compound=LEFT,image=imageicon2,width=130,bg="#39c790",font="arial 14 bold",command=save)#a6eda8
save.place(x=350,y=400)

#Choose file
b1=tk.Button(root,text=' Choose file ',font="bold",command=lambda:setSourcePath(),bg='skyblue')#SKYBLUE #FFD580
b1.grid(row=0,column=0,padx=9,pady=18)
b1.place(x=574,y=338)

#From pg_no
Label(root,text="From :",font="arial 11 bold",bg='#292929',fg="white").place(x=599,y=420)
fromTxt=Text(root,font="Robote 9 bold", bg="#a7a7a7",fg="black",relief=GROOVE,wrap=WORD)#babaff
fromTxt.place(x=655,y=419,width=27,height=19)

#To pg_no
Label(root,text="To      :",font="arial 11 bold",bg='#292929',fg="white").place(x=599,y=457)
toTxt=Text(root,font="Robote 9 bold", bg="#a7a7a7",fg="black",relief=GROOVE,wrap=WORD)
toTxt.place(x=655,y=457,width=27,height=19)

root.mainloop()

'''-------------------------------------------------App Layout----------------------------------------------'''
# pyinstaller -w -F -i ".\icon.png" .\Speechify.py