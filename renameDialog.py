import os
from tkinter import *
from tkinter import ttk, messagebox, Event
from fileTool import fileOption

class RenameDialog(Toplevel):
    def __init__(self, list_files, fileOptioner):
        super().__init__()
        self.FLAG_GEN_1 = "1-999"
        self.FLAG_GEN_2 = "001-999"
        self.FLAG_GEN_3 = "a-z"
        self.list_files = list_files
        self.fileOptioner = fileOptioner
        self.list_fileParentPath = []
        self.list_fileName = []
        self.initUI()

    def initUI(self):
        self.title("Rename Dialog")
        
        f_top = Frame(self, relief=GROOVE, bd = 2)
        f_top.pack(side=TOP)
        f_center = Frame(self, relief=GROOVE, bd = 2)
        f_center.pack(side=TOP)
        f_sub = Frame(self, relief=GROOVE, bd = 2)
        f_sub.pack(side=TOP)
        f_listFile = Frame(f_center, relief=GROOVE, bd=2)
        f_listFile.pack(side=LEFT)
        f_input = Frame(f_center, relief=GROOVE, bd=2)
        f_input.pack(side=LEFT)

        self.int_ck = IntVar()
        ckbtn = Checkbutton(f_top, text="使用规则批量命名", variable=self.int_ck, command=self.doCk)
        ckbtn.pack(side=LEFT)
        self.str_name_1 = StringVar()
        self.str_name_2 = StringVar()
        self.str_name_3 = StringVar()
        entry_name_1 = Entry(f_top, textvariable=self.str_name_1)
        entry_name_1.pack(side=LEFT)
        self.gen_choose = ttk.Combobox(f_top, textvariable=self.str_name_2, state="readonly")
        self.gen_choose['values'] = (self.FLAG_GEN_1, self.FLAG_GEN_2, self.FLAG_GEN_3)
        self.gen_choose.current(0)
        self.gen_choose.pack(side=LEFT)
        Label(f_top, text=" . ").pack(side=LEFT)
        entry_name_3 = Entry(f_top, textvariable=self.str_name_3)
        entry_name_3.pack(side=LEFT)
        entry_name_1.bind("<Return>",self.doCk)
        entry_name_3.bind("<Return>",self.doCk)


        Label(f_listFile, text="文件原名：").pack(side=TOP)
        Label(f_input, text="修改名：").pack(side=TOP)

        self.text_input = Text(f_input, height=30,width=30)
        self.text_input.pack(side=TOP)
        btn_doRe = Button(f_sub, text="rename all file", command=self.doRename).pack(side=TOP)
        for file in self.list_files:
            self.list_fileParentPath.append(os.path.split(file)[0])
            self.list_fileName.append(os.path.split(file)[1])
        self.text_list_old = Text(f_listFile, height=30,width=30, background="beige")
        self.text_list_old.pack(side=TOP)
        for fileName in self.list_fileName:
            self.text_list_old.insert(END, fileName + "\n")
        self.text_list_old.config(state=DISABLED)
    def doCk(self, event=None):
        print("RenameDialog.doCk()")
        if self.int_ck.get() == 1:
            print(self.int_ck.get())
            if self.str_name_1.get() == "":
                self.str_name_1.set(self.list_fileName[0].split(".")[0])
                self.str_name_3.set(self.list_fileName[0].split(".")[1])
            n = 1
            self.text_input.delete(1.0, END)
            for filename in self.list_fileName:
                new_name = ""
                if self.str_name_2.get() == self.FLAG_GEN_1:
                    new_name = self.str_name_1.get() + "_" + str(n) + "." + self.str_name_3.get()
                if self.str_name_2.get() == self.FLAG_GEN_2:
                    new_name = self.str_name_1.get() + "_" + "000"[len(str(n)):3] + str(n) + "." + self.str_name_3.get()
                if self.str_name_2.get() == self.FLAG_GEN_3:
                    if len(self.list_files) < 27:
                        new_name = self.str_name_1.get() + "_" + chr(n + 96) + "." + self.str_name_3.get()
                    else:
                        messagebox.showerror(title="ERROR", message="文件超过 26 个，请选择其他扩展格式。")
                        self.gen_choose.current(0)
                n = n + 1
                self.text_input.insert(END, new_name + "\n")
        else:
            print(self.int_ck.get())
            self.str_name_1.set("")
            self.str_name_2.set("")
            self.str_name_3.set("")

    def doRename(self):
        print("RenameDialog.doRename...")
        str_input = self.text_input.get(1.0,END)
        list_name_new = []
        list_temp = str_input.split("\n")
        print(len(list_temp))
        print(len(self.list_files))
        for i in range(len(list_temp)):
            new_name = ''.join(list_temp[i].split())
            if new_name != "":
                list_name_new.append(os.path.join(self.list_fileParentPath[i],new_name))
        print("========list_new_name========")
        print(list_name_new)
        print("========self.list_files======")
        print(self.list_files)
        if len(self.list_files) == len(list_name_new):
            self.fileOptioner.renameFiles(self.list_files, list_name_new)
        else:
            messagebox.showerror(title="ERROR", message="文件 与 文件名 数量不一致！")