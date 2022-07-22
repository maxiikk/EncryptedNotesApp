from Encryptor import AES_Encryption
from tkinter import *
import os.path
from tkinter import ttk
import random
import struct
import pyperclip as clip

master = Tk() 
master.title("Encrypted Notes App v1.0") 
master.geometry("410x550") 
menu = Menu(master) 
master.config(menu = menu, bg='#bdbdbd') 
master.resizable(width=False, height=False)
mypassword = StringVar() 
passwordentered = IntVar() 
passwarningopen = IntVar()
setpassopen = IntVar()
openednotename = StringVar()
openednotename.set("NULL")
successfullydecrypted = IntVar()
reencryptionpassword = StringVar()
menu = Menu(master) 
master.config(menu = menu, bg='#bdbdbd') 
tools = Menu(menu, tearoff = 0)
menu.add_cascade(label = "Tools", menu = tools)
def shorten(text, tolen):
    l = ""
    for a in range(tolen):
        l += text[a]
    l += "..."
    return l
def encrypt(k):
    cipher = AES_Encryption(key=mypassword.get(), iv = 'dsfgsjklcvb45eso') 
    enc = cipher.encrypt(k) 
    enc = str(enc) 
    l = "" 
    o = 0 
    for b in enc: 
        if o != 0 and o != 1 and o != (len(enc)-1):
            l += b
        o += 1
    return l

def decrypt(todec): 
    todec = todec.encode().decode('unicode_escape').encode("raw_unicode_escape")
    def remove_bytes(buffer, start, end): 
        fmt = '%ds %dx %ds' % (start, end-start, len(buffer)-end)
        return b''.join(struct.unpack(fmt, buffer))
    todec = remove_bytes(todec, (len(todec)-1), (len(todec)))
    cipher = AES_Encryption(key=mypassword.get(), iv = 'dsfgsjklcvb45eso')
    decr = cipher.decrypt(todec)
    decr = str(decr)
    return decr

def setpasswarning():
    passerror = Toplevel(master) 
    passerrorlabel = StringVar() 
    passerror.config(bg='#bdbdbd') 
    passerror.geometry("300x100")
    passwarningopen.set(1)
    def warnclose(): 
        passwarningopen.set(0) 
        passerror.destroy() 
    passerror.protocol("WM_DELETE_WINDOW", warnclose) 
    passerror.resizable(width=False, height=False) 
    passerrorlabel.set("Set a password first!")
    passerror.title("Password Error")
    blanklabel = Label(passerror, text = " ", bg='#bdbdbd').grid(row = 0)
    errlabel = Label(passerror, text = passerrorlabel.get(), bg='#bdbdbd', font=("Courier", 16, "bold")).grid(row = 1) 

def setpassword(mode = 0):
    setapass = Toplevel(master)
    mainframe = Frame(setapass, bg='#bdbdbd')
    mainframe.grid(row = 0)
    e = Entry(mainframe) 
    e2 = Entry(mainframe) 
    setpasslabel = StringVar() 
    confirmpasslabel = StringVar() 
    setpassbuttonlabel = StringVar() 
    setapass.config(bg='#bdbdbd') 
    def passclose(): 
        setpassopen.set(0) 
        setapass.destroy() 
    setapass.protocol("WM_DELETE_WINDOW", passclose)
    setapass.resizable(width=False, height=False)
    setpassopen.set(1) 
    warninglabel = StringVar() 
    warninglabel.set("")
    changepassmode = IntVar()
    changepassmode.set(mode)
    def complete():
        if len(e.get()) != 0 and len(e2.get()) != 0: 
            if e.get() == e2.get():
                mypassword.set(e.get()) 
                passwordentered.set(1)
                setpassopen.set(0)
                setapass.destroy() 
            else: 
                warninglabel.set("The two passwords are not equal!")
        else:
            warninglabel.set("Password fields shouldn't be empty!")
    def completeonevent(event):
        complete()
    setapass.bind('<Return>', completeonevent)
    setpasslabel.set("Set a password:")
    setpassbuttonlabel.set("Set password")
    setapass.title("Set A Password First!")
    confirmpasslabel.set("Confirm Password:")
    setapass.geometry("550x110")
    blanklabel = Label(mainframe, text = " ", bg='#bdbdbd').grid(row = 0) 
    warnlabel = Label(setapass, textvariable = warninglabel, bg='#bdbdbd', fg = "red").grid(row = 3, stick = W)
    label = Label(mainframe, text = setpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 1, stick = W)
    label = Label(mainframe, text = confirmpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 2, stick = W)
    e.grid(row = 1, column = 1, stick = W) 
    e2.grid(row = 2, column = 1, stick = W) 
    e2.config(show="*") 
    e.config(show="*") 
    blanklabel = Label(mainframe, text = "    ", bg='#bdbdbd').grid(row = 1, column = 2, stick = W) #>>>>
    setpass = Button(mainframe, text = setpassbuttonlabel.get(), command = complete, width = 15, bg='lightgrey', borderwidth = 5, font=("Arial", 10, "bold")).grid(row = 2, column = 3, stick = W) 

setpassword()

def areyousure(mode = 0, setapass = 0):
    areyousure = Toplevel(master)
    areyousure.config(bg='#bdbdbd')
    areyousure.resizable(width=False, height=False)
    label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 0, column = 0, stick = W)
    label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 1, column = 0, stick = W)
    yesbuttonlabel = StringVar()
    nobuttonlabel = StringVar()
    def finish():
        if mode == 0:
            savenotesfile()
        elif mode == 1:
            createnote(txtfilename.get())
        elif mode == 2:
            encryptwithotherpassword(setapass)
        areyousure.destroy()
    areyousure.title("Are you sure?")
    if mode == 2:
        label = Label(areyousure, text = "Are you sure that you want to re-encrypt the note?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
    else:
        label = Label(areyousure, text = "Are you sure that you want to save the note?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
    yesbuttonlabel.set("Yes")
    nobuttonlabel.set("NO")
    def finish2(event):
        finish()
    areyousure.bind('<Return>', finish2)
    areyousure.bind('<space>', finish2)
    yes = Button(areyousure, text = yesbuttonlabel.get(), command = finish, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 2, stick = W) 
    no = Button(areyousure, text = nobuttonlabel.get(), command = areyousure.destroy, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 0, stick = W) 

def changepassword():
    setapass = Toplevel(master) 
    mainframe = Frame(setapass, bg='#bdbdbd')
    mainframe.grid(row = 0)
    e = Entry(mainframe) 
    e2 = Entry(mainframe) 
    setpasslabel = StringVar() 
    confirmpasslabel = StringVar() 
    setpassbuttonlabel = StringVar() 
    setapass.config(bg='#bdbdbd') 
    def passclose():
        setpassopen.set(0) 
        setapass.destroy() 
    setapass.protocol("WM_DELETE_WINDOW", passclose) 
    setapass.resizable(width=False, height=False) 
    setpassopen.set(1) 
    warninglabel = StringVar() 
    warninglabel.set("") 
    varactive = IntVar()
    varactive.set(0)
    def areyousure2(): 
        varactive.set(1)
        areyousure = Toplevel(master)
        areyousure.config(bg='#bdbdbd')
        areyousure.resizable(width=False, height=False)
        label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 0, column = 0, stick = W)
        label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 1, column = 0, stick = W)
        yesbuttonlabel = StringVar()
        def passclose():
            setpassopen.set(0) 
            varactive.set(0)
            setapass.destroy() 
        areyousure.protocol("WM_DELETE_WINDOW", passclose) 
        nobuttonlabel = StringVar()
        def finish():
            complete()
            areyousure.destroy()
        areyousure.title("Are you sure?")
        label = Label(areyousure, text = "Are you sure that you want to change the password?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
        yesbuttonlabel.set("Yes")
        nobuttonlabel.set("NO")
        def finish2(event):
            finish()
        areyousure.bind('<Return>', finish2)
        areyousure.bind('<space>', finish2)
        yes = Button(areyousure, text = yesbuttonlabel.get(), command = finish, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 2, stick = W) 
        no = Button(areyousure, text = nobuttonlabel.get(), command = areyousure.destroy, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 0, stick = W) 
    def complete():
        def areyousure2():
            savenotesfile()
            opennote(txtfilename.get())
        if len(e.get()) != 0 and len(e2.get()) != 0: 
            if e.get() == e2.get(): 
                mypassword.set(e.get()) 
                passwordentered.set(1)
                setpassopen.set(0) 
                areyousure2()
                setapass.destroy() 
            else: 
                warninglabel.set("The two passwords are not equal!")
        else: 
            warninglabel.set("Password fields shouldn't be empty!")
    def areyousure3(event):
        if varactive.get() != 1:
            areyousure2()
    setapass.bind('<Return>', areyousure3)
    setpasslabel.set("Set the new password:")
    setpassbuttonlabel.set("Change password")
    setapass.title("Set A New Password")
    confirmpasslabel.set("Confirm Password:")
    setapass.geometry("550x110")
    blanklabel = Label(mainframe, text = " ", bg='#bdbdbd').grid(row = 0) 
    warnlabel = Label(setapass, textvariable = warninglabel, bg='#bdbdbd', fg = "red").grid(row = 3, stick = W)
    label = Label(mainframe, text = setpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 1, stick = W)
    label = Label(mainframe, text = confirmpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 2, stick = W)
    e.grid(row = 1, column = 1, stick = W) 
    e2.grid(row = 2, column = 1, stick = W) 
    e2.config(show="*") 
    e.config(show="*") 
    blanklabel = Label(mainframe, text = "    ", bg='#bdbdbd').grid(row = 1, column = 2, stick = W) 
    setpass = Button(mainframe, text = setpassbuttonlabel.get(), command = areyousure2, width = 15, bg='lightgrey', borderwidth = 5, font=("Arial", 10, "bold")).grid(row = 2, column = 3, stick = W) 
        
def savenotesfile(): 
    if passwordentered.get() == 1: 
        if len(txtfilename.get()) > 0:
            if os.path.isfile(txtfilename.get() + ".txt"): 
                contents = open((txtfilename.get() + ".txt"), "r+")
                lines2 = contents.readlines()
                notetext.delete ("1.0" , "end")
                donttrunc = 0
                for line in lines2:
                    try:
                        k = decrypt(line)
                        notetext.insert (INSERT, k +"\n")
                    except:
                        donttrunc = 1
                        warningtextbox.delete("1.0", "end")
                        warningtextbox.insert(INSERT, "Wrong Password")
                contents.close()
                sfile = open((txtfilename.get() + ".txt"), "r+")
                if donttrunc != 1:
                    sfile.truncate(0)
                    notes = str(notetext.get("1.0", "end"))
                    for line in notes.splitlines():
                        try:
                            l = encrypt(line)
                            sfile.write(str(l) + "\n")
                        except:
                            warningtextbox.delete("1.0", "end")
                            warningtextbox.insert(INSERT, "Cant Encrypt")
                sfile.close()
    elif passwordentered.get() != 1 and setpassopen.get() != 1:
        if passwarningopen.get() == 0:
            setpasswarning()
        setpassword()
    elif passwordentered.get() != 1 and setpassopen.get() == 1: 
        if passwarningopen.get() == 0:
           setpasswarning()

def createnote(txtname):
    if passwordentered.get() == 1 and len(txtname) > 0 and txtname != "NULL" and txtname != "NULL.txt":
        filename = (txtname + ".txt")
        notefile = open(str(filename), 'w+')
        lines = notetext.get("1.0", "end")
        for line in lines.splitlines():
            try:
                k = encrypt(line)
                notefile.write(k +"\n")
                successfullydecrypted.set(1)
                analyzetext()
                warningtextbox.delete("1.0", "end")
                openednotename.set(txtfilename.get())
            except:
                successfullydecrypted.set(0)
                warningtextbox.delete("1.0", "end")
                warningtextbox.insert(INSERT, "Couldnt Encrypt")
        notefile.close()
    elif txtname == "NULL" or txtname == "NULL.txt":
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Name cannot be NULL")
    else:
        if passwarningopen.get() != 1:
            setpasswarning()
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Set a password")
def analyzetext():
    if successfullydecrypted.get() == 1:
        linecount = 0
        charcount = 0
        lines = notetext.get("1.0", "end")
        for line in lines.splitlines():
            linecount += 1
            for a in line:
                charcount += 1
        textanalytics.set(f"Character Count: {str(charcount)}\nLine Count: {str(linecount)}")
def opennote(txtname, mode = 0):
    notetext.delete("1.0", "end")
    if mode == 1:
        txtfilename.delete(0, END)
        txtfilename.insert(INSERT, txtname)
    filename = str(txtname + ".txt")
    print(filename)
    if os.path.isfile(filename):
        if passwordentered.get() == 1:
            notefile = open(filename, "r+")
            lines = notefile.readlines()
            notefile.close()
            empty = 0
            i = 0
            linecount = 0
            for line in lines:
                linecount += 1
            for line in lines:
                i += 1
                try:
                    k = decrypt(line)
                    if empty >= 2 and k == "":
                        notetext.insert (INSERT, k)
                    elif k == "":
                        notetext.insert (INSERT, k + "\n")
                        empty += 1
                    elif linecount != i:
                        notetext.insert (INSERT, k + "\n")
                        empty = 0
                    else:
                        notetext.insert (INSERT, k)
                    successfullydecrypted.set(1)
                    openednotename.set(txtfilename.get())
                except:
                    successfullydecrypted.set(0)
                    warningtextbox.delete("1.0", "end")
                    warningtextbox.insert(INSERT, "Wrong Password")
                    break
                warningtextbox.delete("1.0", "end")
                analyzetext()
        else:
            warningtextbox.delete("1.0" , "end")
            warningtextbox.insert(INSERT, "Set a password")
            if passwarningopen.get() != 1:
                setpasswarning()
    else:
        warningtextbox.delete("1.0" , "end")
        warningtextbox.insert(INSERT, "Doesnt Exist")

def failedwin():
    failed = Toplevel(master)
    failed.title("FAILED!")
    failed.resizable(width = False, height = False)
    failed.config(bg='#bdbdbd')
    failed.geometry("200x50")
    Label(failed, text = "        ", bg='#bdbdbd').grid(row = 0)
    Label(failed, text = "           FAILED!", fg = "red", font = ("bold", 14), bg='#bdbdbd').grid(row = 1)
    Label(failed, text = "        ", bg='#bdbdbd').grid(row = 2)

def successwin(text):
    success = Toplevel(master)
    success.title("SUCCESS!")
    success.resizable(width = False, height = False)
    success.geometry("250x100")
    success.config(bg='#bdbdbd')
    Label(success, text = "        ", bg='#bdbdbd').grid(row = 0)
    Label(success, text = ("          " + text +"!"), fg = "green", font = ("bold", 14), bg='#bdbdbd').grid(row = 1)
    Label(success, text = "        ", bg='#bdbdbd').grid(row = 2)

def separatewith():
    separatewindow = Toplevel(master)
    separatewindow.title("Note separation")
    separatewindow.resizable(width = False, height = False)
    separatewindow.config(bg='#bdbdbd')
    separatewindow.geometry("320x150")
    mainframe = Frame(separatewindow, bg='#bdbdbd')
    mainframe.grid(row = 0)
    secframe = Frame(separatewindow, bg='#bdbdbd')
    secframe.grid(row = 1)
    errorlabel = StringVar()
    errorlabel.set("")
    Label(mainframe, text = "Separator: ", font = ("italic", 10), bg='#bdbdbd').grid(row = 0, column = 0, stick = E)
    Label(secframe, text = "Place the separator at the end of the note as well!\nThe separated note will have the current note's \nname and a number of the part at the end", bg='#bdbdbd').grid(row = 5, column= 0, stick = W)
    Label(separatewindow, text = "   ", bg='#bdbdbd').grid(row = 1, column = 2, stick = W)
    sep = Entry(mainframe, bg='lightgrey')
    sep.grid(row = 0, column = 1, stick = W)
    sepbyline = IntVar()
    def checked():
        if sepbyline.get() == 1:
            sep['state'] = DISABLED
        else:
            sep['state'] = NORMAL
    Checkbutton(mainframe, text = "Separate by line", variable = sepbyline, bg='#bdbdbd', command = checked).grid(row = 1, column = 1, stick = W)
    def close():
        separatewindow.destroy()
    def startseparation():
        if successfullydecrypted.get() == 1:
            if len(sep.get()) == 0 and sepbyline.get() != 1:
                errorlabel.set("Provide a separator!")
                return
            sepval = sep.get()
            nameofnote = openednotename.get()
            lines = notetext.get("1.0", "end")
            temp = ""
            i = 1
            opened = 0
            for line in lines.splitlines():
                if sepbyline.get() == 1:
                    try:
                        sepnote = open(nameofnote + str(i) + ".txt", "w")
                        opened = 1
                    except:
                        opened = 0
                        errorlabel.set("Cannot create the separated notes")
                        break
                    errorlabel.set("")
                    temp2 = str(encrypt(line))
                    sepnote.write(temp2 + "\n")
                    temp = ""
                    i += 1
                    if opened == 1:
                        sepnote.close()
                else:
                    if line == sepval:
                        try:
                            sepnote = open(nameofnote + str(i) + ".txt", "w")
                            opened = 1
                        except:
                            opened = 0
                            errorlabel.set("Cannot create the separated notes")
                            break
                        errorlabel.set("")
                        temp2 = str(encrypt(temp))
                        sepnote.write(temp2 + "\n")
                        temp = ""
                        i += 1
                        if opened == 1:
                            sepnote.close()
                    else:
                        temp += line + "\n"
            if opened == 1:
                successwin("SUCCESS")
            else:
                failedwin()
            close()
        else:
            errorlabel.set("Decrypt a note first!")
    Label(mainframe, text = "  ", bg='#bdbdbd').grid(row = 0, column = 2, stick = W)
    separatenote = Button(mainframe, text = "Separate the note", font = ("bold", 10), command = startseparation).grid(row = 0, column = 3, stick = W)
    Label(secframe, textvariable = errorlabel, fg = "red", bg='#bdbdbd').grid(row = 2, column = 0, stick = W)
def listmyfiles(mode = 0):
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".txt")]
    if mode == 1:
        l = ""
        for f in files:
            l += f + "\n"
        return l
    return files
def opennoteslist():
    noteswindow = Toplevel(master)
    noteswindow.title("Notes")
    noteswindow.resizable(height = False, width = False)
    noteswindow.config(bg='#bdbdbd')
    noteswindow.geometry("410x300")
    mainframe = Frame(noteswindow)
    mainframe.grid(row=0, stick = W)
    mainframe.config(bg='#bdbdbd')
    firstframe = Frame(noteswindow)
    firstframe.config(bg='#bdbdbd')
    firstframe.grid(row = 1)
    canvas = Canvas(firstframe, bg='#bdbdbd')
    canvas.grid(row=0, column=0, sticky="news")
    scrollbar = Scrollbar(firstframe, orient='vertical', command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky = NS)
    canvas['yscrollcommand'] = scrollbar.set
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
    frame_buttons = Frame(canvas, bg='#bdbdbd')
    canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
    def scrolllistbox(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    noteswindow.bind("<MouseWheel>", scrolllistbox)
    def listthem():
        files = listmyfiles()
        i = 0
        for f in files:
            text = str(f).removesuffix('.txt')
            text2 = text
            if len(text) > 45:
                text2 = shorten(text, 45)
            Label(frame_buttons, text = "      ", bg='#bdbdbd').grid(row = i, column = 0, stick = E)
            Label(frame_buttons, text = text2, bg='#bdbdbd').grid(row = i, column = 1, stick = E)
            Label(frame_buttons, text = "       ", bg='#bdbdbd').grid(row = i, column = 2, stick = E)
            Button(frame_buttons, text = "    Open   ", command = lambda text2 = text: opennote(text2, 1)).grid(row = i, column = 3, sticky = E)
            i += 1
    refreshbutton = Button(mainframe, text = "Refresh", width=20, height=1, command=listthem, bg='#bdbdbd').grid(row = 0, stick = W)
    listthem()
def searchinfiles():
    noteswindow = Toplevel(master)
    noteswindow.title("Search")
    noteswindow.resizable(height = False, width = False)
    noteswindow.config(bg='#bdbdbd')
    noteswindow.geometry("410x300")
    mainframe = Frame(noteswindow)
    mainframe.grid(row=0, stick = W)
    mainframe.config(bg='#bdbdbd')
    def scrolllistbox(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    noteswindow.bind("<MouseWheel>", scrolllistbox)
    def searchtext(texttosearch):
        mainframe = Frame(noteswindow)
        mainframe.grid(row=0, stick = W)
        mainframe.config(bg='#bdbdbd')
        firstframe = Frame(noteswindow)
        firstframe.config(bg='#bdbdbd')
        firstframe.grid(row = 1, stick = W)
        canvas = Canvas(firstframe, bg='#bdbdbd')
        def scrolllistbox(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.grid(row=0, column=0, sticky="news")
        scrollbar = Scrollbar(firstframe, orient='vertical', command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky = NS)
        canvas['yscrollcommand'] = scrollbar.set
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
        frame_buttons = Frame(canvas, bg='#bdbdbd')
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
        noteswindow.bind("<MouseWheel>", scrolllistbox)
        if passwordentered.get() != 1:
            if passwarningopen.get() != 1:
                setpasswarning()
            warningtextbox.delete("1.0", "end")
            warningtextbox.insert(INSERT, "Set a password")
            return
        if len(texttosearch) <= 0:
            warningtextbox.delete("1.0", "end")
            warningtextbox.insert(INSERT, "Enter text to search for!")
            return
        files = listmyfiles()
        i = 0
        for f in files:
            try:
                temp = open(f, "r")
                lines = temp.readlines()
                temp.close()
                for line in lines:
                    try:
                        line = decrypt(line)
                        if texttosearch in line:
                            text = str(f).removesuffix('.txt')
                            text2 = text
                            if len(text) > 45:
                                text2 = shorten(text, 45)
                            Label(frame_buttons, text = "      ", bg='#bdbdbd').grid(row = i, column = 0, stick = E)
                            Label(frame_buttons, text = text2, bg='#bdbdbd').grid(row = i, column = 1, stick = E)
                            Label(frame_buttons, text = "       ", bg='#bdbdbd').grid(row = i, column = 2, stick = E)
                            Button(frame_buttons, text = "    Open   ", command = lambda text2 = text: opennote(text2, 1)).grid(row = i, column = 3, sticky = E)
                            i += 1
                            break
                    except:
                        warningtextbox.delete("1.0", "end")
                        warningtextbox.insert(INSERT, "Error!")
            except:
                warningtextbox.delete("1.0", "end")
                warningtextbox.insert(INSERT, "Error!")
    Label(mainframe, text = "Search:   ", bg='#bdbdbd').grid(row = 0, column = 0)
    texttosearchfor = Entry(mainframe, width = 40)
    texttosearchfor.grid(row = 0, column = 1)
    searchbutton = Button(mainframe, text = "Seach", width = 15, height = 1, command= lambda: searchtext(texttosearchfor.get()), bg='#bdbdbd').grid(row = 0, column = 2)

def exportdecrypted():
    if passwordentered.get() == 1 and successfullydecrypted.get() == 1:
        sourcefile = open(openednotename.get() + ".txt", "r+")
        lines = sourcefile.readlines()
        sourcefile.close()
        filetoexportto = open(openednotename.get() + "_decrypted.txt", "w+")
        empty = 0
        failure = 0
        for line in lines:
            try:
                k = decrypt(line)
                if empty >= 2 and k == "":
                    filetoexportto.write(k)
                elif k == "":
                    filetoexportto.write(k + "\n")
                    empty += 1
                else:
                    filetoexportto.write(k + "\n")
                    empty = 0
            except:
                warningtextbox.delete("1.0", "end")
                warningtextbox.insert(INSERT, "Wrong password!")
                failure = 1
                break
        text = openednotename.get()
        text2 = text
        if len(text) > 10:
            text2 = shorten(text, 10)
        if failure == 0: successwin("EXPORTED" + "\n" + text2 + "_decrypted.txt")
        filetoexportto.close()
    elif passwordentered.get() == 0:
        setpasswarning()
    elif successfullydecrypted.get() != 1:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Decrypt a note first!")
    else:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Error")

def checkdec(filename):
    if passwordentered.get() != 1:
        return
    tempfile = open(filename, "r")
    lines = tempfile.readlines()
    tempfile.close()
    decrypted = 0
    while 1:
        try:
            for line in lines:
                temp = decrypt(line)
        except:
            break
        decrypted = 1
        break
    return decrypted

def mergenotes():
    mergewindow = Toplevel(master)
    mergewindow.title("Note merge")
    mergewindow.resizable(width = False, height = False)
    mergewindow.config(bg='#bdbdbd')
    mergewindow.geometry("400x400")
    mainframe = Frame(mergewindow, bg='#bdbdbd')
    mainframe.grid(row = 0)
    errorlabel = StringVar()
    errorlabel.set("")
    #Label(mainframe, text = "  ", bg='#bdbdbd').grid(row = 0, stick = W)
    Label(mainframe, text = "Name of note to merge into: ", bg='#bdbdbd', font = ("Arial", 10, "bold")).grid(row = 0, column = 0, stick = W)
    notenametomergeinto = Entry(mainframe, bg='lightgrey')
    notenametomergeinto.grid(row = 0, column = 1, stick = W)
    Label(mergewindow, text = "Notes to merge separated by line:", bg='#bdbdbd', font = ("Arial", 10, "bold")).grid(row = 2, stick = W)
    notestomerge = Text(mergewindow, bg='lightgrey', height = 10, width = 20)
    notestomerge.grid(row = 3, column = 0, stick = W)
    cantopen = StringVar()
    filesdontexist = StringVar()
    cantdecrypt = StringVar()
    cantopen.set("Cannot open file: ")
    filesdontexist.set("Files that dont exist: ")
    cantdecrypt.set("Files that cannot be decrypted: ")
    totalfiles = IntVar()
    def startmerge():
        totalfiles.set(0)
        filename = ""
        cantopen.set("Cannot open file: ")
        filesdontexist.set("Files that dont exist: ")
        cantdecrypt.set("Files that cannot be decrypted: ")
        errors = 0
        openedmain = 0
        if passwordentered.get() != 1:
            errorlabel.set("NO PASSWORD PROVIDED!")
            setpasswarning()
            setpassword()
            return
        if len(notenametomergeinto.get()) == 0:
            errorlabel.set("ENTER A NAME FOR THE FILE TO MERGE INTO!")
            return
        if ".txt" in notenametomergeinto.get():
            mergeinto = (notenametomergeinto.get()).replace("\n","")
            try:
                mainfile = open(mergeinto, "w+")
                openedmain = 1
            except:
                openedmain = 0
                errorlabel.set("Error while opening the main note")
                return
        else:
            try:
                mainfile = open((notenametomergeinto.get() + ".txt"), "w+")
                openedmain = 1
            except:
                openedmain = 0
                errorlabel.set("Error while opening the main file")
                return
        lines = notestomerge.get("1.0", "end")
        opened = 0
        for line in lines.splitlines():
            totalfiles.set(totalfiles.get()+1)
            if ".txt" in line:
                filename = line.replace("\n", "")
            else:
                filename = line.replace("\n", "") + ".txt"
            if os.path.isfile(filename):
                try:
                    if checkdec(filename) == 1:
                        tempfile = open(filename, "r")
                        opened = 1
                        lines2 = tempfile.readlines()
                        for line2 in lines2:
                            mainfile.write(line2)
                        tempfile.close()
                    else:
                        errorlabel.set("Cannot decrypt " + filename)
                        cantdecrypt.set(cantdecrypt.get() + filename + " ")
                        opened = 0
                        errors += 1
                except:
                    errorlabel.set("Cannot open file " + filename)
                    cantopen.set((cantopen.get() + filename + " "))
                    opened = 0
                    errors += 1
            else:
                errorlabel.set("No such note as " + filename)
                filesdontexist.set((filesdontexist.get() + filename + " "))
                errors += 1
        if openedmain == 1 and opened == 1 and errors == 0:
            mainfile.close()
            successwin("SUCCESS")
        elif openedmain == 1 and (errors > 0 and errors < totalfiles.get()):
            mainfile.close()
            successwin("SUCCESS WITH A\nFEW ERRORS")
        elif openedmain == 1 and errors == totalfiles.get():
            mainfile.close()
            failedwin()
    Button(mainframe, text = "Merge", command = startmerge, width = 10, font = ("bold", 10)).grid(row = 0, column = 2, stick = W)
    Label(mergewindow, textvariable = filesdontexist, bg='#bdbdbd').grid(row = 5, stick = W)
    Label(mergewindow, textvariable = cantopen, bg='#bdbdbd').grid(row = 6, stick = W)
    Label(mergewindow, textvariable = cantdecrypt, bg='#bdbdbd').grid(row = 7, stick = W)
    Label(mergewindow, textvariable = errorlabel, fg = "red", bg='#bdbdbd').grid(row = 4, stick = W)

tools.add_command(label = "Export Decrypted Note", command = exportdecrypted)
tools.add_command(label = "Separate note", command = separatewith)
tools.add_command(label = "Merge notes", command = mergenotes)
menu.add_command(label = "Notes", command = opennoteslist)
menu.add_command(label = "Search", command = searchinfiles)

def reencrypt(k):
    cipher = AES_Encryption(key=reencryptionpassword.get(), iv = 'dsfgsjklcvb45eso')
    enc = cipher.encrypt(k) 
    enc = str(enc) 
    l = "" 
    o = 0 
    for b in enc: 
        if o != 0 and o != 1 and o != (len(enc)-1):
            l += b
        o += 1
    return l

def encryptwithotherpassword(setapass):
    if successfullydecrypted.get() == 1:
        linestoreencrypt = notetext.get("1.0", "end")
        linestoreencrypt = linestoreencrypt.splitlines()
        notefile = open(openednotename.get() + ".txt", 'w')
        notefile.truncate(0)
        for line in linestoreencrypt:
            k = reencrypt(line)
            notefile.write(k + "\n")
            warningtextbox.delete("1.0", "end")
        notefile.close()
        setapass.destroy()
        opennote(txtfilename.get())
    else:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "None Successfully Opened Notes") 

def newpassword(mode = 0):
    setapass = Toplevel(master) 
    e = Entry(setapass) 
    e2 = Entry(setapass) 
    setpasslabel = StringVar() 
    confirmpasslabel = StringVar() 
    setpassbuttonlabel = StringVar() 
    setapass.config(bg='#bdbdbd') 
    def passclose(): 
        setpassopen.set(0) 
        setapass.destroy() 
    setapass.protocol("WM_DELETE_WINDOW", passclose)
    setapass.resizable(width=False, height=False)
    setpassopen.set(1) 
    warninglabel = StringVar() 
    warninglabel.set("")
    changepassmode = IntVar()
    changepassmode.set(mode)
    if successfullydecrypted.get() == 0:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Decrypt A Note First")
        setapass.destroy()
    def complete():
        if len(e.get()) != 0 and len(e2.get()) != 0: 
            if e.get() == e2.get():
                areyousure(2, setapass)
                reencryptionpassword.set(e.get())
                setpassopen.set(0)
            else: 
                warninglabel.set("The two passwords are not equal!")
        else:
            warninglabel.set("Password fields shouldn't be empty!")
    def completeonevent(event):
        complete()
    setapass.bind('<Return>', completeonevent)
    setpasslabel.set("Set the new password of this note:")
    setpassbuttonlabel.set("Re-Encrypt")
    setapass.title("Re-Encryption")
    confirmpasslabel.set("Confirm Password:")
    setapass.geometry("550x110")
    blanklabel = Label(setapass, text = " ", bg='#bdbdbd').grid(row = 0) 
    warnlabel = Label(setapass, textvariable = warninglabel, bg='#bdbdbd', fg = "red").grid(row = 3, stick = W)
    label = Label(setapass, text = setpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 1, stick = W)
    label = Label(setapass, text = confirmpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 2, stick = W)
    e.grid(row = 1, column = 1, stick = W) 
    e2.grid(row = 2, column = 1, stick = W) 
    e2.config(show="*") 
    e.config(show="*") 
    blanklabel = Label(setapass, text = "    ", bg='#bdbdbd').grid(row = 1, column = 2, stick = W) #>>>>
    setpass = Button(setapass, text = setpassbuttonlabel.get(), command = complete, width = 15, bg='lightgrey', borderwidth = 5, font=("Arial", 10, "bold")).grid(row = 2, column = 3, stick = W) 

def copytoclipboard():
    if successfullydecrypted.get() == 1:
        clip.copy(notetext.get("1.0", "end"))
    else:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Decrypt A Note First")

def opennote2(event):
    opennote(str(txtfilename.get()))

firstframe = Frame(master, bg='#bdbdbd')
firstframe.grid(row = 0, column = 0)
secondframe = Frame(master, bg='#bdbdbd')
secondframe.grid(row = 1, column = 0)
thirdframe = Frame(master, bg='#bdbdbd')
thirdframe.grid(row = 2, column = 0)
notetext = Text(secondframe, width = 50, borderwidth = 2, bg='lightgrey', height = 22)
notetext.grid(row = 3, column = 1)
textanalytics = StringVar()
textanalytics.set("Character Count: N/A\nLine Count: N/A")
txtfilename = Entry(firstframe, width = 20, borderwidth = 2, bg='lightgrey')
txtfilename.grid(row = 0, column = 1, stick = W)
opennotebutton = Button(firstframe, text = "     Open the note         ", command = lambda:opennote(str(txtfilename.get()))).grid(row = 1, column = 1, stick = W)
createnotebutton = Button(firstframe, text = "Create/Save the note", command = lambda: areyousure(1)).grid(row = 1, column = 0, stick = E)
encryptwith = Button(firstframe, text = "Encrypt this note\nwith other password    ", command = newpassword).grid(row = 2, column = 1, stick = W)
changepass = Button(firstframe, text = "Change encryption/\ndecryption password", command = changepassword).grid(row = 2, column = 0, stick = E)
Label(firstframe, text = "Note name: ", bg='#bdbdbd').grid (row = 0, column = 0, stick = E)
cleartextbox = Button(secondframe, text = "               Clear               ", command = lambda: notetext.delete("1.0", "end")).grid(row = 4, column = 1, stick = E)
copytoclip = Button(thirdframe, text = "Copy note to clipboard", command = copytoclipboard).grid(row = 5, column = 0, stick = E)
warninglabel = Label(thirdframe, text = "Warnings: ", bg='#bdbdbd').grid(row = 5, column = 2, stick = S)
warningtextbox = Text(thirdframe, width = 20, borderwidth = 2, bg='lightgrey', height = 1, fg = "red")
warningtextbox.grid(row = 6, column = 2, stick = N)
textanalyticslabel = Label(thirdframe, textvariable = textanalytics, bg='#bdbdbd').grid(row = 6, column = 0, stick = E)
txtfilename.bind('<Return>', opennote2)
mainloop()







# Made by MaxiiKK at https://github.com/maxiikk/encryptednotesapp


"""
Needed modules for python to run this app:
    1. pycryptodome
    2. AES-Encryptor
    3. pyperclip





version = 1.0
"""