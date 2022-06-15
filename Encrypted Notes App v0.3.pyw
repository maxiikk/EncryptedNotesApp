from Encryptor import AES_Encryption
from tkinter import *
import os.path
import pyperclip as clip
from tkinter import ttk
import random
import struct 

master = Tk() 
master.title("Encrypted Notes App") 
master.geometry("600x320") 
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
    setpasslabel.set("Set a password:")
    setpassbuttonlabel.set("Set password")
    setapass.title("Set A Password First!")
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

setpassword()

def areyousure3(txtname):
    areyousure = Toplevel(master)
    areyousure.config(bg='#bdbdbd')
    areyousure.resizable(width=False, height=False)
    label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 0, column = 0, stick = W)
    label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 1, column = 0, stick = W)
    yesbuttonlabel = StringVar()
    nobuttonlabel = StringVar()
    def finish(txtname):
        createnote(txtname)
        areyousure.destroy()
    areyousure.title("Are you sure?")
    label = Label(areyousure, text = "Are you sure that you want to save the file?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
    yesbuttonlabel.set("Yes")
    nobuttonlabel.set("NO")
    yes = Button(areyousure, text = yesbuttonlabel.get(), command = lambda: finish(txtname), width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 2, stick = W) 
    no = Button(areyousure, text = nobuttonlabel.get(), command = areyousure.destroy, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 0, stick = W) 
def areyousure():
    areyousure = Toplevel(master)
    areyousure.config(bg='#bdbdbd')
    areyousure.resizable(width=False, height=False)
    label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 0, column = 0, stick = W)
    label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 1, column = 0, stick = W)
    yesbuttonlabel = StringVar()
    nobuttonlabel = StringVar()
    def finish():
        savenotesfile()
        areyousure.destroy()
    areyousure.title("Are you sure?")
    label = Label(areyousure, text = "Are you sure that you want to save the file?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
    yesbuttonlabel.set("Yes")
    nobuttonlabel.set("NO")
    yes = Button(areyousure, text = yesbuttonlabel.get(), command = finish, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 2, stick = W) 
    no = Button(areyousure, text = nobuttonlabel.get(), command = areyousure.destroy, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 0, stick = W) 
def changepassword():
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
    def areyousure2(): 
        areyousure = Toplevel(master)
        areyousure.config(bg='#bdbdbd')
        areyousure.resizable(width=False, height=False)
        label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 0, column = 0, stick = W)
        label = Label(areyousure, text = "   ", bg='#bdbdbd').grid(row = 1, column = 0, stick = W)
        yesbuttonlabel = StringVar()
        nobuttonlabel = StringVar()
        def finish():
            complete()
            areyousure.destroy()
        areyousure.title("Are you sure?")
        label = Label(areyousure, text = "Are you sure that you want to change the password?", bg='#bdbdbd').grid(row = 0, column = 1, stick = W)
        yesbuttonlabel.set("Yes")
        nobuttonlabel.set("NO")
        yes = Button(areyousure, text = yesbuttonlabel.get(), command = finish, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 2, stick = W) 
        no = Button(areyousure, text = nobuttonlabel.get(), command = areyousure.destroy, width = 15, bg='lightgrey', borderwidth = 5).grid(row = 2, column = 0, stick = W) 
    def complete():
        def areyousure2():
            savenotesfile()
        if len(e.get()) != 0 and len(e2.get()) != 0: 
            if e.get() == e2.get(): 
                mypassword.set(e.get()) 
                setpassopen.set(0) 
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
    setapass.geometry("550x110")
    blanklabel = Label(setapass, text = " ", bg='#bdbdbd').grid(row = 0) 
    warnlabel = Label(setapass, textvariable = warninglabel, bg='#bdbdbd', fg = "red").grid(row = 3, stick = W)
    label = Label(setapass, text = setpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 1, stick = W)
    label = Label(setapass, text = confirmpasslabel.get(), bg='#bdbdbd', font=("Sans Serif", 10, "bold")).grid(row = 2, stick = W)
    e.grid(row = 1, column = 1, stick = W) 
    e2.grid(row = 2, column = 1, stick = W) 
    e2.config(show="*") 
    e.config(show="*") 
    blanklabel = Label(setapass, text = "    ", bg='#bdbdbd').grid(row = 1, column = 2, stick = W) 
    setpass = Button(setapass, text = setpassbuttonlabel.get(), command = areyousure2, width = 15, bg='lightgrey', borderwidth = 5, font=("Arial", 10, "bold")).grid(row = 2, column = 3, stick = W) 
        
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
notetext = Text(master, width = 50, borderwidth = 2, bg='lightgrey', height = 10)
notetext.grid(row = 3, column = 1)
def createnote(txtname):
    if passwordentered.get() == 1 and len(txtname) > 0:
        filename = (txtname + ".txt")
        notefile = open(str(filename), 'w+')
        lines = notetext.get("1.0", "end")
        for line in lines.splitlines():
            try:
                k = encrypt(line)
                notefile.write(k +"\n")
                successfullydecrypted.set(1)
                warningtextbox.delete("1.0", "end")
                openednotename.set(txtfilename.get())
            except:
                successfullydecrypted.set(0)
                warningtextbox.delete("1.0", "end")
                warningtextbox.insert(INSERT, "Couldnt Encrypt")
        notefile.close()
    else:
        setpasswarning()

def opennote(txtname):
    notetext.delete("1.0", "end")
    filename = str(txtname + ".txt")
    print(filename)
    if os.path.isfile(filename):
        if passwordentered.get() == 1:
            notefile = open(filename, "r+")
            lines = notefile.readlines()
            notefile.close()
            for line in lines:
                try:
                    k = decrypt(line)
                    notetext.insert (INSERT, k +"\n")
                    successfullydecrypted.set(1)
                    openednotename.set(txtfilename.get())
                except:
                    successfullydecrypted.set(0)
                    warningtextbox.delete("1.0", "end")
                    warningtextbox.insert(INSERT, "Wrong Password")
                    break
                warningtextbox.delete("1.0", "end")
        else:
            warningtextbox.delete("1.0" , "end")
            warningtextbox.insert(INSERT, "No Password")
    else:
        warningtextbox.delete("1.0" , "end")
        warningtextbox.insert(INSERT, "Doesnt Exist")


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
    def encryptwithotherpassword():
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
        else:
            warningtextbox.delete("1.0", "end")
            warningtextbox.insert(INSERT, "None Successfully Opened Notes") 
    def complete():
        if len(e.get()) != 0 and len(e2.get()) != 0: 
            if e.get() == e2.get():
                reencryptionpassword.set(e.get())
                encryptwithotherpassword()
                setpassopen.set(0)
                setapass.destroy() 
            else: 
                warninglabel.set("The two passwords are not equal!")
        else:
            warninglabel.set("Password fields shouldn't be empty!")
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
  


txtfilename = Entry(master, width = 20, borderwidth = 2, bg='lightgrey')
txtfilename.grid(row = 0, column = 1, stick = W)
opennotebutton = Button(master, text = "     Open the note         ", command = lambda:opennote(str(txtfilename.get()))).grid(row = 1, column = 1, stick = W)
createnotebutton = Button(master, text = "Create/Save the note", command = lambda: areyousure3(txtfilename.get())).grid(row = 1, column = 0, stick = E)
encryptwith = Button(master, text = "Encrypt this note\nwith other password    ", command = newpassword).grid(row = 2, column = 1, stick = W)
changepass = Button(master, text = "Change encryption/\ndecryption password", command = changepassword).grid(row = 2, column = 0, stick = E)
Label(master, text = "File name: ", bg='#bdbdbd').grid (row = 0, column = 0, stick = E)
cleartextbox = Button(master, text = "               Clear               ", command = lambda: notetext.delete("1.0", "end")).grid(row = 4, column = 1, stick = E)
warninglabel = Label(master, text = "Warnings: ", bg='#bdbdbd').grid(row = 5, column = 1, stick = S)
warningtextbox = Text(master, width = 20, borderwidth = 2, bg='lightgrey', height = 1, fg = "red")
warningtextbox.grid(row = 6, column = 1, stick = S)
mainloop()







# Made by MaxiiKK at https://github.com/maxiikk/encryptednotesapp


"""
Needed modules for python to run this app:
    1. pycryptodome
    2. AES-Encryptor





version = 0.3
"""