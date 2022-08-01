from Encryptor import AES_Encryption
from tkinter import *
import os.path
from tkinter import ttk
import random
import struct
import pyperclip as clip
from tkinter.filedialog import askopenfilename

master = Tk()
appwidth = 410
appheight = 550
appgeom = "410x550"
screenwidth = master.winfo_screenwidth()
screenheight = master.winfo_screenheight()
xx = (screenwidth/2) - (appwidth/2)
yy = (screenheight/2) - (appheight/2)
master.title("Encrypted Notes App v1.5 by MaxiiKK") 
master.geometry(f'{appwidth}x{appheight}+{int(xx-200)}+{int(yy)}')
menu = Menu(master) 
master.config(menu = menu, bg='#bdbdbd') 
master.resizable(width=False, height=False)
mypassword = StringVar() 
passwordentered = IntVar() 
passwarningopen = IntVar()
setpassopen = IntVar()
searchopen = IntVar()
noteslistopen = IntVar()
openednotename = StringVar()
openednotename.set("NULL")
successfullydecrypted = IntVar()
reencryptionpassword = StringVar()
checknotestoaddopen = IntVar()
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
    try:
        decr = cipher.decrypt(todec)
    except:
        return 1
    if str(decr) == "Failed To Decrypt String Please Check The Key And IV\nPlease Re-Verify The Given Data, Data May Be Changed\nData Bytes Must Be Multiple Of 16":
        return 1
    decr = str(decr)
    return decr

def setpasswarning():
    passerror = Toplevel(master) 
    passerrorlabel = StringVar() 
    passerror.config(bg='#bdbdbd') 
    passerror.geometry(f'{300}x{100}+{int(xx)}+{int(yy+140)}')
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
                warningtextbox.delete("1.0", "end")
                if txtfilename.get() != "":
                    notetext.focus_set()
                else:
                    txtfilename.focus_set()
                setpassopen.set(0)
                setapass.destroy() 
            else: 
                warninglabel.set("The two passwords are not equal!")
        else:
            warninglabel.set("Password fields shouldn't be empty!")
    def completeonevent(event):
        complete()
    setpasslabel.set("Set a password:")
    setpassbuttonlabel.set("Set password")
    setapass.title("Set A Password First!")
    confirmpasslabel.set("Confirm Password:")
    setapass.geometry(f'{550}x{110}+{int(xx-200)}+{int(yy-143)}')
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
    e.bind("<Return>", lambda event: e2.focus_set())
    e2.bind("<Return>", lambda event: complete())
    setapass.focus_set()
    e.focus_set()

setpassword()

def areyousure(mode = 0, setapass = 0, temptext = ""):
    areyousure = Toplevel(master)
    areyousure.focus_set()
    areyousure.config(bg='#bdbdbd')
    areyousure.resizable(width=False, height=False)
    label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 0, column = 0, stick = W)
    label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 1, column = 0, stick = W)
    yesbuttonlabel = StringVar()
    nobuttonlabel = StringVar()
    areyousure.geometry(f'{513}x{74}+{int(xx-200)}+{int(yy)}')
    def finish():
        if mode == 0:
            savenotesfile()
        elif mode == 1:
            createnote(txtfilename.get())
        elif mode == 2:
            encryptwithotherpassword(setapass)
        elif mode == 3:
            master.destroy()
        elif mode == 4:
            renamenote(openednotename.get(), temptext)
        areyousure.destroy()
    areyousure.title("Are you sure?")
    if mode == 2:
        label = Label(areyousure, text = "Are you sure that you want to re-encrypt the note?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
    elif mode == 3:
        label = Label(areyousure, text = "Are you sure that you want to close the app?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
    elif mode == 4:
        label = Label(areyousure, text = "Are you sure that you want to rename the note?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
    else:
        label = Label(areyousure, text = "Are you sure that you want to save the note?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
    yesbuttonlabel.set("Yes")
    nobuttonlabel.set("NO")
    def finish2(event):
        finish()
    areyousure.bind('<Return>', lambda event: finish2())
    areyousure.bind('<space>', lambda event: finish2())
    areyousure.bind("<Escape>", lambda event: passclose())
    yes = Button(areyousure, text = yesbuttonlabel.get(), command = finish, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 2, stick = W) 
    no = Button(areyousure, text = nobuttonlabel.get(), command = areyousure.destroy, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 0, stick = W) 
def renamenote(filename, newname):
    if not filename.endswith(".txt"):
        filename += ".txt"
    try:
        os.rename(filename, newname)
        successwin("Renamed to " + newname)
    except:
        failedwin()
        return
def renamenoteinit(filename, newname):
    if not filename.endswith(".txt"):
        filename += ".txt"
    if len(newname) == 0:
        failedwin()
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "No name to rename to")
        return
    if "_decrypted" in newname:
        failedwin()
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Name cannot contain _decrypted")
        return
    if os.path.isfile(filename) and successfullydecrypted.get() == 1:
        if newname.endswith(".txt"):
            if newname == filename:
                successwin("Same name as before")
            else:
                areyousure(mode = 4, temptext = newname)
        else:
            newname += ".txt"
            if newname == filename:
                successwin("Same name as before")
            else:
                areyousure(mode = 4, temptext = newname)
    else:
        failedwin()
        return
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
        areyousure.geometry(f'{513}x{74}+{int(xx-200)}+{int(yy)}')
        label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 0, column = 0, stick = W)
        label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 1, column = 0, stick = W)
        yesbuttonlabel = StringVar()
        def passclose():
            setpassopen.set(0) 
            varactive.set(0)
            areyousure.destroy() 
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
        areyousure.bind('<Return>', lambda event: finish2())
        areyousure.bind('<space>', lambda event: finish2())
        areyousure.bind("<Escape>", lambda event: passclose())
        yes = Button(areyousure, text = yesbuttonlabel.get(), command = finish, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 2, stick = W) 
        no = Button(areyousure, text = nobuttonlabel.get(), command = passclose, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 0, stick = W)
        
    def areyousure3():
        if varactive.get() != 1:
            areyousure2()
    def complete():
        def areyousure2():
            savenotesfile()
            opennote(txtfilename.get())
        if len(e.get()) != 0 and len(e2.get()) != 0: 
            if e.get() == e2.get(): 
                mypassword.set(e.get()) 
                passwordentered.set(1)
                setpassopen.set(0)
                if txtfilename.get() != "":
                    notetext.focus_set()
                else:
                    txtfilename.focus_set()
                varactive.set(0)
                areyousure2()
                setapass.destroy() 
            else: 
                warninglabel.set("The two passwords are not equal!")
        else: 
            warninglabel.set("Password fields shouldn't be empty!")
    setpasslabel.set("Set the new password:")
    setpassbuttonlabel.set("Change password")
    setapass.title("Set A New Password")
    confirmpasslabel.set("Confirm Password:")
    setapass.geometry(f'{550}x{110}+{int(xx-200)}+{int(yy-143)}')
    blanklabel = Label(mainframe, text = " ", bg='#bdbdbd').grid(row = 0) 
    warnlabel = Label(setapass, textvariable = warninglabel, bg='#bdbdbd', fg = "red").grid(row = 3, stick = W)
    label = Label(mainframe, text = setpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 1, stick = W)
    label = Label(mainframe, text = confirmpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 2, stick = W)
    e.grid(row = 1, column = 1, stick = W) 
    e2.grid(row = 2, column = 1, stick = W) 
    e2.config(show="*") 
    e.config(show="*") 
    e.focus_set()
    blanklabel = Label(mainframe, text = "    ", bg='#bdbdbd').grid(row = 1, column = 2, stick = W) 
    setpass = Button(mainframe, text = setpassbuttonlabel.get(), command = areyousure2, width = 15, bg='lightgrey', borderwidth = 5, font=("Arial", 10, "bold")).grid(row = 2, column = 3, stick = W) 
    e.bind("<Return>", lambda event: e2.focus_set())
    e2.bind("<Return>", lambda event: areyousure3())
        
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
    if passwordentered.get() == 1 and len(txtname) > 0 and txtname != "NULL" and txtname != "NULL.txt" and ("_decrypted" not in txtname):
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
    elif txtname == "":
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Name cannot be empty!")
    elif "_decrypted" in txtname:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Name cannot contain \"_decrypted\"!")
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
    txtfilename.delete(0, END)
    txtfilename.insert(INSERT, txtname)
    notetext.delete("1.0", "end")
    if mode == 1:
        txtfilename.delete(0, END)
        txtfilename.insert(INSERT, txtname)
    if "_decrypted" in txtname:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Name cannot contain _decrypted")
        return
    filename = txtname
    if not txtname.endswith(".txt"):
        filename = str(txtname + ".txt")
    if not os.path.isfile(filename):
        if os.path.isfile(filename + ".txt"):
            filename = filename + ".txt"
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
    failed.geometry(f'{200}x{50}+{int(xx+215)}+{int(yy+87)}')
    Label(failed, text = "        ", bg='#bdbdbd').grid(row = 0)
    Label(failed, text = "           FAILED!", fg = "red", font = ("bold", 14), bg='#bdbdbd').grid(row = 1)
    Label(failed, text = "        ", bg='#bdbdbd').grid(row = 2)

def successwin(text, filename = "", geom = "250x100"):
    success = Toplevel(master)
    success.title("SUCCESS!")
    success.resizable(width = False, height = False)
    success.geometry(f'{geom}+{int(xx+215)}+{int(yy+36)}')
    success.config(bg='#bdbdbd')
    Label(success, text = "        ", bg='#bdbdbd').grid(row = 0)
    Label(success, text = ("          " + text +"!   "), fg = "green", font = ("bold", 14), bg='#bdbdbd').grid(row = 1)
    if filename != "":
        Button(success, text = " Open ", command = lambda: opennote(filename), width = 10, height = 1).grid(row = 1, column = 1, stick = W)
    Label(success, text = "        ", bg='#bdbdbd').grid(row = 2)

def separatewith():
    separatewindow = Toplevel(master)
    separatewindow.title("Note separation")
    separatewindow.resizable(width = False, height = False)
    separatewindow.config(bg='#bdbdbd')
    separatewindow.geometry(f'{320}x{130}+{int(xx+215)}+{int(yy)}')
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
    sep.focus_set()
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
                close()
                notetext.focus_set()
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
    noteswindow.geometry(f'{410}x{300}+{int(xx+215)}+{int(yy+170)}')
    def notesclose(): 
        noteslistopen.set(0) 
        noteswindow.destroy() 
    noteswindow.protocol("WM_DELETE_WINDOW", notesclose)
    noteslistopen.set(1)
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
    onlyreadablevar = IntVar()
    checkednoteslist = []
    def checkednote(filename):
        if filename in checkednoteslist:
            checkednoteslist.remove(filename)
        else:
            checkednoteslist.insert(0, filename)
    def deleteitems():
        failed = 0
        for a in checkednoteslist:
            try:
                os.remove(a + ".txt")
            except:
                failedwin()
                return
        successwin("Deleted Succesfully")
        listthem()
    def onlyreadable():
        if passwordentered.get() == 1:
            if onlyreadablevar.get() == 1:
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
                files = listmyfiles()
                i = 0
                for f in files:
                    tempdec = checkdec(f)
                    if tempdec == 1:
                        text = str(f).removesuffix('.txt')
                        text2 = text
                        if len(text) > 45:
                            text2 = shorten(text, 45)
                        Label(frame_buttons, text = "      ", bg='#bdbdbd').grid(row = i, column = 0, stick = E)
                        Label(frame_buttons, text = text2, bg='#bdbdbd').grid(row = i, column = 1, stick = E)
                        Label(frame_buttons, text = "       ", bg='#bdbdbd').grid(row = i, column = 2, stick = E)
                        tempvar = IntVar()
                        Button(frame_buttons, text = "    Open   ", command = lambda text2 = text: opennote(text2, 1)).grid(row = i, column = 3, sticky = E)
                        notecheckbutton = Checkbutton (frame_buttons, text = "", variable = tempvar, command = lambda filename = text: checkednote(filename), bg='#bdbdbd').grid(row = i, column = 4, stick = W)
                        i += 1
            else:
                listthem()
    def listthem():
        if onlyreadablevar.get() == 1:
            onlyreadable()
            return
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
        files = listmyfiles()
        i = 0
        for f in files:
            if "_decrypted" not in str(f):
                text = str(f).removesuffix('.txt')
                text2 = text
                if len(text) > 45:
                    text2 = shorten(text, 45)
                Label(frame_buttons, text = "      ", bg='#bdbdbd').grid(row = i, column = 0, stick = E)
                Label(frame_buttons, text = text2, bg='#bdbdbd').grid(row = i, column = 1, stick = E)
                Label(frame_buttons, text = "       ", bg='#bdbdbd').grid(row = i, column = 2, stick = E)
                Button(frame_buttons, text = "    Open   ", command = lambda text2 = text: opennote(text2, 1)).grid(row = i, column = 3, sticky = E)
                tempvar = IntVar()
                notecheckbutton = Checkbutton (frame_buttons, text = "", variable = tempvar, command = lambda filename = text: checkednote(filename), bg='#bdbdbd').grid(row = i, column = 4, stick = W)
                i += 1
    refreshbutton = Button(mainframe, text = "Refresh", width=20, height=1, command=listthem).grid(row = 0, stick = W)
    onlyreadablecheck = Checkbutton (mainframe, text = "Only Readable", variable = onlyreadablevar, command = onlyreadable, bg='#bdbdbd').grid(row = 0, column = 2, stick = W)
    onlyreadablevar.set(1)
    onlyreadable()
    deletebutton = Button(mainframe, text = "Delete Selected", width=20, height=1, command = deleteitems).grid(row = 0, column = 1, stick = W)
    listthem()
    noteswindow.bind("<Return>", lambda event: listthem())
def opennoteslist2():
    if noteslistopen.get() != 1:
        opennoteslist()
    else:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Notes already open")
def searchinfiles():
    noteswindow = Toplevel(master)
    noteswindow.title("Search")
    noteswindow.resizable(height = False, width = False)
    noteswindow.config(bg='#bdbdbd')
    noteswindow.geometry(f'{410}x{25}+{int(xx+215)}+{int(yy)}')
    def searchclose(): 
        searchopen.set(0)
        noteswindow.destroy() 
    noteswindow.protocol("WM_DELETE_WINDOW", searchclose)
    searchopen.set(1)
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
        noteswindow.geometry(f'{410}x{300}+{int(xx+215)}+{int(yy)}')
        files = listmyfiles()
        i = 0
        found = 0
        for f in files:
            try:
                temp = open(f, "r")
                lines = temp.readlines()
                temp.close()
                for line in lines:
                    try:
                        line = decrypt(line)
                        if texttosearch.lower() in line.lower():
                            found += 1
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
                        break
            except:
                warningtextbox.delete("1.0", "end")
                warningtextbox.insert(INSERT, "Error!")
        if found == 0:
            noteswindow.geometry("410x50")
            Label(frame_buttons, text = "                                                 ", bg='#bdbdbd').grid(row = i, column = 0, stick = E)
            Label(frame_buttons, text = "Not Found", bg='#bdbdbd', fg = "red").grid(row = i, column = 1, stick = E)
    Label(mainframe, text = "Search:   ", bg='#bdbdbd').grid(row = 0, column = 0)
    texttosearchfor = Entry(mainframe, width = 40)
    texttosearchfor.grid(row = 0, column = 1)
    noteswindow.bind("<Return>", lambda event: searchtext(texttosearchfor.get()))
    searchbutton = Button(mainframe, text = "Seach", width = 15, height = 1, command= lambda: searchtext(texttosearchfor.get())).grid(row = 0, column = 2)
    texttosearchfor.focus_set()
def searchinfiles2():
    if searchopen.get() != 1:
        searchinfiles()
    else:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Search already open")
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
                if temp == 1:
                    return 0
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
    mergewindow.geometry(f'{400}x{400}+{int(xx+215)}+{int(yy+170)}')
    mainframe = Frame(mergewindow, bg='#bdbdbd')
    mainframe.grid(row = 0)
    errorlabel = StringVar()
    errorlabel.set("")
    #Label(mainframe, text = "  ", bg='#bdbdbd').grid(row = 0, stick = W)
    Label(mainframe, text = "Name of note to merge into: ", bg='#bdbdbd', font = ("Arial", 10, "bold")).grid(row = 0, column = 0, stick = W)
    notenametomergeinto = Entry(mainframe, bg='lightgrey')
    notenametomergeinto.grid(row = 0, column = 1, stick = W)
    notenametomergeinto.focus_set()
    Label(mergewindow, text = "Notes to merge separated by line:", bg='#bdbdbd', font = ("Arial", 10, "bold")).grid(row = 2, stick = W)
    notestomerge = Text(mergewindow, bg='lightgrey', height = 10, width = 20)
    notestomerge.grid(row = 3, column = 0, stick = W)
    def finishadding(items):
        if len(items) != 0:
            for item in items:
                notestomerge.insert(INSERT, item + "\n")
    def checknotestoadd():
        noteswindow = Toplevel(master)
        noteswindow.title("Note Selection")
        noteswindow.resizable(height = False, width = False)
        noteswindow.config(bg='#bdbdbd')
        noteswindow.geometry(f'{410}x{300}+{int(xx+215)}+{int(yy+170)}')
        def notesclose(): 
            checknotestoaddopen.set(0) 
            noteswindow.destroy() 
        noteswindow.protocol("WM_DELETE_WINDOW", notesclose)
        checknotestoaddopen.set(1)
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
        checkednoteslist = []
        def checkednote(filename):
            if filename in checkednoteslist:
                checkednoteslist.remove(filename)
            else:
                checkednoteslist.insert(0, filename)
            print(filename)
        def finishaddinginit(items):
            finishadding(items)
            checknotestoaddopen.set(0)
            noteswindow.destroy()
        def listthem():
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
            files = listmyfiles()
            i = 0
            for f in files:
                if checkdec(f):
                    text = str(f).removesuffix('.txt')
                    text2 = text
                    if len(text) > 45:
                        text2 = shorten(text, 45)
                    Label(frame_buttons, text = "      ", bg='#bdbdbd').grid(row = i, column = 0, stick = E)
                    Label(frame_buttons, text = text2, bg='#bdbdbd').grid(row = i, column = 1, stick = E)
                    Label(frame_buttons, text = "       ", bg='#bdbdbd').grid(row = i, column = 2, stick = E)
                    Checkbutton(frame_buttons, text = "  add  ", command = lambda filename = text: checkednote(filename), bg='#bdbdbd').grid(row = i, column = 3, sticky = E)
                    i += 1
        refreshbutton = Button(mainframe, text = "Refresh", width=20, height=1, command=listthem, bg='lightgrey').grid(row = 0, stick = W)
        finishbutton = Button(mainframe, text = "Finish", width = 15, height = 1, command = lambda: finishaddinginit(checkednoteslist), bg = 'lightgrey').grid(row = 0, column = 1, stick = W)
        listthem()
        noteswindow.bind("<Return>", lambda event: finishaddinginit(checkednoteslist))
    def checknotestoadd2():
        if checknotestoaddopen.get() != 1:
            checknotestoadd()
        else:
            warningtextbox.delete("1.0", "end")
            warningtextbox.insert(INSERT, "Notes selection already open")
    def addanote():
        filename = askopenfilename()
        notestomerge.insert(INSERT, filename + "\n")
    buttonsframe = Frame(mergewindow)
    buttonsframe.grid(row = 4, stick = W)
    browsenotes = Button (buttonsframe, text = "Browse...", width = 10, height = 1, command = addanote).grid(row = 0, column = 0, stick = W)
    addthroughnoteslist = Button (buttonsframe, text = "Add with notes list", width = 20, height = 1, command = checknotestoadd2).grid(row = 0, column = 1, stick = W)
    cantopen = StringVar()
    filesdontexist = StringVar()
    cantdecrypt = StringVar()
    cantopen.set("Cannot open file: ")
    filesdontexist.set("Files that dont exist: ")
    cantdecrypt.set("Files that cannot be decrypted: ")
    totalfiles = IntVar()
    def startmerge():
        successes = 0
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
        if "_decrypted" in notenametomergeinto.get():
            errorlabel.set("Destination note name cannot contain \"_decrypted\"!")
            return
        mergeinto = (notenametomergeinto.get()).replace("\n","")
        origmergeinto = mergeinto
        if not origmergeinto.endswith(".txt"):
            origmergeinto += ".txt"
        mergeinto = mergeinto + "_temp.txt"
        lines = notestomerge.get("1.0", "end")
        isitempty = 1
        for line in lines.splitlines():
            if len(line.strip(" ")) != 0:
                isitempty = 0
        if isitempty == 1:
            errorlabel.set("No sources!")
            return
        try:
            if mergeinto.endswith(".txt"):
                mainfile = open(mergeinto, "w+")
                openedmain = 1
            else:
                mainfile = open((mergeinto + ".txt"), "w+")
                openedmain = 1
        except:
            openedmain = 0
            errorlabel.set("Error while opening the main note")
            return
        opened = 0
        for line in lines.splitlines():
            totalfiles.set(totalfiles.get()+1)
            if line.endswith(".txt"):
                filename = line.replace("\n", "")
            else:
                filename = line.replace("\n", "") + ".txt"
            if os.path.isfile(filename) and filename != ".txt":
                try:
                    if checkdec(filename) == 1:
                        tempfile = open(filename, "r")
                        opened = 1
                        lines2 = tempfile.readlines()
                        for line2 in lines2:
                            mainfile.write(line2)
                        successes += 1
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
                if filename != ".txt":
                    errorlabel.set("No such note as " + filename)
                    filesdontexist.set((filesdontexist.get() + filename + ", "))
                    errors += 1
        if openedmain == 1 and opened == 1 and errors == 0 and successes != 0:
            mainfile.close()
            if os.path.isfile(origmergeinto):
                os.remove(origmergeinto)
                os.rename(mergeinto, origmergeinto)
            else:
                os.rename(mergeinto, origmergeinto)
            successwin("SUCCESS", origmergeinto)
        elif openedmain == 1 and (errors > 0 and errors < totalfiles.get()) and successes != 0:
            mainfile.close()
            if os.path.isfile(origmergeinto):
                os.remove(origmergeinto)
                os.rename(mergeinto, origmergeinto)
            else:
                os.rename(mergeinto, origmergeinto)
            successwin("SUCCESS WITH A\nFEW ERRORS", origmergeinto, "300x100")
        elif errors > 0:
            mainfile.close()
            os.remove(mergeinto)
            failedwin()
    Button(mainframe, text = "Merge", command = startmerge, width = 10, font = ("bold", 10)).grid(row = 0, column = 2, stick = W)
    Label(mergewindow, textvariable = filesdontexist, bg='#bdbdbd').grid(row = 6, stick = W)
    Label(mergewindow, textvariable = cantopen, bg='#bdbdbd').grid(row = 7, stick = W)
    Label(mergewindow, textvariable = cantdecrypt, bg='#bdbdbd').grid(row = 8, stick = W)
    Label(mergewindow, textvariable = errorlabel, fg = "red", bg='#bdbdbd').grid(row = 5, stick = W)

def openfilethroughbrowser():
    if passwordentered.get() == 1:
        filename = askopenfilename()
        filename = filename.replace(".txt", "")
        opennote(filename)
    else:
        warningtextbox.delete("1.0", "end")
        warningtextbox.insert(INSERT, "Set a password")
menu = Menu(master) 
master.config(menu = menu, bg='#bdbdbd') 
tools = Menu(menu, tearoff = 0)
menu.add_command(label = "Open...", command = openfilethroughbrowser)
menu.add_cascade(label = "Tools", menu = tools)
tools.add_command(label = "Export Decrypted Note", command = exportdecrypted)
tools.add_command(label = "Separate note", command = separatewith)
tools.add_command(label = "Merge notes", command = mergenotes)
tools.add_command(label = "Rename opened note with the currently entered name", command = lambda: renamenoteinit(openednotename.get(), txtfilename.get()))
menu.add_command(label = "Notes", command = opennoteslist2)
menu.add_command(label = "Search", command = searchinfiles2)
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
                if txtfilename.get() != "":
                    notetext.focus_set()
                else:
                    txtfilename.focus_set()
                setpassopen.set(0)
            else: 
                warninglabel.set("The two passwords are not equal!")
        else:
            warninglabel.set("Password fields shouldn't be empty!")
    setpasslabel.set("Set the new password of this note:")
    setpassbuttonlabel.set("Re-Encrypt")
    setapass.title("Re-Encryption")
    confirmpasslabel.set("Confirm Password:")
    setapass.geometry(f'{550}x{110}+{int(xx-200)}+{int(yy-143)}')
    blanklabel = Label(setapass, text = " ", bg='#bdbdbd').grid(row = 0) 
    warnlabel = Label(setapass, textvariable = warninglabel, bg='#bdbdbd', fg = "red").grid(row = 3, stick = W)
    label = Label(setapass, text = setpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 1, stick = W)
    label = Label(setapass, text = confirmpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 2, stick = W)
    e.grid(row = 1, column = 1, stick = W) 
    e2.grid(row = 2, column = 1, stick = W) 
    e2.config(show="*") 
    e.config(show="*") 
    e.bind("<Return>", lambda event: e2.focus_set())
    e2.bind("<Return>", lambda event: complete())
    e.focus_set()
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
firstframe.grid(row = 0, column = 0, stick = W)
firstframe2 = Frame(master, bg='#bdbdbd')
firstframe2.grid(row = 1, column = 0)
secondframe = Frame(master, bg='#bdbdbd')
secondframe.grid(row = 2, column = 0)
thirdframe = Frame(master, bg='#bdbdbd')
thirdframe.grid(row = 3, column = 0)
notetext = Text(secondframe, width = 50, borderwidth = 2, bg='lightgrey', height = 25)
notetext.grid(row = 3, column = 1)
textanalytics = StringVar()
textanalytics.set("Character Count: N/A\nLine Count: N/A")
txtfilename = Entry(firstframe, width = 42, borderwidth = 2, bg='lightgrey')
txtfilename.grid(row = 0, column = 1, stick = W)
opennotebutton = Button(firstframe2, text = "     Open the note         ", command = lambda:opennote(str(txtfilename.get()))).grid(row = 1, column = 1, stick = W)
createnotebutton = Button(firstframe2, text = "Create/Save the note", command = lambda: areyousure(1)).grid(row = 1, column = 0, stick = E)
tools.add_command(label = "Set/Change encryption and decryption password", command = changepassword)
tools.add_command(label = "Encrypt this note with other password", command = newpassword)
Label(firstframe, text = "Note name:", bg='#bdbdbd').grid (row = 0, column = 0, stick = W)
cleartextbox = Button(secondframe, text = "               Clear               ", command = lambda: notetext.delete("1.0", "end")).grid(row = 4, column = 1, stick = E)
copytoclip = Button(thirdframe, text = "Copy note to clipboard", command = copytoclipboard).grid(row = 5, column = 0, stick = E)
warninglabel = Label(thirdframe, text = "Warnings: ", bg='#bdbdbd').grid(row = 5, column = 2, stick = S)
warningtextbox = Text(thirdframe, width = 20, borderwidth = 2, bg='lightgrey', height = 1, fg = "red")
warningtextbox.grid(row = 6, column = 2, stick = N)
textanalyticslabel = Label(thirdframe, textvariable = textanalytics, bg='#bdbdbd').grid(row = 6, column = 0, stick = E)
txtfilename.bind('<Return>', opennote2)
notetext.bind('<Tab>', lambda event: notetext.insert (notetext.index(INSERT), "    "))
master.bind('<Escape>', lambda event: areyousure(mode = 3))
mainloop()







# Made by MaxiiKK at https://github.com/maxiikk/encryptednotesapp


"""
Needed modules for python to run this app:
    1. pycryptodome
    2. AES-Encryptor
    3. pyperclip





version = 1.5
"""